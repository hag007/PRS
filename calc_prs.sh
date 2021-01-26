#!/bin/bash
set -e
source constants.sh
source parse_args.sh "$@"

# Parse input
discovery_path=${GWASs_path}${discovery}'/'
target_path=${datasets_path}${target}"/${imp}/"
prs_path=${PRSs_path}${discovery}_${target}"/${imp}/"
if [[ -z ${maf} ]]; then maf=0.05; fi
if [[ -z ${geno} ]]; then geno=0.1; fi
if [[ -z ${imp} ]]; then imp="original"; fi
if [[ -z ${memory} ]]; then memory=500000; fi
if [[ -z ${threads} ]]; then threads=80; fi
if [[ -z ${stage} ]]; then stage=4; fi
if [[ -z ${pval_th}  ]]; then pval_th="0.1"; fi

# Start pipeline
mkdir -p $prs_path || echo ""
echo clumping
plink \
	--bfile ${target_path}ds.QC \
	--clump-p1 1 \
	--clump-p2 1 \
	--clump-r2 0.2 \
	--clump-kb 500 \
	--clump ${discovery_path}gwas.QC.Transformed \
	--clump-snp-field SNP \
	--clump-field P \
	--out ${prs_path}prs \
	--memory ${memory} \
	--threads ${threads} \
	--exclude ${target_path}ds.dupvar
echo filter by clumping
awk 'NR!=1{print $3}' ${prs_path}prs.clumped >  ${prs_path}prs.valid.snp

echo extract SNP p-value
awk '{print $1,$8}' ${discovery_path}gwas.QC.Transformed > ${prs_path}SNP.pvalue

echo pvalue inclusion criteria
echo "0.00000005 0 0.00000005" >> ${prs_path}range_list
echo "0.001 0 0.001" > ${prs_path}range_list
echo "0.05 0 0.05" >> ${prs_path}range_list
echo "0.1 0 0.1" >> ${prs_path}range_list
echo "0.2 0 0.2" >> ${prs_path}range_list
echo "0.3 0 0.3" >> ${prs_path}range_list
echo "0.4 0 0.4" >> ${prs_path}range_list
echo "0.5 0 0.5" >> ${prs_path}range_list
echo "1.0 0 1.0" >> ${prs_path}range_list

echo calculate PRS
plink \
	--bfile ${target_path}ds.QC \
	--score ${discovery_path}gwas.QC.Transformed 1 4 11 header \
	--q-score-range ${prs_path}range_list ${prs_path}SNP.pvalue \
	--extract ${prs_path}prs.valid.snp \
	--memory ${memory} \
	--threads ${threads} \
	--out ${prs_path}prs


if [[ -f "${datasets_path}${target}/pheno" ]]; then
	echo Finding the best-fit PRS
	Rscript-3.6.0 ${discovery} ${target} ${imp} ${pval_th};
fi

