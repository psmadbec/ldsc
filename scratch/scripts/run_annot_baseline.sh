#!/bin/bash

# phenotype and file name
[ -z "$1" ] && { echo "Need to pass in phenotype"; exit 1; }
[ -z "$2" ] && { echo "Need to pass in file name"; exit 1; }
phenotype=$1
fname=$2

python ../../ldsc.py\
	--h2 ../phenotype_files/$phenotype.sumstats.gz\
	--ref-ld-chr ../annot/$fname.,../baselineLD/baselineLD.\
	--w-ld-chr ../weights/weights.\
	--overlap-annot\
	--frqfile-chr ../frq/chr.\
	--out ../output/$phenotype'_'$fname