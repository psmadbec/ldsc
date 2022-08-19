import numpy as np
from pandas_plink import read_plink

f_in = '../g1000_plink_eur/1000G.EUR.QC.{}.bed'
f_out = '../frq/chr.{}.frq'

def gen_chromosome(chromosome):
    (bim, fam, bed) = read_plink(f_in.format(chromosome), verbose=False)
    maf = 1 - np.mean(bed.compute(), axis=1) / 2
    line_template = '{}\t{}\t{}\t{}\t{}\t{}\n'
    with open(f_out.format(chromosome), 'w') as f:
        f.write(line_template.format('CHR', 'SNP', 'A1', 'A2', 'MAF', 'NCHROBS'))
        for row in bim.iterrows():
            row_dict = row[1]
            f.write(line_template.format(
                row_dict.chrom,
                row_dict.snp,
                row_dict.a0,
                row_dict.a1,
                "{:.5f}".format(maf[row[0]]),
                fam.shape[0] * 2
            ))

def main():
    for chromosome in range(1, 23):
        print(f'Generating frequencies for chromosome {chromosome}')
        gen_chromosome(chromosome)

if __name__ == '__main__':
    main()