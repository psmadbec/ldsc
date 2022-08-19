import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--phenotype', default=None, type=str, help="Input phenotype.")
parser.add_argument('--ancestry', default='EUR', type=str,
                    help="Ancestry, should be three letter version (e.g. EUR) and will be made upper.")

def get_snp_map():
    snp_map = {}
    with open('../phenotype_files/snp.csv', 'r') as f:
        header = f.readline()
        for full_row in f.readlines():
            row = full_row.split('\t')
            snp_map[row[1].strip()] = row[0].strip()
    return snp_map

def stream_to_txt(args, snp_map):
    with open(f'../phenotype_files/{args.phenotype}_{args.ancestry}.json', 'r') as f_in:
        with open(f'../phenotype_files/{args.phenotype}_{args.ancestry}.txt', 'w') as f_out:
            line_template = '{}\t{}\t{}\t{}\t{}\n'
            f_out.write(line_template.format('MarkerName', 'Allele1', 'Allele2', 'p', 'N'))
            for json_string in f_in.readlines():
                line = json.loads(json_string)
                if 'varId' in line and line['varId'] in snp_map:
                    line_string = line_template.format(
                        snp_map[line['varId']],
                        line['reference'].lower(),
                        line['alt'].lower(),
                        line['pValue'],
                        line['n']
                    )
                    f_out.write(line_string)

def make_file(args):
    snp_map = get_snp_map()
    print(f"Created SNP map ({len(snp_map)} variants)")
    stream_to_txt(args, snp_map)

if __name__ == '__main__':
    make_file(parser.parse_args())
