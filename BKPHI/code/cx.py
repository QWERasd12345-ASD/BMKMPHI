from Bio import SeqIO
import pandas as pd
import numpy as np

# 文件路径
fasta_files = ['data/DeepHost_train.fasta', 'data/DeepHost_val.fasta', 'data/DeepHost_test.fasta']
label_files = ['data/DeepHost_y_train.csv', 'data/DeepHost_y_val.csv', 'data/DeepHost_y_test.csv']

# 读取FASTA文件和标签文件
sequences = []
labels = []

for fasta_file, label_file in zip(fasta_files, label_files):
    # 读取FASTA文件
    seq_records = list(SeqIO.parse(fasta_file, "fasta"))
    sequences.extend(seq_records)  # 将所有序列添加到列表

    # 读取标签文件
    label_df = pd.read_csv(label_file, header=None)
    labels.extend(label_df.values.flatten())  # 将标签添加到列表

# 现在我们有了所有的序列和标签，准备按比例划分数据
# 将序列和标签打包成一个列表
data = list(zip(sequences, labels))

# 随机打乱数据
np.random.shuffle(data)

# 按照比例划分
train_split = int(0.8 * len(data))
val_split = int(0.9 * len(data))

train_data = data[:train_split]
val_data = data[train_split:val_split]
test_data = data[val_split:]

# 定义一个函数来保存FASTA和标签文件
def save_fasta_and_labels(data, fasta_filename, label_filename):
    sequences, labels = zip(*data)  # 拆分序列和标签
    # 保存FASTA文件
    SeqIO.write(sequences, fasta_filename, "fasta")
    # 保存标签文件
    pd.DataFrame(labels).to_csv(label_filename, header=False, index=False)
    
    # 输出FASTA文件的序列数量和标签文件的不重复标签数量
    num_sequences = len(sequences)
    num_labels = len(set(labels))  # 计算不重复的标签数量
    print(f"保存文件 {fasta_filename}：序列数量 = {num_sequences}")
    print(f"保存文件 {label_filename}：标签的唯一数量 = {num_labels}")

# 保存训练集、验证集和测试集
save_fasta_and_labels(train_data, 'data/cx/DeepHost_train.fasta', 'data/cx/DeepHost_y_train.csv')
save_fasta_and_labels(val_data, 'data/cx/DeepHost_val.fasta', 'data/cx/DeepHost_y_val.csv')
save_fasta_and_labels(test_data, 'data/cx/DeepHost_test.fasta', 'data/cx/DeepHost_y_test.csv')

print("数据处理完成！")
