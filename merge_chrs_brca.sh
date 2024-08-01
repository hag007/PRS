#!/bin/bash
set -e

source constants_.sh
source parse_args.sh "$@"
source parse_chrs.sh
eval $(parse_chrs $chrs)
target_dataset=${datasets_path}'/ragnaron'

# if [[ -z ${threads} ]]; then threads=22; fi

echo '# Reindex each imputed file before concatenating chrs into a single vcf file'
# declare -a pids=(); for i in "${chrs_range[@]}"; do (bcftools index -f ${target_dataset}/SHEBA_Freeze_Seven.${i}.NF.vcf.gz; echo done chr${i})& pids+=($!); if [[ ${#pids[@]} -ge ${threads} ]]; then wait "${pids[@]}"; pids=(); fi; done; wait "${pids[@]}"

echo '# Concatenate vcf files into a single files'
# x=""; for i in "${chrs_range[@]}"; do x+=" ${target_dataset}/SHEBA_Freeze_Seven.${i}.NF.vcf.gz";done; bcftools concat $x -Oz -o ${target_dataset}/ds.all.vcf.gz --threads 80

echo '# Convert the integrated vcf files to a bfile'
plink2 --vcf ${target_dataset}/ds.all.vcf.gz --double-id --vcf-half-call missing --make-bed --out ${target_dataset}/${imp}/ds

