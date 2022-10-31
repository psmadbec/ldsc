import gzip

studies = """""".strip().split('\n')

# studies = """Coding_UCSC
# Coding_UCSC.flanking.500
# Conserved_LindbladToh
# Conserved_LindbladToh.flanking.500
# CTCF_Hoffman
# CTCF_Hoffman.flanking.500
# DGF_ENCODE
# DGF_ENCODE.flanking.500
# DHS_peaks_Trynka
# DHS_Trynka
# DHS_Trynka.flanking.500
# Enhancer_Andersson
# Enhancer_Andersson.flanking.500
# Enhancer_Hoffman
# Enhancer_Hoffman.flanking.500
# FetalDHS_Trynka
# FetalDHS_Trynka.flanking.500
# H3K27ac_Hnisz
# H3K27ac_Hnisz.flanking.500
# H3K27ac_PGC2
# H3K27ac_PGC2.flanking.500
# H3K4me1_peaks_Trynka
# H3K4me1_Trynka
# H3K4me1_Trynka.flanking.500
# H3K4me3_peaks_Trynka
# H3K4me3_Trynka
# H3K4me3_Trynka.flanking.500
# H3K9ac_peaks_Trynka
# H3K9ac_Trynka
# H3K9ac_Trynka.flanking.500
# Intron_UCSC
# Intron_UCSC.flanking.500
# PromoterFlanking_Hoffman
# PromoterFlanking_Hoffman.flanking.500
# Promoter_UCSC
# Promoter_UCSC.flanking.500
# Repressed_Hoffman
# Repressed_Hoffman.flanking.500
# SuperEnhancer_Hnisz
# SuperEnhancer_Hnisz.flanking.500
# TFBS_ENCODE
# TFBS_ENCODE.flanking.500
# Transcr_Hoffman
# Transcr_Hoffman.flanking.500
# TSS_Hoffman
# TSS_Hoffman.flanking.500
# UTR_3_UCSC
# UTR_3_UCSC.flanking.500
# UTR_5_UCSC
# UTR_5_UCSC.flanking.500
# WeakEnhancer_Hoffman
# WeakEnhancer_Hoffman.flanking.500
# GTEx_eQTL_MaxCPP
# BLUEPRINT_H3K27acQTL_MaxCPP
# BLUEPRINT_H3K4me1QTL_MaxCPP
# BLUEPRINT_DNA_methylation_MaxCPP
# Conserved_Vertebrate_phastCons46way
# Conserved_Vertebrate_phastCons46way.flanking.500
# Conserved_Mammal_phastCons46way
# Conserved_Mammal_phastCons46way.flanking.500
# Conserved_Primate_phastCons46way
# Conserved_Primate_phastCons46way.flanking.500
# BivFlnk
# BivFlnk.flanking.500
# Human_Promoter_Villar
# Human_Promoter_Villar.flanking.500
# Human_Enhancer_Villar
# Human_Enhancer_Villar.flanking.500
# Human_Promoter_Villar_ExAC
# Human_Promoter_Villar_ExAC.flanking.500
# MAFbin1
# MAFbin2
# MAFbin3
# MAFbin4
# MAFbin5
# MAFbin6
# MAFbin7
# MAFbin8
# MAFbin9
# MAFbin10
# Ancient_Sequence_Age_Human_Promoter
# Ancient_Sequence_Age_Human_Promoter.flanking.500
# Ancient_Sequence_Age_Human_Enhancer
# Ancient_Sequence_Age_Human_Enhancer.flanking.500
# Human_Enhancer_Villar_Species_Enhancer_Count
# Nucleotide_Diversity_10kb
# Backgrd_Selection_Stat
# Recomb_Rate_10kb
# CpG_Content_50kb""".strip().split('\n')


def get_new_study(study, CHR):
    with gzip.open(f'../baseline_annot/{study}.{CHR}.annot.gz', 'r') as f:
        new_study = [a.strip().decode() for a in f.readlines()[1:]]
    return new_study


def get_old_study(study, CHR):
    old_study = []
    with gzip.open(f'../baselineLD/baselineLD.{CHR}.annot.gz', 'r') as f:
        header = f.readline().split(b'\t')
        idx = [a.strip() for a in header].index(str.encode(study))
        for line in f.readlines():
            split_line = line.split(b'\t')
            old_study.append(split_line[idx].decode())
    return old_study


def get_debug(CHR):
    with open(f'../g1000_plink_eur/1000G.EUR.QC.{CHR}.bim', 'r') as f:
        debug = f.readlines()
    return debug


def compare_outputs():
    print(len(studies))
    for study in studies:
        for CHR in range(1, 23):
            num_bad = 0
            num_bad_float = []
            old_study = get_old_study(study, CHR)
            new_study = get_new_study(study, CHR)
            for i, (old_line, new_line) in enumerate(zip(old_study, new_study)):
                if abs(float(old_line) - float(new_line)) != 0:
                    num_bad += 1
                if abs(float(old_line) - float(new_line)) > 1E-4:
                    num_bad_float.append(i)
                    print(i + 1, old_line, new_line)
                    print(xxx)
            if num_bad != 0:
                print(f"Warning! CHR {CHR} {num_bad} lines do not match in {study} ({len(num_bad_float)} floats)")
            else:
                print(f"{study} {CHR} Good!")


def main():
    compare_outputs()


if __name__ == '__main__':
    main()
