#!/bin/bash

#flanking_studies=('BivFlnk'
#                   'Coding_UCSC'
#                   'Conserved_LindbladToh'
#                   'Conserved_Mammal_phastCons46way'
#                   'Conserved_Primate_phastCons46way'
#                   'Conserved_Vertebrate_phastCons46way'
#                   'CTCF_Hoffman'
#                   'DGF_ENCODE'
#                   'DHS_Trynka'
#                   'Enhancer_Andersson'
#                   'Enhancer_Hoffman'
#                   'FetalDHS_Trynka'
#                   'H3K27ac_Hnisz'
#                   'H3K27ac_PGC2'
#                   'H3K4me1_Trynka'
#                   'H3K4me3_Trynka'
#                   'H3K9ac_Trynka'
#                   'Human_Enhancer_Villar'
#                   'Human_Promoter_Villar'
#                   'Human_Promoter_Villar_ExAC'
#                   'Intron_UCSC'
#                   'Promoter_UCSC'
#                   'PromoterFlanking_Hoffman'
#                   'Repressed_Hoffman'
#                   'SuperEnhancer_Hnisz'
#                   'TFBS_ENCODE'
#                   'Transcr_Hoffman'
#                   'TSS_Hoffman'
#                   'UTR_3_UCSC'
#                   'UTR_5_UCSC'
#                   'WeakEnhancer_Hoffman',
#                   'Ancient_Sequence_Age_Human_Promoter'
#                   'Ancient_Sequence_Age_Human_Enhancer')

for study in ${flanking_studies[@]}
do
  for CHR in {1..22}
  do
    echo $study $CHR
    python ../../make_annot.py\
      --bed-file ../baselineLD_bed/$study.bed\
      --bimfile ../g1000_plink_eur/1000G.EUR.QC.$CHR.bim\
      --annot ../baseline_annot/$study.$CHR.annot.gz
    python ../../make_annot.py\
      --bed-file ../baselineLD_bed/$study.extend.500.bed\
      --bimfile ../g1000_plink_eur/1000G.EUR.QC.$CHR.bim\
      --annot ../baseline_annot/$study.extend.500.$CHR.annot.gz
    paste <(gzcat ../baseline_annot/$study.$CHR.annot.gz) <(gzcat ../baseline_annot/$study.extend.500.$CHR.annot.gz) |
      awk '{i=0;if($1 == 0 && $2 == 1) i=1; if(NR==1) i="ANNOT";print i}' |
      gzip > ../baseline_annot/$study.flanking.500.$CHR.annot.gz
    rm ../baseline_annot/$study.extend.500.$CHR.annot.gz
  done
done