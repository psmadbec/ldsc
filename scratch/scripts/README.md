#Steps to run from scratch
1) Download baseline model from https://alkesgroup.broadinstitute.org/LDSCORE/1000G_Phase3_baselineLD_v2.2_ldscores.tgz and extract to `baselineLD` directory
2) Download G1000 EUR Dataset from https://alkesgroup.broadinstitute.org/LDSCORE/1000G_Phase3_plinkfiles.tgz and extract to `g1000_plink_eur` directory
3) `./convert_all_baseline_to_snps.sh`
4) `python make_w_hm3.py`
NOTE: We should use the w_hm3.snplist from here:
   wget https://data.broadinstitute.org/alkesgroup/LDSCORE/w_hm3.snplist.bz2
   bunzip2 w_hm3.snplist.bz2
This would negate the need for steps 3 and 4 above
5) `./download_and_created_bed.sh [fname]`
6) `./make_all_annot_l2.sh [fname]`
7) `./fetch_ancestry_file.sh [phenotype]`
8) `./fetch_snp_file.sh`
9) `python make_substats_input.py --phenotype=[phenotype]`
10) `./munge_stats.sh [phenotype]`
11) `./generate_all_weights.sh`
12) `python generate_frequencies.py`
13) `./run_annot_baseline.sh [phenotype] [fname]`

#Files
## SNP file (directory: baseline_v2.2_snps)
###`convert_all_baseline_to_snps.sh`
Runs `convert_baseline_to_snps.sh` for all chromosomes

###`convert_baseline_to_snps.sh [CHR]`
Converts `baselineLD.[CHR].l2.ldscore.gz` to `hm.[CHR].snp`, 
a file containing just the rsID for all snps in the baseline file

###`make_w_hm3.py`
Uses the G1000 dataset and hm files from above to create a single w_hm file for merging later

## Annotation files (directory: annot)
###`download_and_create_bed.sh [fname]`
Runs three scripts with input `fname`:
* `download_annot_csv.sh [fname]`
* `csv_to_bed.sh [fname]`
* `make_all_annot.sh [fname]`

###`download_annot_csv.sh [fname]`
Downloads the csv file for an annotation (`fname`) from s3

###`csv_to_bed.sh [fname]`
Converts `annot/[fname].csv` to `annot/[fname].bed` by adding "chr" to chromosome column

###`make_all_annot.sh [fname]`
Runs `make_annot.sh [fname] [CHR]` for all CHR

###`make_annot.sh [fname] [CHR]`
Runs the `make_annot.py` method for `ldsc` with option:
* `--bed-file annot/[fname].bed` (annotation input)
* `--bimfile g1000_plink_eur/1000G.EUR.QC.[CHR].bim` (downloaded from https://alkesgroup.broadinstitute.org/LDSCORE/1000G_Phase3_plinkfiles.tgz)
* `--annot annot/[fname].[CHR].annot.gz` (output)

###`make_all_annot_l2.sh [fname]`
Runs `make_annot_l2.sh [fname] [CHR]` for all CHR

###`make_annot_l2.sh [fname] [CHR]`
Runs the `ldsc.py` method for `ldsc` with option:
* `--l2` (make l2 version of ld score)
* `--bfile g1000_plink_eur/1000G.EUR.QC.[CHR]` (see above)
* `--ld-wind-cm 1` (1 centiMorgan window)
* `--annot annot/[fnam].[CHR].annot.gz` (annotation file)
* `--thin-annot` (only one column in annotation file)
* `--print-snps baseline_v2.2_snps/hm.[CHR].snp` (only keep these SNPs)
* `--out annot/[fname].[chr]` produces:
  * `[fname].[chr].l2.M`
  * `[fname].[chr].l2.M_5_50`
  * `[fname].[chr].l2.ldscore.gz` (LD Scores)

##Phenotype Files (directory: phenotype_files)
###`fetch_ancestry_file.sh [phenotype]`
* Fetches all parts for european ancestry specific metaanalysis for [phenotype]
* Combines the parts into a single file
* Moves the file and deletes the individual parts

###`fetch_snp_file.sh`
Creates large (~1GB) file from S3 which maps varID to rsID
* Fetches individual parts from VEP output
* Combines parts into single file
* Moves file and removes individual parts

###`make_substats_input.py --phenotype=[phenotype]`
* Loads `snp.csv` into dict to map varID to rsID
* Streams in `[phenotype]_EUR.json` file
* For each line if varID in snp map save five columns:
  * `snp_map[line['varId']]` - rsID
  * `line['reference'].lower()` - reference allele as lower-case
  * `line['alt'].lower()` - alternate allele as lower-case
  * `line['pValue']` - pValue
  * `line['n']` - number of samples
* Outputs: `[phenotype]_EUR.txt`

###`munge_stats.sh [phenotype]`
Runs `munge_stats.py` method from `ldsc` with options:
* `--sumstats phenotype_files/[phenotype]_EUR.txt` (input file)
* `--merge-alleles w_hm3.snplist` (snp list with alleles)
* `--a1-inc` (allele increasing means ???)
* `--out ../phenotype_files/[phenotype]` (output, produces `[phenotype].sumstats.gz`)

## Weights
###`generate_all_weights.sh`
Runs `generate_weights.sh` for all chromosomes

###`generate_weights.sh [CHR]`
Runs `ldsc.py` method from `ldsc` with options:
* `--l2` (make l2 version of ld score)
* `--bfile g1000_plink_eur/1000G.EUR.QC.[CHR]` (see above)
* `--ld-wind-cm 1` (1 centiMorgan window)
* `--extract baseline_v2.2_snps/hm.[CHR].snp` (only use baseline SNPs in calculation)
* `--out weights/weights.[CHR]` produces:
    * `weights.[chr].l2.M`
    * `weights.[chr].l2.M_5_50`
    * `weights.[chr].l2.ldscore.gz` (LD Scores)
NOTE: The weights are LD scores where the SNPs used are limited to those in the model

## Frequencies
###`generate_frequencies.py`
Calculates "frequencies" for filtering. 
* MAF = 1 - mean(allele number) / 2
* MAF calculated from bed file (of bim/bed/fam)
* N = length of fam file * 2
* output: `frq/chr.[CHR].frq` for all chromosomes

## Model
###`run_annot_baseline.sh [phenotype] [fname]`
Runs `ldsc.py` from `ldsc` with options:
* `--h2 ../phenotype_files/[phenotype].sumstats.gz` (run h2 regression with phenotype sumstats)
* `--ref-ld-chr annot/[fname].,baselineLD/baselineLD.` (use baseline with additional annotation)
* `--w-ld-chr ../weights/weights.` (weights)
* `--overlap-annot` (??? Not sure, from tutorial)
* `--frqfile-chr ../frq/chr.` (frequency, for filtering)
* `--out ../output/[phenotype]_[fname]` (outputs `[phenotype]_[fname].results`)
