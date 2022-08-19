#!/bin/bash

# file name and chromosome
[ -z "$1" ] && { echo "Need to pass in file name"; exit 1; }
fname=$1

for chr in {1..22}
do
  ./make_annot_l2.sh $fname $chr
done
