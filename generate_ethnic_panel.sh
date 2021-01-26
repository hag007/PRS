#!/bin/bash
set -e

base_path='/specific/elkon/hagailevi/PRS/'
codebase_path=${base_path}'codebase/'
GWASs_path=${base_path}'GWASs/'
datasets_path=${base_path}'datasets/'
target_dataset=${datasets_path}${1}'/'
reference_path='/specific/netapp5/gaga/data-scratch/hagailevi/'
ALL=${reference_path}'1000G_ALL/'
E=${reference_path}'1000G_'${1}'/'
E_panel=${reference_path}'imputation/panels/1000G_'${1}'/'
beagle_path='/specific/elkon/hagailevi/tools/beagle'
if [[ ! $2 == '' ]]; then

    if [[ $2 == *'-'* ]]; then 
    
       chrs_range=(${2//-/ })
       chrs_range=$(seq ${chrs_range[0]} ${chrs_range[1]})
    else
       chrs_range=(${2//,/ })
       chrs_range=${chrs_range[@]}
    
    fi

else
    chrs_range=('')
fi

for a in $chrs_range; do
    # plink --vcf ${1000G_ALL}chr${a}.vcf --keep ${1000G_E}included_ids --recode vcf-iid --out ${1000G_E}chr${a} 
    java -jar ${beagle_path}/vcf2bref3.jar ${E}chr${a}.vcf > ${E_panel}chr${a}.bref3

done
