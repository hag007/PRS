#!/bin/bash
set -e

source constants.sh 
source parse_args.sh $@
source parse_chrs.sh
eval $(parse_chrs $chrs)

target_source_dataset=${datasets_path}${src}'/'
imputation_path=${reference_path}'imputation/'

# First, make sure you have the sample files (bfiles - ds.bem, ds.bim and ds.fam, or ds.vcf) and reference panel files (can be downloaded it from beagle website).

echo '# Convert bfiles to vcfs'
# for i in $chrs_range ; do plink --bfile ${target_source_dataset}ds --recode vcf-iid --out ${target_source_dataset}/ds; done
plink --bfile ${target_source_dataset}original/ds --recode vcf-iid --out ${target_source_dataset}original/ds --memory 500000

echo '# Prepare a directory for imputed files'
{ 
  mkdir ${target_source_dataset}imputed 
} || { 
  echo "Imputed folder already exists. Skipping.." 
}

echo '# Run beagles on vcf reference panel'
for i in ${chrs_range[@]} ; do java -Xmx400g -jar ${beagle_path}beagle.jar gt=${target_source_dataset}original/ds.vcf ref=${imputation_path}panels/1000G_ALL/chr${i}.bref3 out=${target_source_dataset}imputed/ds.imputed.${i} chrom=${i} map=${imputation_path}maps/1000G_ALL/chr${i}.map window=100; done
