#!/bin/bash

# file name
[ -z "$1" ] && { echo "Need to pass in file name"; exit 1; }
fname=$1

cat ../annot/$fname.csv | awk 'BEGIN { OFS = "\t"}{$1="chr"$1; print $0}' > ../annot/$fname.bed
