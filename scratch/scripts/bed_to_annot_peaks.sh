#!/bin/bash

studies=('DHS_peaks_Trynka'
         'H3K4me1_peaks_Trynka'
         'H3K4me3_peaks_Trynka'
         'H3K9ac_peaks_Trynka')

for study in ${studies[@]}
do
  for CHR in {1..22}
  do
    echo $study $CHR
    python ../../make_annot.py\
      --bed-file ../baselineLD_bed/$study.bed\
      --bimfile ../g1000_plink_eur/1000G.EUR.QC.$CHR.bim\
      --annot ../baseline_annot/$study.$CHR.annot.gz
  done
done