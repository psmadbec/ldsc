#!/bin/bash

mkdir ../annot
mkdir ../baseline_v2.2_snps
mkdir ../baselineLD
mkdir ../baseline_annot
mkdir ../frq
mkdir ../output
mkdir ../phenotype_files
mkdir ../weights
mkdir ../genetic_map

curl https://alkesgroup.broadinstitute.org/LDSCORE/1000G_Phase3_baselineLD_v2.2_ldscores.tgz > baselineLD.tgz
tar -xf baselineLD.tgz -C ../baselineLD/
rm baselineLD.tgz

curl https://alkesgroup.broadinstitute.org/LDSCORE/1000G_Phase3_plinkfiles.tgz > g1000_plink_eur.tgz
tar -xf g1000_plink_eur.tgz
mv 1000G_EUR_Phase3_plink g1000_plink_eur

curl https://mathgen.stats.ox.ac.uk/impute/1000GP_Phase3.tgz > 1000GP_Phase3.tgz
gunzip 1000GP_Phase3.tgz
tar -xf 1000GP_Phase3.tar
mv 1000GP_Phase3/genetic_map* ./genetic_map
rm 1000GP_Phase3.tar
rm -r 1000GP_Phase3

# Actually just download the bed files and then the different ancestry bed/bim/fam as well
# Rename the Transcription_Hoffman to Transcr_Hoffman
# mv Ancient* bed files to _Original versions, and then remove lines: awk 'BEGIN {OFS="\t"} {if($2!=$3)print $0}'
# For those we'll want to investigate it all as well

