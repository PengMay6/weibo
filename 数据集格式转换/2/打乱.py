import csv
import random

def shuffle_csv(file_path):
    # 读取CSV文件
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)  # 将CSV数据转换为列表

    # 随机打乱每一行数据
    random.shuffle(data)

    # 将打乱后的数据写入新的CSV文件
    with open('shuffled_' + file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

# 调用函数并传入CSV文件路径
shuffle_csv('usual_train2.csv')
