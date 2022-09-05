#!/bin/bash

[ -z "$1" ] && { echo "Need to pass in phenotype"; exit 1; }
[ -z "$2" ] && { echo "Need to pass in ancestry"; exit 1; }
PHENOTYPE=$1
ANCESTRY=$2

mkdir -p ../local_files
aws s3 cp s3://dig-analysis-data/out/metaanalysis/ancestry-specific/$PHENOTYPE/ancestry=$ANCESTRY/ ../local_files/ --recursive --exclude="_SUCCESS"
rm -f ../local_files/$PHENOTYPE'_'$ANCESTRY.json
cat ../local_files/part-*.json >> ../local_files/$PHENOTYPE'_'$ANCESTRY.json
rm ../local_files/part-*.json
