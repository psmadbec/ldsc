from Bio import SeqIO
import gzip
import re


class FaFinder:
    def __init__(self, data_path):
        self.data_path = data_path
        fasta_sequences = SeqIO.parse(open(f'{self.data_path}/Homo_sapiens.GRCh37.75.dna.primary_assembly.fa'), 'fasta')
        self.fa_dict = {fasta.id: str(fasta.seq) for fasta in fasta_sequences}

    def get_actual_ref(self, chromosome, position, ref_length):
        if chromosome == 'XY':  # 'XY' is a valid chromosome, but not in reference. Use 'X' instead
            return self.fa_dict['X'][int(position) - 1:int(position) - 1 + ref_length]
        if chromosome in self.fa_dict:
            return self.fa_dict[chromosome][int(position) - 1:int(position) - 1 + ref_length]


def get_1000g_vector(CHR):
    out = []
    with open(f'../g1000_plink_eur/1000G.EUR.QC.{CHR}.bim', 'r') as f:
        for line in f.readlines():
            split_line = line.split('\t')
            out.append(int(split_line[3]))
    return out


def get_CpG_and_n_for_range(fa_finder, CHR, start, number):
    ref = fa_finder.get_actual_ref(str(CHR), start, number + 1)
    return len(re.findall('CG', ref)), len(re.findall('N', ref[:-1]))


def get_CpG_content(fa_finder, CHR, g1000_data):
    print(f'Calculating for chromosome {CHR}')
    window = 50000
    out = []
    start = max(g1000_data[0] + 1, g1000_data[0] - window)
    end = min(g1000_data[-1], g1000_data[0] + window + 1)
    CpG, n = get_CpG_and_n_for_range(fa_finder, CHR, start, end - start)
    for i in range(len(g1000_data)):
        new_start = max(g1000_data[0] + 1, g1000_data[i] - window)
        new_end = min(g1000_data[-1], g1000_data[i] + window + 1)
        left_CpG, left_n = get_CpG_and_n_for_range(fa_finder, CHR, start, new_start - start)
        right_CpG, right_n = get_CpG_and_n_for_range(fa_finder, CHR, end, new_end - end)
        start = new_start
        end = new_end
        CpG = CpG + right_CpG - left_CpG
        n = n + right_n - left_n
        out.append(round(CpG / (end - start - n), 5))
    return out


def make_annot_files(CHR, CpG_content):
    print(f'Saving chromosome {CHR}')
    with gzip.open(f'../baseline_annot/CpG_Content_50kb.{CHR}.annot.gz', 'w') as f:
        f.write(b'ANNOT\n')
        for CpG in CpG_content:
            f.write(str(CpG).encode() + b'\n')


def main():
    fa_finder = FaFinder('../fasta_files')
    for CHR in range(1, 23):
        g1000 = get_1000g_vector(CHR)
        CpG_content = get_CpG_content(fa_finder, CHR, g1000)
        make_annot_files(CHR, CpG_content)


if __name__ == '__main__':
    main()
