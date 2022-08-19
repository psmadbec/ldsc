#!/bin/bash

aws s3 cp s3://dig-analysis-data/out/varianteffect/snp/ ./ --recursive --exclude="_SUCCESS"
rm -f snp.csv
head -n 1 part-*.csv | uniq >> snp.csv
tail -n +2 part-*.csv >> snp.csv
mv snp.csv ../phenotype_files/snp.csv
rm *.csv
