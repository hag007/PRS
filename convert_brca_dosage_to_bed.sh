#!/bin/bash
source parse_args.sh "$@" 

mkdir -p $PRS_DATASETS_ELKON/cimba/original/raw/dat || true 2&> /dev/null
mkdir -p $PRS_DATASETS_ELKON/cimba/original/raw/bed || true 2&> /dev/null

echo "Create dat file header"
cat $PRS_DATASETS_ELKON/cimba/original/raw/215_brca${brca_type}_sample_order.txt | awk 'BEGIN {printf "SNP\tA1\tA2\t"} {printf $1" "$1"\t"} END {print ""}' > $PRS_DATASETS_ELKON/cimba/original/raw/dat/brca${brca_type}_chr${chr}.dat

echo "Create dat file content"
paste <(cat $PRS_DATASETS_ELKON/cimba/original/raw/onco_brca${brca_type}_info_chr${chr}_varid.txt | tail -n +2 | awk '{ if(substr($5,1,2) == "rs"){ split($5,a, ":"); print a[1]"\t"$7"\t"$8;}}' ) <(gunzip -c  $PRS_DATASETS_ELKON/cimba/original/raw/215_brca${brca_type}_oncoarray_imputed_dosages_chr${chr}.txt.gz  | awk -v FS=' ' -v OFS='\t' '{$1=$1; if(substr($1,1,2) == "rs"){ print $0 }}' | cut -f 5-) >> $PRS_DATASETS_ELKON/cimba/original/raw/dat/brca${brca_type}_chr${chr}.dat

echo "Create fam file"
cat $PRS_DATASETS_ELKON/cimba/original/raw/215_brca${brca_type}_sample_order.txt | awk '{print $1" "$1" 0 0 0 9"}' > $PRS_DATASETS_ELKON/cimba/original/raw/dat/brca${brca_type}_chr${chr}.fam

echo "convert dat to bed files"
plink2 --import-dosage $PRS_DATASETS_ELKON/cimba/original/raw/dat/brca${brca_type}_chr${chr}.dat format=1 --fam $PRS_DATASETS_ELKON/cimba/original/raw/dat/brca${brca_type}_chr${chr}.fam --make-bed --out $PRS_DATASETS_ELKON/cimba/original/raw/bed/brca${brca_type}_chr${chr}
