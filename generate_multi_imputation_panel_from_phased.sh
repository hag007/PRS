#!/bin/bash
set -e 

source constants_.sh
source parse_args.sh "$@"

# Parse input
if [[ -z ${chr} ]]; then echo "Please specify chr index"; exit 1; fi
if [[ -z ${pop} ]]; then pop="all"; fi
if [[ -z ${thread} ]]; then thread=30; fi
if [[ -z ${vcf_path} ]]; then vcf_path='/specific/elkon/hagailevi/data-scratch/1000G_ALL'; fi
if [[ -z ${threads} ]]; then threads=30; fi
if [[ -z ${memory} ]]; then memory=500000; fi
if [[ -z ${stage} ]]; then stage=4; fi
if [[ -z ${target} ]]; then target="$PRS_DATASETS/1kg"; fi
if [[ -z ${force} ]]; then force=false; fi



echo "make dir ${vcf_path}/multi/${pop} (if not exists)"
mkdir -p ${vcf_path}/multi/${pop} || echo ""


echo 'create a subset of individuals in a haps/legend/sample format'
if [[ ! -f ${vcf_path}/multi/${pop}/chr${chr} ]] || [[ ${force} ]]; then
# if [[ false ]]; then
    
    if [[ -z ${extract} ]]; then
        # plink2 --vcf ${vcf_path}/chr${chr}.vcf.gz --keep ${target}/pop.${pop}.panel --export haps --out ${vcf_path}/multi/${pop}/chr${chr}
        bcftools convert ${vcf_path}/chr${chr}.vcf.gz --samples-file ${target}/pop.${pop}.panel --hapsample ${vcf_path}/multi/${pop}/chr${chr} --vcf-ids
        # bcftools convert ${vcf_path}/chr${chr}.vcf.gz --samples-file ${target}/pop.${pop}.panel --haplegendsample ${vcf_path}/multi/${pop}/chr${chr}
        gunzip /specific/elkon/hagailevi/data-scratch/1000G_ALL/multi/${pop}/chr${chr}.hap.gz
        mv /specific/elkon/hagailevi/data-scratch/1000G_ALL/multi/${pop}/chr${chr}.hap /specific/elkon/hagailevi/data-scratch/1000G_ALL/multi/${pop}/chr${chr}.haps
        mv /specific/elkon/hagailevi/data-scratch/1000G_ALL/multi/${pop}/chr${chr}.samples /specific/elkon/hagailevi/data-scratch/1000G_ALL/multi/${pop}/chr${chr}.sample
        echo "skip..."
    else
        echo "TBD: add extract option for filtering SNPs"
        exit 1

        # plink2 --vcf ${vcf_path}/chr${chr}.vcf.gz --keep ${target}/pop.${pop}.panel --extract ${target}/${extract} --export haps --out ${vcf_path}/multi/${pop}/chr${chr}
        # bcftools convert ${vcf_path}/chr${chr}.vcf.gz --hapsample ${vcf_path}/multi/${pop}/chr${chr}.hap
    fi
fi


# echo 'convert haps/legend/sample to haps/sample format'
# paste -d ' ' <(zcat chr${chr}.legend.gz | tail -n +2 -q) <(zcat chr${chr}.haps.gz) | awk '{ print 2" "$0 }' > chr2.21.shapeit.haps


echo 'create a reference panel using shapeit'
shapeit -convert --input-haps ${vcf_path}/multi/${pop}/chr${chr} --output-log ${vcf_path}/multi/${pop}/chr${chr}.log --output-ref ${vcf_path}/multi/${pop}/chr${chr}.ref.hap ${vcf_path}/multi/${pop}/chr${chr}.ref.legend.gz ${vcf_path}/multi/${pop}/chr${chr}.ref.sample --thread ${thread}
