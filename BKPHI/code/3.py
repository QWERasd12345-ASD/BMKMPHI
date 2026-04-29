import random
import math
import matplotlib.pyplot as plt
from itertools import product

# 固定随机种子
GLOBAL_RANDOM_SEED_FOR_CGR_MAPPING = 12345

def generate_all_kmers(k):
    bases = ['A', 'C', 'G', 'T']
    return [''.join(p) for p in product(bases, repeat=k)]

def generate_random_kmer_mapping(k, seed):
    array_size = int(math.sqrt(4 ** k))
    all_kmers = generate_all_kmers(k)
    all_coords = [(x, y) for y in range(array_size) for x in range(array_size)]

    random.seed(seed)
    random.shuffle(all_coords)

    kmer_map = {}
    for i, kmer in enumerate(all_kmers):
        kmer_map[kmer] = all_coords[i]
    return kmer_map, array_size

def visualize_kmer_mapping(kmer_map, array_size, filename):
    fig, ax = plt.subplots(figsize=(16, 16))
    ax.set_xlim(-0.5, array_size - 0.5)
    ax.set_ylim(-0.5, array_size - 0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.invert_yaxis()  # 让坐标和图像一致，从上到下

    for kmer, (x, y) in kmer_map.items():
        ax.text(x, y, kmer, ha='center', va='center', fontsize=5)

    ax.set_title(f'CGR k-mer Mapping (k={k}, seed={GLOBAL_RANDOM_SEED_FOR_CGR_MAPPING})')
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print(f"✅ 图像已保存：{filename}")

if __name__ == "__main__":
    k = 6
    kmer_map, array_size = generate_random_kmer_mapping(k, GLOBAL_RANDOM_SEED_FOR_CGR_MAPPING)
    visualize_kmer_mapping(kmer_map, array_size, f'kmer_map_k{k}_seed{GLOBAL_RANDOM_SEED_FOR_CGR_MAPPING}.png')
