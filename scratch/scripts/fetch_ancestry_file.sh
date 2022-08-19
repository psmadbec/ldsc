#!/bin/bash

# phenotype (currently only EUR)
[ -z "$1" ] && { echo "Need to pass in phenotype"; exit 1; }
phenotype=$1

aws s3 cp s3://dig-analysis-data/out/metaanalysis/ancestry-specific/$phenotype/ancestry=EU/ ./ --recursive --exclude="_SUCCESS"
rm -f $phenotype'_'EUR.json
cat part-*.json >> $phenotype'_'EUR.json
mv $phenotype'_'EUR.json ../phenotype_files/$phenotype'_'EUR.json
rm *.json
