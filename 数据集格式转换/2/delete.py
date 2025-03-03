import pandas as pd

# 读取csv文件
df = pd.read_csv("usual_train.csv", header=None)

# 按第二列的不同值拆分数据框
grouped = df.groupby(1)

# 将分组后的数据保存到不同的csv文件中
for name, group in grouped:
    group.to_csv(f"usual_train_{name}.csv", index=False, header=False)
