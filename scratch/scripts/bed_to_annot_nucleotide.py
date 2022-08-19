import gzip


def get_1000g_vector(CHR):
    out = []
    with open(f'../g1000_plink_eur/1000G.EUR.QC.{CHR}.bim', 'r') as f:
        for line in f.readlines():
            split_line = line.split('\t')
            out.append(int(split_line[3]))
    return out


def get_nucleotide_diversity(g1000):
    out = []
    i = 0
    j = 0
    for k, bp in enumerate(g1000):
        while g1000[i] <= bp - 10000:
            i += 1
        while j < len(g1000) and g1000[j] < bp + 10000:
            j += 1
        distance = (10000 if i > 0 else bp - g1000[0]) + (10000 if j < len(g1000) else g1000[-1] - bp)
        out.append(round((j - i) / distance * 1000, 6))
    return out


def make_annot_files(CHR, nucleotide_diversity):
    print(f'Chromosome {CHR}')
    with gzip.open(f'../baseline_annot/Nucleotide_Diversity_10kb.{CHR}.annot.gz', 'w') as f:
        f.write(b'ANNOT\n')
        for nd in nucleotide_diversity:
            f.write(str(nd).encode() + b'\n')


def main():
    for CHR in range(1, 23):
        g1000 = get_1000g_vector(CHR)
        nucleotide_diversity = get_nucleotide_diversity(g1000)
        make_annot_files(CHR, nucleotide_diversity)


if __name__ == '__main__':
    main()
