import pandas as pd
from collections import Counter

# 文件路径
files = {
    "train": "data/cx/DeepHost_y_train.csv",
    "val": "data/cx/DeepHost_y_val.csv",
    "test": "data/cx/DeepHost_y_test.csv"
}

# 用于统计
unique_species_per_file = {}
total_species_counter = Counter()

# 遍历每个文件
for name, path in files.items():
    df = pd.read_csv(path, header=None)  # 没有表头
    species_list = df[0].dropna().astype(str).str.strip().tolist()
    
    # 获取当前文件的独立物种集合
    unique_species = set(species_list)
    unique_species_per_file[name] = unique_species
    
    # 统计物种出现的总次数
    total_species_counter.update(species_list)

# 获取所有文件的独立物种集合
all_unique_species = set().union(*unique_species_per_file.values())

# 打印每个文件的独立物种数
print("每个文件的独立物种数：")
for name, species_set in unique_species_per_file.items():
    print(f"{name}: {len(species_set)} 个物种")

# 统计训练集与验证集和测试集的交集
train_species = unique_species_per_file["train"]
val_species = unique_species_per_file["val"]
test_species = unique_species_per_file["test"]

# 计算交集
val_intersection_with_train = val_species.intersection(train_species)
test_intersection_with_train = test_species.intersection(train_species)

# 输出交集结果
print(f"\n验证集与训练集的交集：{len(val_intersection_with_train)} 个物种")
print(f"测试集与训练集的交集：{len(test_intersection_with_train)} 个物种")

# 输出总的独立物种数
print(f"\n总共独立物种数: {len(all_unique_species)}")

print("\n生成物种统计 TXT 文件...")

# 将结果写入 TXT 文件
with open("species_count.txt", "w", encoding="utf-8") as f:
    f.write("物种名\t出现次数\n")
    for species, count in total_species_counter.most_common():
        f.write(f"{species}\t{count}\n")

print("完成！输出文件为：species_count.txt")
