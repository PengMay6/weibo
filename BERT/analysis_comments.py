# import pandas as pd
# import torch
# from transformers import BertTokenizer, BertForSequenceClassification
# from torch.utils.data import DataLoader, Dataset
# from tqdm import tqdm  # 导入tqdm
# from globalVariable import *
# # 模型和分词器所在的文件夹路径
# model_directory = r'BERT\MyBERT2'
#
#
#
# # 加载分词器和模型
# tokenizer = BertTokenizer.from_pretrained(model_directory)
# model = BertForSequenceClassification.from_pretrained(model_directory, num_labels=3)
# model.eval()  # 将模型设置为评估模式
#
# # 检查是否有可用的GPU
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.to(device)
#
#
# class TextDataset(Dataset):
#     def __init__(self, texts):
#         self.encodings = tokenizer(texts, truncation=True, padding=True, max_length=128, return_tensors="pt")
#
#     def __len__(self):
#         return len(self.encodings.input_ids)
#
#     def __getitem__(self, idx):
#         item = {key: val[idx] for key, val in self.encodings.items()}
#         return item
#
# def main(articleCommentsFilePath):
#     # 读取数据
#     df = pd.read_csv(articleCommentsFilePath)
#
#     # 创建数据加载器
#     text_dataset = TextDataset(df['content'].tolist())  # 使用 'content' 列
#     text_loader = DataLoader(text_dataset, batch_size=10, num_workers=3)  # 使用多个工作进程
#
#     # 预测函数
#     def predict(loader):
#         model.eval()
#         predictions = []
#         with torch.no_grad():
#             for batch in tqdm(loader, desc="Predicting"):  # 使用tqdm添加进度条
#                 batch = {k: v.to(device) for k, v in batch.items()}
#                 outputs = model(**batch)
#                 logits = outputs.logits
#                 preds = torch.argmax(logits, dim=1)
#                 predictions.extend(preds.cpu().numpy())
#         return predictions
#
#     # 进行预测
#     predictions = predict(text_loader)
#
#     # 将数值标签映射为文本标签
#     label_map = {0: '消极', 1: '中性', 2: '积极'}
#     text_labels = [label_map[pred] for pred in predictions]
#
#     # 将预测结果添加到DataFrame
#     df['sentiment'] = text_labels
#
#     # 保存预测结果到新的CSV文件
#     df.to_csv(articleCommentsFilePath, index=False)
#
#
# if __name__ == '__main__':
#     main()

import pandas as pd
import asyncio
import aiohttp
import time
from tqdm import tqdm  # 导入tqdm
from globalVariable import *
from collections import deque
# 配置参数
API_KEY = "B5W6ViVqOwzDE5F8rNVuw5PU"
SECRET_KEY = "zJCq1O4ZytWX5lNLHQWkOU3q5LqAzkfB"
QPS_LIMIT = 20  # 严格匹配配额
TOKEN_URL = "https://aip.baidubce.com/oauth/2.0/token"
API_URL = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify"


class HighPerformanceAnalyzer:
    def __init__(self):
        self.access_token = None
        self.token_expire = 0
        self.semaphore = asyncio.Semaphore(QPS_LIMIT)  # 精确控制并发
        self.rate_queue = deque(maxlen=QPS_LIMIT)  # 滑动窗口计数器

    async def _get_token(self):
        """异步获取Token"""
        async with aiohttp.ClientSession() as session:
            params = {
                "grant_type": "client_credentials",
                "client_id": API_KEY,
                "client_secret": SECRET_KEY
            }
            async with session.post(TOKEN_URL, params=params) as resp:
                data = await resp.json()
                self.access_token = data["access_token"]
                self.token_expire = time.time() + data["expires_in"] - 300  # 提前5分钟刷新

    async def _enforce_rate_limit(self):
        """精准速率控制"""
        now = time.time()
        # 移除1秒前的记录
        while self.rate_queue and self.rate_queue[0] < now - 1:
            self.rate_queue.popleft()

        # 如果当前窗口已达QPS限制，等待
        if len(self.rate_queue) >= QPS_LIMIT:
            oldest = self.rate_queue[0]
            wait_time = max(0, (oldest + 1) - now)
            await asyncio.sleep(wait_time)
            return await self._enforce_rate_limit()

        self.rate_queue.append(time.time())

    @staticmethod
    def _parse_result(data):
        """解析结果"""
        item = data["items"][0]
        sentiment = item["sentiment"]
        return ("积极", item["confidence"]) if sentiment == 2 else \
            ("中性", item["confidence"]) if sentiment == 1 else \
                ("消极", item["confidence"])

    async def analyze(self, text):
        """执行分析请求"""
        # 速率控制
        await self._enforce_rate_limit()

        # Token管理
        if not self.access_token or time.time() > self.token_expire:
            await self._get_token()

        # 发起请求
        async with self.semaphore:
            async with aiohttp.ClientSession(
                    connector=aiohttp.TCPConnector(limit=0, ssl=False)  # 不限制连接数
            ) as session:
                payload = {"text": text[:1024]}
                url = f"{API_URL}?charset=UTF-8&access_token={self.access_token}"

                try:
                    async with session.post(url, json=payload, timeout=3) as resp:
                        data = await resp.json()
                        if "error_code" in data:
                            raise Exception(data["error_msg"])
                        return self._parse_result(data)
                except Exception as e:
                    return ("请求失败", 0)


async def process_comments(comments):
    analyzer = HighPerformanceAnalyzer()
    # 初始化时间戳
    start_time = time.time()
    # 进度跟踪
    total = len(comments)
    processed = 0
    last_log = time.time()

    # 批量处理
    batch_size = QPS_LIMIT * 5  # 每批处理量
    results = []

    for i in range(0, total, batch_size):
        batch = comments[i:i + batch_size]
        tasks = [analyzer.analyze(comment) for comment in batch]

        # 实时输出进度
        for task in asyncio.as_completed(tasks):
            result = await task
            results.append(result)
            processed += 1

            # 每0.5秒输出进度
            if time.time() - last_log > 0.5:
                speed = processed / (time.time() - start_time)
                print(f"\r进度: {processed}/{total} | 速度: {speed:.1f} QPS", end="")
                last_log = time.time()

    return results


async def main_async(articleCommentsFilePath):
    # 读取数据
    df = pd.read_csv(articleCommentsFilePath)

    # 获取评论内容
    comments = df['content'].tolist()

    # 运行事件循环
    results = await process_comments(comments)

    # 将结果添加到DataFrame
    df['sentiment'] = [result[0] for result in results]

    # 保存预测结果到新的CSV文件
    df.to_csv(articleCommentsFilePath, index=False)


def main(articleCommentsFilePath):
    import asyncio
    asyncio.run(main_async(articleCommentsFilePath))


