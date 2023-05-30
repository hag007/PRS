#!/bin/bash
set -e
source constants_.sh
source parse_args.sh "$@"

# Parse input
target_dataset="${datasets_path}${target}/${imp}/"
# ref_dataset="${datasets_path}${target%%_*}/${imp}/"
ref_dataset=${datasets_path}/${ref_dataset}/
if [[ -z ${maf} ]]; then maf=0.05; fi
if [[ -z ${geno} ]]; then geno=0.1; fi
if [[ -z ${imp} ]]; then imp="original"; fi
if [[ -z ${memory} ]]; then memory=500000; fi
if [[ -z ${threads} ]]; then threads=80; fi
if [[ -z ${stage} ]]; then stage=4; fi

# Start pipeline
if [[ ${stage} -le 1 ]]; then
	echo '### perform prunning ###'
	plink \
		--bfile ${ref_dataset}ds.QC \
		--out ${ref_dataset}dsX \
		--memory ${memory} \
		--threads ${threads} \
		--indep-pairwise 200 50 0.25
fi

if [[ ${stage} -le 2 ]]; then
	echo '### calc ref pca'
	plink2 \
		--bfile ${ref_dataset}ds.QC \
		--out ${ref_dataset}dsX.ref \
		--memory ${memory} \
		--threads ${threads} \
		--extract ${ref_dataset}dsX.prune.in \
		--freq \
		--pca approx biallelic-var-wts 6
fi
if [[ ${stage} -le 3 ]]; then
	echo  "calc target pca"
	plink2 \
		--bfile ${target_dataset}ds.QC \
		--out ${target_dataset}dsX.pca \
		--memory ${memory} \
		--threads ${threads} \
		--extract ${ref_dataset}dsX.prune.in \
		--geno 0.1 \
		--mind 0.1 \
		--read-freq ${ref_dataset}dsX.ref.afreq \
		--score ${ref_dataset}dsX.ref.eigenvec.var 2 3 header-read no-mean-imputation variance-standardize \
		--score-col-nums 5-10
fi
# if [[ ${stage} -le 4 ]]; then
# 	echo  "calc target pca"
# 	plink2 \
# 		--bfile ${target_dataset}ds.QC \
# 		--out ${target_dataset}dsX.pca \
# 		--memory ${memory} \
# 		--threads ${threads} \
# 		--extract ${ref_dataset}dsX.prune.in \
# 		--geno 0.1 \
# 		--mind 0.1 \
# 		--read-freq ${ref_dataset}dsX.ref.acount \
# 		--score ${ref_dataset}dsX.ref.eigenvec.allele 2 5 header-read no-mean-imputation  
# fi
if [[ ${stage} -le 5 ]]; then
      echo '### calc target2  pca'
      plink2 \
              --bfile ${target_dataset}ds.QC \
              --out ${target_dataset}dsX2 \
              --memory ${memory} \
              --threads ${threads} \
              --extract ${target_dataset}dsX.prune.in \
              --pca approx  6
fi

