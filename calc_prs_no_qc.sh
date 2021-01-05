set -e
base_path='/specific/elkon/hagailevi/PRS/'
codebase_path=${base_path}'codebase/'
GWASs_path=${base_path}'GWASs/'
datasets_path=${base_path}'datasets/'
PRSs_path=${base_path}'PRSs/'
discovery_gwas=${GWASs_path}${1}'/'
target_dataset=${datasets_path}${2}'/'
prs_path=${PRSs_path}${1}_${2}'/'

mkdir $prs_path || echo ""

echo clumping
plink \
    --bfile ${target_dataset}ds \
    --clump-p1 1 \
    --clump-p2 1 \
    --clump-r2 0.2 \
    --clump-kb 500 \
    --clump ${discovery_gwas}gwas.QC.Transformed \
    --clump-snp-field SNP \
    --clump-field P \
    --out ${prs_path}prs

echo filter by clumping
awk 'NR!=1{print $3}' ${prs_path}prs.clumped >  ${prs_path}prs.valid.snp

echo extract SNP p-value
awk '{print $1,$8}' ${discovery_gwas}gwas.QC.Transformed > ${prs_path}SNP.pvalue

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
    --bfile ${target_dataset}ds \
    --score ${discovery_gwas}gwas.QC.Transformed 1 4 11 header \
    --q-score-range ${prs_path}range_list ${prs_path}SNP.pvalue \
    --extract ${prs_path}prs.valid.snp \
    --out ${prs_path}prs

echo perform prunning
plink \
    --bfile ${target_dataset}ds \
    --indep-pairwise 200 50 0.25 \
    --out ${target_dataset}ds

echo calculate the first 6 PCs
plink \
    --bfile ${target_dataset}ds \
    --extract ${target_dataset}ds.prune.in \
    --pca 6 \
    --out ${target_dataset}ds

# echo Finding the "best-fit" PRS
# Rscript best_fit_prs.R
