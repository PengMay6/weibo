import csv

def count_numbers(csv_file):
    counts = {}
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过标题行
        for row in reader:
            label = row[1].strip()  # 获取第二列的标签并去除首尾空格
            if label.isdigit():  # 检查标签是否为数字
                if label in counts:
                    counts[label] += 1
                else:
                    counts[label] = 1
    return counts

csv_file = 'usual_train_2.csv'  # 替换为你的CSV文件路径
number_counts = count_numbers(csv_file)
print("每个数字的个数:")
for number, count in number_counts.items():
    print(f"数字 {number}: {count} 个")
