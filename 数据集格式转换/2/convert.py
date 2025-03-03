# usual_train.txt

import json
import csv

# 读取文本文件，并将内容解析为JSON格式
with open('usual_test_labeled.txt', 'r', encoding='utf-8') as f:
    data = json.loads(f.read())

# 创建CSV文件并写入数据
with open('usual_test_labeled.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['content', 'label']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # 遍历JSON数据并写入CSV文件
    for item in data:
        label = item['label']
        # 如果"label"是数字，则写入CSV文件
        if label.isdigit():
            # 将英文逗号修改为中文逗号
            content = item['content'].replace(',', '，')
            # 将英文句号修改为中文句号
            content = content.replace('.', '。')
            # 将英文问号修改为中文问号
            content = content.replace('?', '？')
            # 将英文感叹号修改为中文感叹号
            content = content.replace('!', '！')
            # 将英文冒号修改为中文冒号
            content = content.replace(':', '：')
            # 将英文分号修改为中文分号
            content = content.replace(';', '；')
            # 将英文引号修改为中文引号
            content = content.replace('"', '“').replace("'", "”")
            writer.writerow({'content': content, 'label': label})

print("转换完成！")
