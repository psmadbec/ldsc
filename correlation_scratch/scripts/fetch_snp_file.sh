#!/bin/bash

aws s3 cp s3://dig-analysis-data/out/varianteffect/snp/ ../local_files/ --recursive --exclude="_SUCCESS"
rm -f ../local_files/snp.csv
head -n 1 ../local_files/part-*.csv | uniq >> ../local_files/snp.csv
tail -n +2 ../local_files/part-*.csv >> ../local_files/snp.csv
rm ../local_files/part-*.csv
