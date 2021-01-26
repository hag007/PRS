#!/bin/bash
set -e

source constants.sh
source parse_chrs.sh

# Parse input
eval $(parse_chrs $chrs)
target_dataset=${datasets_path}${target}'/'

# Run pipeline
for a in $chrs_range; do bcftools view --samples-file /specific/netapp5/gaga/data-scratch/hagailevi/1000G_EAS/chs_only /specific/netapp5/gaga/data-scratch/hagailevi/1000G_ALL/chr${a}.vcf -Ou | bcftools annotate --collapse snps  > /specific/netapp5/gaga/data-scratch/hagailevi/1000G_EAS/chr${a}.vcf; echo "done ${a}"; done 
# for a in $chrs_range; do bcftools annotate --collapse snps /specific/netapp5/gaga/data-scratch/hagailevi/1000G_ALL/chr${a}.vcf > /specific/netapp5/gaga/data-scratch/hagailevi/1000G_EAS/chr${a}.vcf; echo "done ${a}"; done 
