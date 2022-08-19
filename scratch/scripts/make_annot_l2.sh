#!/bin/bash

# file name and chromosome
[ -z "$1" ] && { echo "Need to pass in file name"; exit 1; }
[ -z "$2" ] && { echo "Need to pass in chromosome"; exit 1; }
fname=$1
chr=$2

python ../../ldsc.py\
    --l2\
    --bfile ../g1000_plink_eur/1000G.EUR.QC.$chr\
    --ld-wind-cm 1\
    --annot ../annot/$fname.$chr.annot.gz\
    --thin-annot\
    --out ../annot/$fname.$chr\
    --print-snps ../baseline_v2.2_snps/hm.$chr.snp
