import collections, sys, io
from collections import OrderedDict
from matplotlib import pyplot as plt
from matplotlib import cm
import pylab, math
from pyfaidx import Fasta
from collections import defaultdict
import random # 导入random模块

from PIL import Image
import numpy as np
#from torchvision import transforms

# ==============================================================================
# 新增：全局变量和函数用于管理随机kmer-坐标映射
# ==============================================================================
# 用于存储不同k值下的kmer到随机坐标的映射表
GLOBAL_KMER_RANDOM_POS_MAP = {}
# 用于确保随机映射的一致性，设置一个固定的随机种子
GLOBAL_RANDOM_SEED_FOR_CGR_MAPPING = 12345

def generate_all_kmers(k):
    """
    生成所有可能的kmer字符串。
    """
    bases = ['A', 'C', 'G', 'T']
    from itertools import product
    all_kmers = [''.join(p) for p in product(bases, repeat=k)]
    return all_kmers

def _initialize_random_kmer_mapping(k, array_size):
    """
    为给定k值初始化kmer到随机CGR坐标的映射。
    这个函数只会在每个k值第一次被使用时执行。
    """
    global GLOBAL_KMER_RANDOM_POS_MAP
    global GLOBAL_RANDOM_SEED_FOR_CGR_MAPPING

    # 如果这个k值对应的映射已经存在，则直接返回
    if k in GLOBAL_KMER_RANDOM_POS_MAP:
        return

    # 保存当前的随机状态，以便在生成映射后恢复
    current_random_state = random.getstate()
    # 设置固定的随机种子，确保每次程序运行生成相同的随机映射
    random.seed(GLOBAL_RANDOM_SEED_FOR_CGR_MAPPING)

    all_kmers = generate_all_kmers(k)
    
    # 生成所有可能的CGR坐标 (0-indexed)
    all_coords = []
    for y in range(array_size):
        for x in range(array_size):
            all_coords.append((x, y)) # 存储为 (x, y) 坐标

    # 随机打乱坐标顺序
    random.shuffle(all_coords)

    # 创建kmer到随机坐标的映射
    kmer_map = {}
    for i, kmer in enumerate(all_kmers):
        if i < len(all_coords): # 确保kmer数量不超过可用坐标数量 (通常是相等的)
            kmer_map[kmer] = all_coords[i]
        else:
            # 这通常不应该发生，因为kmer数量和坐标数量都是4^k
            sys.stderr.write(f"Warning: Not enough unique coordinates for all {k}-mers. Kmer: {kmer}\n")
            break

    GLOBAL_KMER_RANDOM_POS_MAP[k] = kmer_map
    
    # 恢复之前的随机状态
    random.setstate(current_random_state)
# ==============================================================================


def empty_dict():
	"""
	None type return vessel for defaultdict
	:return:
	"""
	return None

def count_kmers(sequence, k):
	d = collections.defaultdict(int)
	for i in range(len(sequence)-(k-1)):
		d[sequence[i:i+k]] += 1

	for key in list(d.keys()):
		if "N" in key: # 过滤掉包含N的kmer
			del d[key]
	return d

def probabilities(data, kmer_count, k):
	probabilities = collections.defaultdict(float)
	N = len(data)
	if (N - k + 1) <= 0: # 避免除以零或负数
		return probabilities
	for key, value in kmer_count.items():
		probabilities[key] = float(value) / (N - k + 1)
	return probabilities

def chaos_game_representation(probabilities, k):
	array_size = int(math.sqrt(4**k))
    
	# 调用初始化函数，确保随机映射表已为当前k值生成
	_initialize_random_kmer_mapping(k, array_size)
	kmer_map = GLOBAL_KMER_RANDOM_POS_MAP[k]

	chaos = []
	for i in range(array_size):
		chaos.append([0.0]*array_size) # 使用浮点数初始化，以存储概率值

	# 遍历kmer及其概率，根据随机映射填充CGR矩阵
	for key, value in probabilities.items():
		# 确保kmer在映射表中（count_kmers已经过滤了'N'，这里主要是为了健壮性）
		if key in kmer_map:
			posx, posy = kmer_map[key]
			# CGR通常是(y, x)索引，这里需要与你的原始实现保持一致，
			# 原始实现是 chaos[int(posy)-1][int(posx)-1]
			# 由于我们现在是0-indexed的坐标，所以直接使用posy, posx
			chaos[posy][posx] = value
		# 如果kmer不在映射表中（例如，因为它包含'N'，或者因为某种原因没有生成所有kmer），
		# 那么它将不会被放置在CGR中，这与原始行为一致。

	return chaos


