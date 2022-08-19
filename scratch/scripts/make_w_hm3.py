
def get_snp_map():
    snp_map = {}
    for CHR in range(1, 23):
        with open(f'../g1000_plink_eur/1000G.EUR.QC.{CHR}.bim', 'r') as f:
            for full_row in f.readlines():
                row = full_row.split('\t')
                snp_map[row[1].strip()] = (row[4].strip(), row[5].strip())
    return snp_map

def stream_to_txt(snp_map):
    with open(f'../baseline_v2.2_snps/w_hm3.snplist', 'w') as f_out:
        line_template = '{}\t{}\t{}\n'
        f_out.write(line_template.format('SNP', 'A1', 'A2'))
        for CHR in range(1, 23):
            with open(f'../baseline_v2.2_snps/hm.{CHR}.snp', 'r') as f_in:
                c_in = 0
                c_out = 0
                for snp in f_in.readlines():
                    if snp.strip() in snp_map:
                        row = snp_map[snp.strip()]
                        line_string = line_template.format(
                            snp.strip(),
                            row[0].upper(),
                            row[1].upper()
                        )
                        f_out.write(line_string)
                        c_in += 1
                    else:
                        c_out += 1
            print(f'For chromosome {CHR} {c_in}/{c_out + c_in} variants converted')

def make_file():
    snp_map = get_snp_map()
    print(f"Created SNP map ({len(snp_map)} variants)")
    stream_to_txt(snp_map)

if __name__ == '__main__':
    make_file()
