import argparse
import json
import subprocess


ancestry_map = {
    'AA': 'AFR',
    'AF': 'AFR',
    'HS': 'AMR',
    'EA': 'EAS',
    'EU': 'EUR',
    'SA': 'SAS'
}


def get_single_json_file(phenotype, ancestry):
    subprocess.check_call(['./fetch_phenotype_ancestry_file.sh', phenotype, ancestry])


def get_snp_map():
    snp_map = {}
    with open('../local_files/snp.csv', 'r') as f:
        header = f.readline()
        for full_row in f.readlines():
            row = full_row.split('\t')
            snp_map[row[1].strip()] = row[0].strip()
    return snp_map


def stream_to_txt(phenotype, ancestry, snp_map):
    with open(f'../local_files/{phenotype}_{ancestry}.json', 'r') as f_in:
        with open(f'../local_files/{phenotype}_{ancestry}.txt', 'w') as f_out:
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


def create_sumstats(phenotype, ancestry):
    subprocess.check_call([
        'python', '../../munge_sumstats.py',
        '--sumstats', f'../local_files/{phenotype}_{ancestry}.txt',
        '--out', f'../local_files/{phenotype}_{ancestry}',
        '--merge-alleles', '../snps/w_hm3.snplist',
        '--a1-inc'
    ])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--phenotype', default=None, required=True, type=str,
                        help="Input phenotype.")
    parser.add_argument('--ancestry', default=None, required=True, type=str,
                        help="Ancestry, should be two letter version (e.g. EU) and will be made upper.")
    args = parser.parse_args()
    phenotype = args.phenotype
    ancestry = args.ancestry.upper()
    if ancestry not in ancestry_map:
        raise Exception(f'Invalid ancestry ({ancestry}), must be one of {", ".join(ancestry_map.keys())}')

    get_single_json_file(phenotype, ancestry)
    snp_map = get_snp_map()
    print(f"Created SNP map ({len(snp_map)} variants)")
    stream_to_txt(phenotype, ancestry, snp_map)
    create_sumstats(phenotype, ancestry)
    # upload_and_remove_files(phenotype, ancestry)


if __name__ == '__main__':
    main()
