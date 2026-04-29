import pandas as pd
from Bio import SeqIO

# 读取FASTA文件，提取细菌序列的名称（Accession）
def read_fasta_accessions(fasta_file):
    accessions = [record.id for record in SeqIO.parse(fasta_file, "fasta")]
    return accessions

# 生成目标CSV文件
def generate_prokaryote_csv(fasta_file, output_file):
    accessions = read_fasta_accessions(fasta_file)

    # 创建数据框，并添加空列
    prokaryote_df = pd.DataFrame({
        "Accession": accessions,
        "Superkingdom": [""] * len(accessions),  # 空白列
        "Phylum": [""] * len(accessions),       # 空白列
        "Class": [""] * len(accessions),        # 空白列
        "Order": [""] * len(accessions),        # 空白列
        "Family": [""] * len(accessions),       # 空白列
        "Genus": [""] * len(accessions),        # 空白列
        "Species": accessions,                  # Accession作为Species
        "Name": [""] * len(accessions)          # 空白列
    })

    # 写入CSV文件
    prokaryote_df.to_csv(output_file, index=False)

# 调用函数
fasta_file = "data/DeepHost_host_117.fasta"  # 替换为实际的FASTA文件路径
output_file = "prokaryote.csv"           # 输出的CSV文件路径

generate_prokaryote_csv(fasta_file, output_file)
