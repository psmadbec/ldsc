import gzip


def get_background_data():
    out = {}
    with open(f'../baselineLD_bed/Backgrd_Selection_Stat.bed', 'r') as f:
        for line in f.readlines():
            split_line = line.split('\t')
            CHR = int(split_line[0].replace('chr', ''))
            if CHR not in out:
                out[CHR] = []
            out[CHR].append((int(split_line[1]), int(split_line[2]), float(split_line[3])))
    return out


def get_1000g_dict():
    out = {}
    for CHR in range(1, 23):
        out[CHR] = []
        with open(f'../g1000_plink_eur/1000G.EUR.QC.{CHR}.bim', 'r') as f:
            for line in f.readlines():
                split_line = line.split('\t')
                out[CHR].append(int(split_line[3]))
    return out


def get_median_value(g1000, all_background_data):
    out = []
    for CHR in range(1, 23):
        i = 0
        background_data = all_background_data[CHR]
        for bp in g1000[CHR]:
            while i < len(background_data) and bp > background_data[i][1]:
                i += 1
            if i < len(background_data) and background_data[i][0] < bp <= background_data[i][1]:
                out.append(background_data[i][2])
    out.sort()
    return out[len(out) // 2]


def combine_g1000_background(g1000, background_data, median_value):
    out = []
    i = 0
    for bp in g1000:
        while i < len(background_data) and bp > background_data[i][1]:
            i += 1
        if i < len(background_data) and background_data[i][0] < bp <= background_data[i][1]:
            out.append(background_data[i][2])
        else:
            out.append(median_value)
    return out


def make_annot_files(CHR, combined_data):
    print(f'Chromosome {CHR}')
    with gzip.open(f'../baseline_annot/Backgrd_Selection_Stat.{CHR}.annot.gz', 'w') as f:
        f.write(b'ANNOT\n')
        for value in combined_data:
            f.write(str(value).encode() + b'\n')


def main():
    background_data = get_background_data()
    g1000 = get_1000g_dict()
    median_value = get_median_value(g1000, background_data)
    print(f'median value = {median_value}')
    for CHR in range(1, 23):
        combined_data = combine_g1000_background(g1000[CHR], background_data[CHR], median_value)
        make_annot_files(CHR, combined_data)


if __name__ == '__main__':
    main()