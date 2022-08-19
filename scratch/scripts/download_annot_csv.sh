#!/bin/bash

# file name
[ -z "$1" ] && { echo "Need to pass in file name"; exit 1; }
fname=$1

aws s3 cp s3://dig-analysis-data/out/ldsc/regions/gregor_backup/merged/$fname/$fname.csv ../annot/
