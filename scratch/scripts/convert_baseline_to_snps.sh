#!/bin/bash

# chromosome
[ -z "$1" ] && { echo "Need to pass in chromosome"; exit 1; }
chr=$1

gzcat ../baselineLD/baselineLD.$chr.l2.ldscore.gz | tail -n +2 | awk '{print $2}' > ../baseline_v2.2_snps/hm.$chr.snp
hm_lines="$(wc -l < ../baseline_v2.2_snps/hm.$chr.snp | xargs)"
orig_lines=$(wc -l < <(gzcat ../baselineLD/baselineLD.$chr.l2.ldscore.gz) | xargs)
echo "Created hm.$chr.snp with $hm_lines lines from ../baselineLD/baselineLD.$chr.l2.ldscore.gz with $orig_lines lines"
