import pandas as pd
from Bio import SeqIO
from sklearn.metrics import accuracy_score

# 读取FASTA文件，提取contig_name列表
def read_fasta(fasta_file):
    contig_names = []
    for record in SeqIO.parse(fasta_file, "fasta"):
        contig_names.append(record.id)
    return contig_names

# 读取标签文件
def read_labels(label_file):
    labels_df = pd.read_csv(label_file, header=None, names=["Host"])
    return labels_df["Host"].tolist()

# 读取预测结果文件
def read_predictions(pred_file):
    pred_df = pd.read_csv(pred_file)
    return pred_df

# 计算预测准确率
def compute_accuracy(fasta_file, label_file, pred_file):
    contig_names = read_fasta(fasta_file)
    true_labels = read_labels(label_file)
    pred_df = read_predictions(pred_file)

    # 生成真实 contig_name -> label 对应字典
    true_label_dict = dict(zip(contig_names, true_labels))

    # 生成预测 contig_name -> 预测 label 对应字典
    pred_label_dict = dict(zip(pred_df["contig_name"], pred_df["Top_1_label"]))

    # 确保所有的 contig_name 都有预测结果，若缺失，则视为错误
    y_true = []
    y_pred = []

    for contig in contig_names:
        y_true.append(true_label_dict[contig])  # 真实标签
        if contig in pred_label_dict:
            y_pred.append(pred_label_dict[contig])  # 预测标签
        else:
            y_pred.append("Unknown")  # 视为预测错误

    # 计算accuracy
    accuracy = accuracy_score(y_true, y_pred)
    print(f"预测准确率 (Accuracy): {accuracy:.4f}")

# 运行函数
fasta_file = "CHERRY-main/c_test.fasta"  # 替换为实际的FASTA文件路径
label_file = "CHERRY-main/c_y_test.csv"  # 替换为实际的标签文件路径
pred_file = "CH_final_prediction.csv"  # 替换为实际的预测结果文件路径

compute_accuracy(fasta_file, label_file, pred_file)
