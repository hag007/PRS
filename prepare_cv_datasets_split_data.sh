source ./constants_.sh
source ./parse_args.sh "$@"

source ./init_args_cv.sh

hapmap_file_name="hapmap.all.rs"
if [[ -z $hapmap_snps_only || $hapmap_snps_only == false ]]; then
       	extract_hapmap=""
	geno_num=0.1
	mind_num=0.1
	maf_param="--maf 0.05"
else
	extract_hapmap="--extract ${PRS_CODEBASE}/hapmap3_pop/${hapmap_file_name}"
	geno_num=0.3
	mind_num=0.3
	maf_param=""
fi

if [[ -z $data ]]; then echo "you forgot to input whether you want to split the validation or the train data"; fi
if [[ $data == "train" || $data == "both" ]]; then suffix=${train_suffix}; else suffix=${test_suffix}; fi
test_suffix_0=${suffix}0
test_suffix_1=${suffix}1
# too lazy so i kept the param "test" though it can hold the train suffix

if [[ ! -f ${imp_path}ds_${pheno}_${pop}${test_suffix_0}.bed ]]; then
plink2 \
    --bfile ${imp_path}ds_${pheno}_${pop}${suffix} \
    --keep ${target_path}pheno_${pheno}_${pop}${test_suffix_0} \
    ${extract_hapmap} \
    ${maf_param} \
    --geno ${geno_num} \
    --mind ${mind_num} \
    --make-bed \
    --memory 20000 \
    --threads 5 \
    --out ${imp_path}ds_${pheno}_${pop}${test_suffix_0}
fi

if [[ ! -f ${imp_path}ds_${pheno}_${pop}${test_suffix_1}.bed ]]; then
plink2 \
    --bfile ${imp_path}ds_${pheno}_${pop}${suffix} \
    --keep ${target_path}pheno_${pheno}_${pop}${test_suffix_1} \
    ${extract_hapmap} \
    ${maf_param} \
    --geno ${geno_num} \
    --mind ${mind_num} \
    --make-bed \
    --memory 20000 \
    --threads 5 \
    --out ${imp_path}ds_${pheno}_${pop}${test_suffix_1}
fi

if [[ ! -f ${imp_path}ds.dupvar ]]; then
	echo "remove duplicated SNPs- create dupvar file"
	echo "" > ${imp_path}ds.dupvar
	cat ${imp_path}ds.bim | cut -f 2 | sort | uniq -d >> ${imp_path}ds.dupvar
fi

if [[ ! -f ${imp_path}ds_${pheno}_${pop}${test_suffix_0}.eigenvec ]]; then
echo '### calculate the first 6 PCs for train set###'
plink \
  --bfile ${imp_path}ds_${pheno}_${pop}${test_suffix_0} \
  --indep-pairwise 200 50 0.25 \
  --memory 20000 \
  --threads 5 \
  --out ${imp_path}ds_${pheno}_${pop}${test_suffix_0}

plink \
  --bfile ${imp_path}ds_${pheno}_${pop}${test_suffix_0} \
  --extract ${imp_path}ds_${pheno}_${pop}${test_suffix_0}.prune.in \
  --pca 6 \
  --mind 1 \
  --memory 20000 \
  --threads 5 \
  --out ${imp_path}ds_${pheno}_${pop}${test_suffix_0} \
  --geno 1
fi

if [[ ! -f ${imp_path}ds_${pheno}_${pop}${test_suffix_1}.eigenvec ]]; then
echo '### calculate the first 6 PCs for train set###'
plink \
  --bfile ${imp_path}ds_${pheno}_${pop}${test_suffix_1} \
  --indep-pairwise 200 50 0.25 \
  --memory 20000 \
  --threads 5 \
  --out ${imp_path}ds_${pheno}_${pop}${test_suffix_1}

plink \
  --bfile ${imp_path}ds_${pheno}_${pop}${test_suffix_1} \
  --extract ${imp_path}ds_${pheno}_${pop}${test_suffix_1}.prune.in \
  --pca 6 \
  --mind 1 \
  --out ${imp_path}ds_${pheno}_${pop}${test_suffix_1} \
  --geno 1 \
  --memory 20000 \
  --threads 5
fi


