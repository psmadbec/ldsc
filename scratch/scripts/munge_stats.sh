#!/bin/bash

# phenotype (currently only EUR)
[ -z "$1" ] && { echo "Need to pass in phenotype"; exit 1; }
phenotype=$1

python ../../munge_sumstats.py --sumstats ../phenotype_files/$phenotype'_'EUR.txt\
  --merge-alleles ../baseline_v2.2_snps/w_hm3.snplist\
  --out ../phenotype_files/$phenotype\
  --a1-inc