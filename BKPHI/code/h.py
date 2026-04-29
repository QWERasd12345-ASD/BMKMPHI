#import csv

# 定义路径
#input_csv = 'data/dh/phage_host_labels.csv'
#output_csv = 'data/dh/label.csv'

# 读取原始CSV文件并处理宿主名称
#with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
    #reader = csv.reader(infile)
    #writer = csv.writer(outfile)
    
    #for row in reader:
        #if row:  # 确保行不为空
            #host_name = row[0].strip('"')  # 去掉双引号
            #host_name_parts = host_name.split()  # 按空格分割宿主名称
            #if len(host_name_parts) >= 2:  # 如果宿主名称至少有两个部分
                #short_host_name = ' '.join(host_name_parts[:2])  # 只保留前两个部分
            #else:
                #short_host_name = host_name  # 如果不足两个部分，保留原名称
            #writer.writerow([short_host_name])  # 写入新的CSV文件

#print(f"处理后的宿主标签CSV文件已保存到: {output_csv}")



import csv
from collections import defaultdict

# 定义文件路径
file_paths = [
    'data/cx/DeepHost_y_test.csv',
    'data/cx/DeepHost_y_train.csv',
    'data/cx/DeepHost_y_val.csv'
]
output_file = 'data/cx/bacteria_count_sorted.txt'

# 统计细菌名称出现的次数
bacteria_count = defaultdict(int)

# 读取每个 CSV 文件
for file_path in file_paths:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:  # 忽略空行
                    bacteria_name = row[0].strip()  # 假设细菌名称在第一列
                    bacteria_count[bacteria_name] += 1
    except FileNotFoundError:
        print(f"错误：文件 {file_path} 未找到，请检查路径是否正确。")
        exit()

# 按照次数从多到少排序
sorted_bacteria = sorted(bacteria_count.items(), key=lambda x: x[1], reverse=True)

# 将结果写入 TXT 文件
try:
    with open(output_file, 'w', encoding='utf-8') as file:
        for name, count in sorted_bacteria:
            file.write(f"{name}: {count} 次\n")
    print(f"统计完成，结果已写入 {output_file}")
except IOError:
    print(f"错误：无法写入文件 {output_file}，请检查路径和权限。")