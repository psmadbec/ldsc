# At the moment this can be done two ways.
# (1) Run VEP against the varIDs with GERP set up (instructions to follow)
# (2) Use the BigWig file, convert it, and generate the final file directly

# (1)
# If VEP is available on a machine that is easiest. Not too terribly difficult as well is to use the available docker
# docker pull ensemblorg/ensembl-vep
# You'll also have to download the bw file:
# curl https://hgdownload.soe.ucsc.edu/gbdb/hg19/bbi/All_hg19_RS.bw > All_hg19_RS.bw
# And also the cache (which is quite large)
# curl ftp://ftp.ensembl.org/pub/release-107/variation/indexed_vep_cache/homo_sapiens_vep_107_GRCh37.tar.gz > homo_sapiens_vep_107_GRCh37.tar.gz
# Put those into a directory and decompress the homo_sapien cache folder
# You'll also need formatted inputs, e.g. rows of `chr1 pos pos ref/alt`
# Finally by running:
# docker run -v <absolute path to above directory>:/app/ -it ensemblorg/ensembl-vep /bin/bash
# and then once inside running:
# ln -s ../app/All_hg19_RS.bw ./
#./vep --offline -i ../app/<formatted input> -o results.out --custom All_hg19_RS.bw,GERP,bigwig --ASSEMBLY GRCh37 --dir_cache /app/
# Then all that is left is converting the output to the appropriate files (coming up)
