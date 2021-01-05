#!/bin/bash
set -e

base_path='/specific/elkon/hagailevi/PRS/'
codebase_path=${base_path}'codebase/'
GWASs_path=${base_path}'GWASs/'
datasets_path=${base_path}'datasets/'
target_dataset=${datasets_path}${1}'/'

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



plink --bfile ${target_dataset}ds --list-duplicate-vars --out ${target_dataset}ds 
plink --bfile ${target_dataset}ds --exclude ${target_dataset}ds.dupvar --recode vcf-iid --out ${target_dataset}ds
