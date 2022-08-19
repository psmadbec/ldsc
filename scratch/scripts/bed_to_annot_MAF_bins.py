import gzip


def get_frq_map():
    out = {}
    for CHR in range(1, 23):
        with open(f'../frq/chr.{CHR}.frq') as f:
            _ = f.readline()  # has header, but not used
            for line in f.readlines():
                split_line = line.split('\t')
                out[split_line[1]] = float(split_line[4].strip())
    return out


def bin_frq(frq_map):
    sorted_frq = [a for a in sorted(frq_map.values()) if a >= 0.05]
    bins = [0.0] + [sorted_frq[len(sorted_frq) // 10 * i] for i in range(1, 10)]
    return bins


def create_bin_map(frq_map, bins):
    out = {}
    for varID, frq in frq_map.items():
        if frq >= 0.05:
            out[varID] = 10 - len([b for b in bins if b >= frq])
        else:
            out[varID] = 0
    return out


def make_annot_files(CHR, bin_map):
    for i in range(1, 11):
        print(f'Chromosome {CHR} and bin {i}')
        with gzip.open(f'../baseline_annot/MAFbin{i}.{CHR}.annot.gz', 'w') as f:
            f.write(b'ANNOT\n')
            with open(f'../frq/chr.{CHR}.frq', 'r') as frq_f:
                _ = frq_f.readline()  # has header, but not used
                for line in frq_f.readlines():
                    split_line = line.split('\t')
                    b = bin_map[split_line[1].strip()]
                    f.write(b'1\n' if i == b else b'0\n')


def main():
    frq_map = get_frq_map()
    print(len(frq_map))
    bins = bin_frq(frq_map)
    print(bins)
    bin_map = create_bin_map(frq_map, bins)
    for CHR in range(1, 23):
        make_annot_files(CHR, bin_map)


if __name__ == '__main__':
    main()
