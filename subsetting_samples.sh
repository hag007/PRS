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

for a in $chrs_range; do bcftools view --samples-file /specific/netapp5/gaga/data-scratch/hagailevi/1000G_EAS/chs_only /specific/netapp5/gaga/data-scratch/hagailevi/1000G_ALL/chr${a}.vcf -Ou | bcftools annotate --collapse snps  > /specific/netapp5/gaga/data-scratch/hagailevi/1000G_EAS/chr${a}.vcf; echo "done ${a}"; done 
# for a in $chrs_range; do bcftools annotate --collapse snps /specific/netapp5/gaga/data-scratch/hagailevi/1000G_ALL/chr${a}.vcf > /specific/netapp5/gaga/data-scratch/hagailevi/1000G_EAS/chr${a}.vcf; echo "done ${a}"; done 
