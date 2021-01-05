#!/bin/bash
set -e

source constants.sh
source parse_args.sh $@
source parse_chrs.sh
eval $(parse_chrs $chrs)
target_source_dataset=${datasets_path}${src}'/'


if [[ -z imp ]]; then
    imp="imputed";
fi

if [[ -z threads ]]; then
    threads=22;
fi

# if [[ $2 == *'-'* ]]; then 
# 
#    chrs_range=(${2//-/ })
#    chrs_range=$(seq ${chrs_range[0]} ${chrs_range[1]})
# else
#    chrs_range=(${2//,/ })
#    chrs_range=${chrs_range[@]}
# 
# fi

echo '# Reindex each imputed file before concatenating chrs into a single vcf file'
declare -a pids=(); for i in ${chrs_range[@]}; do (bcftools index -f ${target_source_dataset}imputed/ds.${imp}.${i}.vcf.gz; echo done chr${i})& pids+=($!); if [[ ${#pids[@]} -ge ${threads} ]]; then wait "${pids[@]}"; pids=(); fi; done; wait "${pids[@]}"

echo '# Concatenate vcf files into a single files'
x=""; for i in ${chrs_range[@]}; do x+=" ${target_source_dataset}/imputed/ds.imputed.${i}.vcf.gz";done; bcftools concat $x -Oz -o ${target_source_dataset}${imp}/ds.${imp}.all.vcf.gz --threads 80

echo '# Convert the integrated vcf files to a bfile'
plink --vcf ${target_source_dataset}${imp}/ds.${imp}.all.vcf.gz --double-id --make-bed --out ${target_source_dataset}/${imp}/ds
