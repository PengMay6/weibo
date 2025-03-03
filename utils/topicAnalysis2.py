import json
import re
import requests
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 创建一个Session对象来维持会话
session = requests.Session()

headers = {
    "Host": "www.wrd.cn",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Origin": "https://www.wrd.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "browser-h": "730",
    "browser-w": "980"
}


def getWeiAI(ciTiao):
    global names, nums
    payload = {
        "keyword": ciTiao,
        "title": ciTiao,
        "count": "0",
    }

    first_url = "https://www.wrd.cn/view/openTools/checkKeyword.action"
    # 发送第一个网址的POST请求
    response1 = session.post(first_url, headers=headers, data=payload)
    # 检查第一个请求的响应状态码
    if response1.status_code == 200:
        print("第一个网址请求成功！")
    else:
        print(f"第一个网址请求失败，状态码：{response1.status_code}")

    # 词云图
    second_url = "https://www.wrd.cn/view/openTools/goMoreWordsOTChart.action"
    # 发送第二个网址的POST请求（使用了上面的会话对象）
    response2 = session.post(second_url, headers=headers, data=payload)

    # 检查第二个请求的响应状态码
    if response2.status_code == 200:
        print("第二个网址请求成功！")
        # 尝试解析第二个请求的JSON格式数据
        try:
            second_data = response2.json()
            # print("第二个网址的JSON格式数据：", second_data)
            generate_wordcloud(second_data['li'], ciTiao)
        except requests.exceptions.JSONDecodeError:
            print("第二个网址返回的不是JSON数据")
    else:
        print(f"第二个网址请求失败，状态码：{response2.status_code}")

    # 情感占比柱状图
    third_url = 'https://www.wrd.cn/view/openTools/emotionStatAnalysisChartOTChart.action'
    response3 = session.post(third_url, headers=headers, data=payload)
    if response3.status_code == 200:
        print("第三个网址请求成功！")
        try:
            third_data = response3.json()
            # print("第三个网址的JSON格式数据：", third_data)
            names, nums = getCharData(third_data['data'])

        except requests.exceptions.JSONDecodeError:
            print("第三个网址返回的不是JSON数据")
    else:
        print(f"第三个网址请求失败，状态码：{response3.status_code}")

    # 微博话题情绪走势
    fourth_url = 'https://www.wrd.cn/view/openTools/emotionLineChartOTChart.action'
    response4 = session.post(fourth_url, headers=headers, data=payload)
    if response4.status_code == 200:
        print("第四个网址请求成功！")
        try:
            mood_trend_data = response4.json()
            # print("第三个网址的JSON格式数据：", third_data)
            # names, nums = getCharData(third_data['data'])
            return names, nums, mood_trend_data
        except requests.exceptions.JSONDecodeError:
            print("第四个网址返回的不是JSON数据")
    else:
        print(f"第四个网址请求失败，状态码：{response4.status_code}")


# 词云图
def generate_wordcloud(data_str, topicName):
    # 用正则表达式找到所有 { } 内的对象
    pattern = r"{name:'(.*?)',value:(.*?),label:'.*?',itemStyle: {normal: {color: '.*?'}}}"
    matches = re.findall(pattern, data_str)

    # 构建新的字典列表
    result_list = []
    for match in matches:
        name = match[0]
        value = int(match[1])
        result_list.append({"name": name, "value": value})
    # 创建词频字典
    word_freq = {item['name']: item['value'] for item in result_list}
    # 生成词云
    wordcloud = WordCloud(font_path=r'C:\Windows\Fonts\simhei.ttf', width=800, height=400,
                          background_color='white').generate_from_frequencies(word_freq)
    # 保存词云图
    wordCloudPath = f'static\wordCloud_2\{topicName}.png'
    wordcloud.to_file(wordCloudPath)
    return True


# 情绪柱状图
def getCharData(data):
    # print(type(data))
    # print(data)
    names = [item['name'] for item in data]
    nums = [item['value'] for item in data]
    return names, nums


# # 微博话题情绪走势
# def getMoodTrend():


if __name__ == '__main__':
    getWeiAI('追风者声明')
