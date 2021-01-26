#!/bin/bash
set -e
source constants.sh
source parse_args.sh "$@"

# Parse input
target_dataset="${datasets_path}${target}/${imp}/"

if [[ -z ${maf} ]]; then maf=0.05; fi
if [[ -z ${geno} ]]; then geno=0.1; fi
if [[ -z ${imp} ]]; then imp="original"; fi
if [[ -z ${memory} ]]; then memory=500000; fi
if [[ -z ${threads} ]]; then threads=80; fi
if [[ -z ${stage} ]]; then stage=4; fi
if [[ -z ${cluster_names} ]]; then
	cluster_names=""
else
	if [[ ${cluster_names} -eq -1 ]]; then
    	cluster_names='EUR AFR EAS SAS AMR OCN1 OCN2'
    else
    	cluster_names=${cluster_names//,/ }
    fi
fi
if [[ -z ${n_samples} ]]; then
	n_samples=6
else
	if [[ ${n_samples} -eq -1 ]]; then
		n_samples="$(wc -l ${target_dataset}ds.fam | awk '{print $1}')"
	fi
	if [[ ${n} -gte 8000 ]]; then
		n_samples=8000
	fi
fi

# Start pipeline
if [[ ${stage} -gte 1 ]]; then
	echo '### QC ###'
	plink \
		--bfile ${target_dataset}ds \
		--out ${target_dataset}ds.QC \
		--memory ${memory} \
		--threads ${threads} \
		--maf ${maf} \
		--geno ${geno} \
		--hwe 1e-6 \
		--make-bed
fi
if [[ ${stage} -gte 2 ]]; then
	echo '### perform prunning ###'
	plink \
		--bfile ${target_dataset}ds.QC \
		--out ${target_dataset}ds \
		--memory ${memory} \
		--threads ${threads} \
		--indep-pairwise 200 50 0.25
fi
if [[ ${stage} -gte 2 ]]; then
	echo '### calculate the first 6 PCs ###'
	plink \
		--bfile ${target_dataset}ds.QC \
		--out ${target_dataset}ds \
		--extract ${target_dataset}ds.prune.in \
		--memory ${memory} \
		--threads ${threads} \
		--geno 0.1 \
		--mind 0.1 \
		--pca ${n_samples}  \
		--within ${datasets_path}${target}'/pop.panel' \
		--pca-cluster-names ${cluster_names}
fi
 
