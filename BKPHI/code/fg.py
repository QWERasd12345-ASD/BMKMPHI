import os
from Bio import SeqIO
import pandas as pd

def split_sequence(sequence, length):
    """
    将一个DNA序列分割成多个小段，每个段的长度为指定的length。
    """
    return [sequence[i:i+length] for i in range(0, len(sequence), length) if len(sequence[i:i+length]) == length]

def process_fasta(fasta_file, label_file, output_fasta, output_label, segment_length=5000):
    """
    根据给定的fasta文件和标签文件，分割序列并输出新的fasta文件和标签文件。
    
    :param fasta_file: 原始的fasta文件路径
    :param label_file: 对应的标签csv文件路径
    :param output_fasta: 输出的新的fasta文件路径
    :param output_label: 输出的新的标签文件路径
    :param segment_length: 分割后每段的长度，默认为5000
    """
    
    # 读取标签文件
    labels = pd.read_csv(label_file, header=None)
    
    # 创建输出文件
    with open(output_fasta, 'w') as fasta_out, open(output_label, 'w') as label_out:
        seq_id = 0  # 用于生成分割后序列的序号
        for record in SeqIO.parse(fasta_file, "fasta"):
            original_sequence = str(record.seq)
            # 分割序列
            segments = split_sequence(original_sequence, segment_length)
            for i, segment in enumerate(segments, start=1):
                # 为每个分割后的序列生成新的ID，后面加上分割后的序号
                new_id = f"{record.id}_{i}"
                # 写入新的fasta文件
                fasta_out.write(f">{new_id}\n{segment}\n")
                # 写入新的标签文件，标签与原始标签一致
                label_out.write(f"{labels.iloc[seq_id, 0]}\n")
            
            seq_id += 1

if __name__ == "__main__":
    # 输入文件路径和输出文件路径
    fasta_file = "data/cx/DeepHost_train.fasta"   # 原始的fasta文件
    label_file = "data/cx/DeepHost_y_train.csv"    # 对应的标签文件
    output_fasta = "data/5kd/c_TR.fasta"  # 分割后的fasta文件
    output_label = "data/5kd/c_TR.csv"  # 分割后的标签文件
    
    # 运行处理函数，5000bp为默认分割长度
    process_fasta(fasta_file, label_file, output_fasta, output_label, segment_length=5000)

    fasta_file1 = "data/cx/DeepHost_val.fasta"   # 原始的fasta文件
    label_file1 = "data/cx/DeepHost_y_val.csv"    # 对应的标签文件
    output_fasta1 = "data/5kd/c_V.fasta"  # 分割后的fasta文件
    output_label1 = "data/5kd/c_V.csv"  # 分割后的标签文件
    
    # 运行处理函数，5000bp为默认分割长度
    process_fasta(fasta_file1, label_file1, output_fasta1, output_label1, segment_length=5000)

    fasta_file2 = "data/cx/DeepHost_test.fasta"   # 原始的fasta文件
    label_file2 = "data/cx/DeepHost_y_test.csv"    # 对应的标签文件
    output_fasta2 = "data/5kd/c_TE.fasta"  # 分割后的fasta文件
    output_label2 = "data/5kd/c_TE.csv"  # 分割后的标签文件
    
    # 运行处理函数，5000bp为默认分割长度
    process_fasta(fasta_file2, label_file2, output_fasta2, output_label2, segment_length=5000)




