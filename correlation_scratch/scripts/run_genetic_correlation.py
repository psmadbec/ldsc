import argparse
import subprocess

ancestry_map = {
    'AA': 'AFR',
    'AF': 'AFR',
    'HS': 'AMR',
    'EA': 'EAS',
    'EU': 'EUR',
    'SA': 'SAS'
}


def run(phenotypes, ancestry):
    file_list = ','.join([f'../local_files/{phenotype}_{ancestry}.sumstats.gz' for phenotype in phenotypes])
    subprocess.check_call([
        'python', '../../ldsc.py',
        '--rg', file_list,
        '--ref-ld-chr', f'../ldscore/{ancestry_map[ancestry]}/chr@',
        '--w-ld-chr', f'../ldscore/{ancestry_map[ancestry]}/chr@',
        '--out', f'../local_files/{phenotypes[0]}_{ancestry}'
    ])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--phenotypes', default=None, required=True, type=str,
                        help="Input phenotypes.")
    parser.add_argument('--ancestry', default=None, required=True, type=str,
                        help="Ancestry, should be two letter version (e.g. EU) and will be made upper.")
    args = parser.parse_args()
    phenotypes = args.phenotypes.split(',')
    ancestry = args.ancestry.upper()
    if ancestry not in ancestry_map:
        raise Exception(f'Invalid ancestry ({ancestry}), must be one of {", ".join(ancestry_map.keys())}')

    run(phenotypes, ancestry)


if __name__ == '__main__':
    main()
