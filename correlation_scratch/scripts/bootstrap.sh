#!/bin/bash

## Download hapmap3 snps (full)
mkdir ../snps
curl --location https://data.broadinstitute.org/alkesgroup/LDSCORE/w_hm3.snplist.bz2 > w_hm3.snplist.bz2
bunzip2 w_hm3.snplist.bz2
mv w_hm3.snplist ../snps/

# Download all ancestry specific ldscores into the proper location
for ANCESTRY in AFR AMR EAS EUR SAS
do
  mkdir -p ../ldscore/$ANCESTRY
  aws s3 cp s3://dig-analysis-data/scripts/ldscore/data/ldscore_$ANCESTRY.zip ../ldscore/$ANCESTRY/
  unzip ../ldscore/$ANCESTRY/ldscore_$ANCESTRY.zip -d ../ldscore/$ANCESTRY/
  rm ../ldscore/$ANCESTRY/ldscore_$ANCESTRY.zip
done
