import os
from Bio import SeqIO
import pandas as pd
import random

def random_cut_sequence(sequence, length):
    """
    从一个DNA序列中随机截取一个长度为指定的length的子序列。
    
    :param sequence: 原始的DNA序列
    :param length: 要截取的子序列的长度
    :return: 随机截取的子序列
    """
    if len(sequence) < length:
        return None  # 如果序列长度小于要求的长度，返回None
    start_pos = random.randint(0, len(sequence) - length)  # 随机选择起始位置
    return sequence[start_pos:start_pos + length]

def process_fasta(fasta_file, label_file, output_fasta, output_label, segment_length=5000):
    """
    根据给定的fasta文件和标签文件，随机截取每条序列，并输出新的fasta文件和标签文件。
    
    :param fasta_file: 原始的fasta文件路径
    :param label_file: 对应的标签csv文件路径
    :param output_fasta: 输出的新的fasta文件路径
    :param output_label: 输出的新的标签文件路径
    :param segment_length: 截取的子序列长度，默认为5000
    """
    
    # 读取标签文件
    labels = pd.read_csv(label_file, header=None)
    
    # 创建输出文件
    with open(output_fasta, 'w') as fasta_out, open(output_label, 'w') as label_out:
        seq_id = 0  # 用于生成分割后序列的序号
        for record in SeqIO.parse(fasta_file, "fasta"):
            original_sequence = str(record.seq)
            # 随机截取序列
            segment = random_cut_sequence(original_sequence, segment_length)
            if segment:
                # 保持原序列的ID，不添加序号
                new_id = record.id
                # 写入新的fasta文件
                fasta_out.write(f">{new_id}\n{segment}\n")
                # 写入标签文件，标签与原始标签一致
                label_out.write(f"{labels.iloc[seq_id, 0]}\n")
            
            seq_id += 1

if __name__ == "__main__":
    # 输入文件路径和输出文件路径
    fasta_file = "data/cx/DeepHost_train.fasta"   # 原始的fasta文件
    label_file = "data/cx/DeepHost_y_train.csv"    # 对应的标签文件
    output_fasta = "data/1kd/D_TR.fasta"  # 分割后的fasta文件
    output_label = "data/1kd/D_TR.csv"  # 分割后的标签文件
    
    # 运行处理函数，5000bp为默认分割长度
    process_fasta(fasta_file, label_file, output_fasta, output_label, segment_length=5000)

    fasta_file1 = "data/cx/DeepHost_val.fasta"   # 原始的fasta文件
    label_file1 = "data/cx/DeepHost_y_val.csv"    # 对应的标签文件
    output_fasta1 = "data/1kd/D_V.fasta"  # 分割后的fasta文件
    output_label1 = "data/1kd/D_V.csv"  # 分割后的标签文件
    
    # 运行处理函数，5000bp为默认分割长度
    process_fasta(fasta_file1, label_file1, output_fasta1, output_label1, segment_length=5000)

    fasta_file2 = "data/cx/DeepHost_test.fasta"   # 原始的fasta文件
    label_file2 = "data/cx/DeepHost_y_test.csv"    # 对应的标签文件
    output_fasta2 = "data/1kd/D_TE.fasta"  # 分割后的fasta文件
    output_label2 = "data/1kd/D_TE.csv"  # 分割后的标签文件
    
    # 运行处理函数，5000bp为默认分割长度
    process_fasta(fasta_file2, label_file2, output_fasta2, output_label2, segment_length=5000)