import gzip

study_inputs = [
    'Human_Enhancer_Villar_Species_Enhancer_Count'
]
study_outputs = [
    'Human_Enhancer_Villar_Species_Enhancer_Count'
]


def get_output_map(study):
    out = {}
    with open(f'../baselineLD_bed/{study}.bed', 'r') as f:
        for line in f.readlines():
            split_line = line.split('\t')
            for i in range(int(split_line[1]) + 1, int(split_line[2]) + 1):
                out[(split_line[0].split('chr')[1], str(i))] = split_line[3]
    return out


def get_1000g_vector(CHR):
    out = []
    with open(f'../g1000_plink_eur/1000G.EUR.QC.{CHR}.bim', 'r') as f:
        for line in f.readlines():
            split_line = line.split('\t')
            out.append((split_line[0], split_line[3]))
    return out


def create_outputs():
    for i, study_in in enumerate(study_inputs):
        output_map = get_output_map(study_in)
        print(len(output_map))
        for CHR in range(1, 23):
            print(study_in, CHR)
            chr_positions = get_1000g_vector(CHR)
            with gzip.open(f'../baseline_annot/{study_outputs[i]}.{CHR}.annot.gz', 'w') as f:
                f.write(b'ANNOT\n')
                for chr_position in chr_positions:
                    if chr_position in output_map:
                        f.write(str.encode(output_map[chr_position]))
                    else:
                        f.write(b'0\n')


def main():
    create_outputs()


if __name__ == '__main__':
    main()