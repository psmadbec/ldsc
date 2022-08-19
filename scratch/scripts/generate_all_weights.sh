#!/bin/bash

for chr in {1..22}
do
  ./generate_weights.sh $chr
done