import numpy as np
import matplotlib.pyplot as plt
import gzip

maf_dict = {}
pos_dict = {}
with open('../baselineLD_bed/ASMC.bed', 'r') as f:
    for line in f.readlines():
        split_line = [a.strip() for a in line.split('\t')]
        maf_key = float(split_line[4])
        pos_key = (int(split_line[0]), int(split_line[2]))
        age = float(split_line[3])
        if maf_key not in maf_dict:
            maf_dict[maf_key] = []
        maf_dict[maf_key].append(age)
        pos_dict[pos_key] = (age, maf_key)

actual = []
ages = []
for CHR in range(1, 2):
    print(CHR)
    old_study = []
    with gzip.open(f'../baselineLD/baselineLD.{CHR}.annot.gz', 'r') as f:
        header = f.readline().split(b'\t')
        idx = [a.strip() for a in header].index(str.encode('MAF_Adj_ASMC'))
        for line in f.readlines():
            split_line = line.split(b'\t')
            old_study.append(split_line[idx].decode())

    g1000_positions = []
    with open(f'../g1000_plink_eur/1000G.EUR.QC.{CHR}.bim', 'r') as f:
        for i, line in enumerate(f.readlines()):
            split_line = [a.strip() for a in line.split('\t')]
            pos_key = (int(split_line[0]), int(split_line[3]))
            g1000_positions.append(pos_key)

    for actual_value, g1000_pos in zip(old_study, g1000_positions):
        if g1000_pos in pos_dict:
            maf = pos_dict[g1000_pos][1]
            if 0.05 <= maf <= 0.95:
                actual.append(float(actual_value))
                ages.append(pos_dict[g1000_pos][0])

plt.plot(ages, actual, '.')
plt.show()