import gzip
from scipy.stats import norm
import numpy as np


def get_allele_age_dict():
    out = {}
    with open('../baselineLD_bed/alleleage.bed', 'r') as f:
        for line in f.readlines():
            split_line = [a.strip() for a in line.split('\t')]
            out[(int(split_line[0].split('chr')[1]), int(split_line[2]))] = float(split_line[3])
    return out


def maf_bin(bin_num):
    print(f'Fetching MAF bin for bin number {bin_num}')
    vars = []
    for CHR in range(1, 23):
        with open(f'../g1000_plink_eur/1000G.EUR.QC.{CHR}.bim', 'r') as f:
            for line in f.readlines():
                split_line = [a.strip() for a in line.split('\t')]
                vars.append((int(split_line[0]), int(split_line[3])))
    maf_bin = []
    for CHR in range(1, 23):
        with gzip.open(f'../baseline_annot/MAFbin{bin_num}.{CHR}.annot.gz', 'r') as f:
            _ = f.readline()  # useless header row
            for line in f.readlines():
                maf_bin.append(line.strip() == b'1')
    out = []
    for (varId, in_bin) in zip(vars, maf_bin):
        if in_bin:
            out.append(varId)
    return out

c = 0

def get_var_dict(bin, allele_age):
    maf_vars = maf_bin(bin)
    ages = {}
    for varId in maf_vars:
        if varId in allele_age:
            age = allele_age[varId]
            if age not in ages:
                ages[age] = []
            ages[age].append(varId)
    total = sum([len(v) for k, v in ages.items()])

    var_dict = {}
    sorted_ages = sorted(ages)
    variants_less = 0
    for age in sorted_ages:
        varIds = ages[age]
        ranks = [variants_less + 1 + i for i in range(len(varIds))]
        rank_to_use = ranks[len(ranks) // 2] - 0.5 * (len(ranks) % 2 == 0)
        maf_age = norm.ppf((rank_to_use - c) / (total - 2 * c + 1))
        variants_less += len(varIds)
        for varId in varIds:
            var_dict[varId] = maf_age
    return var_dict


def make_annot_files(CHR, var_dict):
    print(f'Writing Chromosome {CHR}')
    with gzip.open(f'../baseline_annot/MAF_Adj_Predicted_Allele_Age.{CHR}.annot.gz', 'w') as f_out:
        f_out.write(b'ANNOT\n')
        with open(f'../g1000_plink_eur/1000G.EUR.QC.{CHR}.bim', 'r') as f_in:
            for line in f_in.readlines():
                split_line = [a.strip() for a in line.split('\t')]
                var_id = (int(split_line[0]), int(split_line[3]))
                f_out.write(str(round(var_dict[var_id], 6)).encode() + b'\n' if var_id in var_dict else b'0\n')


def main():
    allele_age = get_allele_age_dict()
    var_dict = {}
    for bin in range(1, 11):
        var_dict.update(get_var_dict(bin, allele_age))
    for CHR in range(1, 23):
        make_annot_files(CHR, var_dict)


if __name__ == '__main__':
    main()
