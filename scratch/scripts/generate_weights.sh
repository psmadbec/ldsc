#!/bin/bash

# chromosome
[ -z "$1" ] && { echo "Need to pass in chromosome"; exit 1; }
chr=$1

python ../../ldsc.py\
  --l2\
  --bfile ../g1000_plink_eur/1000G.EUR.QC.$chr\
  --ld-wind-cm 1\
  --out ../weights/weights.$chr\
  --extract ../baseline_v2.2_snps/hm.$chr.snp
