#!/bin/bash

# file name
[ -z "$1" ] && { echo "Need to pass in file name"; exit 1; }
fname=$1

./download_annot_csv.sh $fname
./csv_to_bed.sh $fname
./make_all_annot.sh $fname
