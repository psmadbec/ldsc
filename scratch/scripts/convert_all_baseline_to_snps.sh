#!/bin/bash

for i in {1..22}
do
  echo "Converting chr $i"
  ./convert_baseline_to_snps.sh $i
done