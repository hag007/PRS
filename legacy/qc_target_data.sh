#!/bin/bash
set -e
source constants.sh
source parse_args.sh "$@"

# Parse input
discovery_gwas=${GWASs_path}${discovery}'/'
target_dataset=${datasets_path}${target}'/'

# Run pipeline
echo QC
plink \
    --bfile ${target_dataset}ds \
    --maf 0.05 \
    --hwe 1e-6 \
    --geno 0.01 \
    --write-snplist \
    --make-just-fam \
    --out ${target_dataset}ds.QC

echo remove highly correlated SNPs
plink \
    --bfile ${target_dataset}ds \
    --keep ${target_dataset}ds.QC.fam \
    --extract ${target_dataset}ds.QC.snplist \
    --indep-pairwise 200 50 0.25 \
    --out ${target_dataset}ds.QC

#echo Heterozygosity rates
#plink \
#    --bfile ${target_dataset}ds \
#    --extract ${target_dataset}ds.QC.prune.in \
#    --keep ${target_dataset}ds.QC.fam \
#    --het \
#    --out ${target_dataset}ds.QC
#
#echo filter F ceofficent outliers
#Rscript ${codebase_path}filter_f_outliers.R ${2}
#
#echo correct mismatching SNPs
#Rscript ${codebase_path}resolve_mismatch_SNPs_1.R ${1} ${2}
#
#echo Make a back up
#mv ${target_dataset}ds.bim ${target_dataset}ds.bim.bk
#ln -s ${target_dataset}ds.QC.adj.bim ${target_dataset}ds.bim
#
#echo sex check
#
#{
#plink \
#    --bfile ${target_dataset}ds \
#    --extract ${target_dataset}ds.QC.prune.in \
#    --keep ${target_dataset}ds.valid.sample \
#    --check-sex \
#    --out ${target_dataset}ds.QC && \
#
#echo assign sex && \
#Rscript ${codebase_path}assign_sex_2.R ${2} && \
#relatedness_input=ds.QC.valid
#} || {
#relatedness_input=ds.valid.sample
#echo error while analyzing sex. skipping...
#}
#
#echo remove related samples
#plink \
#    --bfile ${target_dataset}ds \
#    --extract ${target_dataset}ds.QC.prune.in \
#    --keep ${target_dataset}${relatedness_input} \
#    --rel-cutoff 0.125 \
#    --out ${target_dataset}ds.QC

echo "generate a QC'ed dataset"
plink \
    --bfile ${target_dataset}ds \
    --make-bed \
    --keep ${target_dataset}ds.QC.rel.id \
    --out ${target_dataset}ds.QC \
    --extract ${target_dataset}ds.QC.snplist \
    --exclude ${target_dataset}ds.mismatch
