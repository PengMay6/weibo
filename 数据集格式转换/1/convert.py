# [["银色 的 罗马 高跟 鞋 ， 圆球 吊饰 耳饰 单 带 ， 个性 十足 ， 有 非常 抢眼 ！", 1], ["稳 吾 到 嘛 ？\n", 3]]
# 转化为
#银色的罗马高跟鞋，圆球吊饰耳饰单带个性十足，有非常抢眼！,1
#稳吾到嘛？\n,3


import json
import csv

# 读取JSON文件
with open('train.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# 去除空格并转换第二个数据，然后分别写入不同的CSV文件
for item in data:
    processed_item = [entry.strip() if isinstance(entry, str) else entry for entry in item]
    # 转换第二个数据
    if len(processed_item) > 1:
        if processed_item[1] == 0:
            processed_item[1] = 1
        elif processed_item[1] in [1, 5]:
            processed_item[1] = 2
        elif processed_item[1] in [2, 3, 4]:
            processed_item[1] = 0
        # 根据转换后的结果写入不同的CSV文件
        filename = f'output_{processed_item[1]}.csv'
        with open(filename, 'a', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(processed_item)

