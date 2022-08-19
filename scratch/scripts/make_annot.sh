#!/bin/bash

# file name and chromosome
[ -z "$1" ] && { echo "Need to pass in file name"; exit 1; }
[ -z "$2" ] && { echo "Need to pass in chromosome"; exit 1; }
fname=$1
chr=$2

python ../../make_annot.py\
    --bed-file ../annot/$fname.bed\
    --bimfile ../g1000_plink_eur/1000G.EUR.QC.$chr.bim\
    --annot ../annot/$fname.$chr.annot.gz
