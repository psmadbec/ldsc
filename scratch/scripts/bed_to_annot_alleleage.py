import gzip
import numpy as np
from scipy.special import erfinv


def get_allele_age_dict():
    out = {}
    with open('../baselineLD_bed/alleleage.bed', 'r') as f:
        for line in f.readlines():
            split_line = [a.strip() for a in line.split('\t')]
            out[(int(split_line[0].split('chr')[1]), int(split_line[2]))] = float(split_line[3])
    return out


def maf_bin(bin_num):
    vars = []
    for CHR in range(1, 22):
        with open(f'../g1000_plink_eur/1000G.EUR.QC.{CHR}.bim', 'r') as f:
            for line in f.readlines():
                split_line = [a.strip() for a in line.split('\t')]
                vars.append((int(split_line[0]), int(split_line[3])))
    maf_bin = []
    for CHR in range(1, 22):
        with gzip.open(f'../baseline_annot/MAFbin{bin_num}.{CHR}.annot.gz', 'r') as f:
            _ = f.readline()  # useless header row
            for line in f.readlines():
                maf_bin.append(line.strip() == b'1')
    out = []
    for (varId, in_bin) in zip(vars, maf_bin):
        if in_bin:
            out.append(varId)
    return out


def main():
    out = get_allele_age_dict()
    maf_vars = maf_bin(1)
    # For bin 2 the effective sample size is 508675?
    # For bin 3 the effective sample size is 532360?
    # For bin 4 the effective sample size is 541433?
    ages = {}
    for varId in maf_vars:
        if varId in out:
            if out[varId] not in ages:
                ages[out[varId]] = []
            ages[out[varId]].append(varId)
        else:
            print(varId)
            print(xxx)
    sorted_keys = sorted(ages.keys())
    var_with_index = []
    for k in sorted_keys:
        grouped_vars = ages[k]
        next_i = len(var_with_index) + (len(grouped_vars) + 1) / 2
        for v in grouped_vars:
            var_with_index.append((next_i, v))
    test = [np.sqrt(2) * erfinv(2 * idx[0] / len(var_with_index) - 1) for idx in var_with_index]





if __name__ == '__main__':
    main()
