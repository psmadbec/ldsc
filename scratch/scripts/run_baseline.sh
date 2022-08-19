#!/bin/bash

# phenotype
[ -z "$1" ] && { echo "Need to pass in phenotype"; exit 1; }
phenotype=$1

python ../../ldsc.py\
	--h2 ../phenotype_files/$phenotype.sumstats.gz\
	--ref-ld-chr ../baselineLD/baselineLD.\
	--w-ld-chr ../weights/weights.\
	--overlap-annot\
	--frqfile-chr ../frq/chr.\
	--out ../output/$phenotype'_'baseline
