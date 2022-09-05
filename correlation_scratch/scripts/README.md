#Steps to run from scratch
1) Run bootstrap script to download LD Scores based on current G1000 files
   NOTE: If you want to update g1000 files use: s3://dig-analysis-data/scripts/generate_g1000.zip (and then update LD scores)
   NOTE: If you want to update LD scores use: s3://dig-analysis-data/scripts/ldscore/generate_ld_scores.zip
2) We will not be generating weights at this point, but if we were to the following would be used:
   For each chromosome and ancestry run (this is customized to the regression):
   `python ldsc.py\
      --bfile ../g1000/EUR/chr.1\
      --l2\
      --ld-wind-cm 1\
      --out ../weights/EUR/chr.1\
      --extract regression.snplist`
3) Download the snp file for mapping `./fetch_snp_file.sh`
4) Generate all sumstats for phenotype and ancestries:
   `python make_sumstats.py --phenotype=<phenotype> --ancestry=<ancestry>`
5) Run ldscore genetic correlation, here using weights that are identical to the ldscores:
   `python ../../ldsc.py \
      --rg ../local_files/BMI_EU.sumstats.gz,../local_files/T2D_EU.sumstats.gz \
      --ref-ld-chr ../local_files/ldscores/EUR/ \
      --w-ld-chr ../local_files/ldscores/EUR/ \
      --out ../local_files/BMI_T2D_EU`
