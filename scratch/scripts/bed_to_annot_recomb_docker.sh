#!/bin/bash

# NOTE: Run the docker with the volume attached
# docker run -v /Users/psmadbec/Code/test_data/plink-docker:/app/ -it c6e /bin/bash

for CHR in {1..22}
do
  cat ../app/g1000_plink_eur/1000G.EUR.QC.$CHR.bim | awk 'BEGIN {OFS="\t"}{L=$4-10000;if(L<0)L=0;print $1,$2,$3,L,$5,$6}' > chr_left.bim
  cat ../app/g1000_plink_eur/1000G.EUR.QC.$CHR.bim | awk 'BEGIN {OFS="\t"}{print $1,$2,$3,$4,$5,$6}' > chr_middle.bim
  cat ../app/g1000_plink_eur/1000G.EUR.QC.$CHR.bim | awk 'BEGIN {OFS="\t"}{print $1,$2,$3,$4+10000,$5,$6}' > chr_right.bim
  cp ../app/g1000_plink_eur/1000G.EUR.QC.$CHR.bed chr_left.bed
  cp ../app/g1000_plink_eur/1000G.EUR.QC.$CHR.bed chr_middle.bed
  cp ../app/g1000_plink_eur/1000G.EUR.QC.$CHR.bed chr_right.bed
  cp ../app/g1000_plink_eur/1000G.EUR.QC.$CHR.fam chr_left.fam
  cp ../app/g1000_plink_eur/1000G.EUR.QC.$CHR.fam chr_middle.fam
  cp ../app/g1000_plink_eur/1000G.EUR.QC.$CHR.fam chr_right.fam
  ./plink --make-bed --bfile chr_left --out chr_left_out --cm-map ../app/genetic_map/genetic_map_chr$CHR"_combined_b37.txt" $CHR
  ./plink --make-bed --bfile chr_middle --out chr_middle_out --cm-map ../app/genetic_map/genetic_map_chr$CHR"_combined_b37.txt" $CHR
  ./plink --make-bed --bfile chr_right --out chr_right_out --cm-map ../app/genetic_map/genetic_map_chr$CHR"_combined_b37.txt" $CHR

  minCM=$(head -n 1 chr_middle_out.bim | awk '{print $3}')
  maxCM=$(tail -n 1 chr_middle_out.bim | awk '{print $3}')
  minBP=$(head -n 1 chr_middle_out.bim | awk '{print $4}')
  maxBP=$(tail -n 1 chr_middle_out.bim | awk '{print $4}')

  cat chr_left_out.bim | awk -v minCM=$minCM -v minBP=$minBP 'BEGIN {OFS="\t"}{if($4<minBP){$4=minBP;$3=minCM};print $0}' > chr_left_fin.bim
  cat chr_right_out.bim | awk -v maxCM=$maxCM -v maxBP=$maxBP 'BEGIN {OFS="\t"}{if($4>maxBP){$4=maxBP;$3=maxCM};print $0}' > chr_right_fin.bim

  echo "ANNOT" | gzip > ../app/baseline_annot/Recomb_Rate_10kb.$CHR.annot.gz
  paste <(cat chr_left_fin.bim | awk '{print $3, $4}') <(cat chr_right_fin.bim | awk '{print $3, $4}') |
  awk '{print ($3 - $1) / ($4 - $2) * 1000000}' |
  gzip >> ../app/baseline_annot/Recomb_Rate_10kb.$CHR.annot.gz
done
