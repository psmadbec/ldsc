import gzip
from scipy.stats import norm


def get_ASMC_dict():
    out = {}
    with open('../baselineLD_bed/ASMC_avg.180813.bed', 'r') as f:
        for line in f.readlines():
            split_line = [a.strip() for a in line.split('\t')]
            out[(int(split_line[0]), int(split_line[2]))] = float(split_line[3])
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

# NOTE: This is a bit odd, but unlike normal quantilization they seem to have split overlapping values and just assigned
# them in sorted chr:pos order. This is wrong, but I'm leaving it for now as a check.
# c is an adjustment to rank, BLOM dictates 3/8, but since no value actually works I'm leaving it 0 for now
c = 0

def get_var_dict(bin, ASMC):
    maf_vars = maf_bin_2(bin)
    ASMC_to_var_ids = {}
    for varId in maf_vars:
        if varId in ASMC:
            asmc = ASMC[varId]
            if asmc not in ASMC_to_var_ids:
                ASMC_to_var_ids[asmc] = []
            ASMC_to_var_ids[asmc].append(varId)
    total = sum([len(v) for k, v in ASMC_to_var_ids.items()])

    var_dict = {}
    sorted_asmc = sorted(ASMC_to_var_ids)
    variants_less = 0
    for asmc in sorted_asmc:
        varIds = ASMC_to_var_ids[asmc]
        ranks = [variants_less + 1 + i for i in range(len(varIds))]
        maf_asmc = [norm.ppf((r - c + 1) / (total - 2 * c + 1)) for r in ranks]
        variants_less += len(varIds)
        for i, varId in enumerate(sorted(varIds)):
            var_dict[varId] = maf_asmc[i]
    return var_dict


def make_annot_files(CHR, var_dict):
    print(f'Writing Chromosome {CHR}')
    with gzip.open(f'../baseline_annot/MAF_Adj_ASMC.{CHR}.annot.gz', 'w') as f_out:
        f_out.write(b'ANNOT\n')
        with open(f'../g1000_plink_eur/1000G.EUR.QC.{CHR}.bim', 'r') as f_in:
            for line in f_in.readlines():
                split_line = [a.strip() for a in line.split('\t')]
                var_id = (int(split_line[0]), int(split_line[3]))
                f_out.write(str(var_dict[var_id]).encode() + b'\n' if var_id in var_dict else b'0\n')


def main():
    asmc_dict = get_ASMC_dict()
    var_dict = {}
    for bin in range(1, 11):
        var_dict.update(get_var_dict(bin, asmc_dict))
    for CHR in range(1, 23):
        make_annot_files(CHR, var_dict)


if __name__ == '__main__':
    main()
