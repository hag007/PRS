set -e
source parse_args.sh "$@"
source constants_.sh

if [[ -z ${imp}  ]]; then imp="original"; fi
if [[ -z ${memory}  ]]; then memory="600000"; fi
if [[ -z ${threads}  ]]; then threads="80"; fi
if [[ -z ${maf}  ]]; then maf="0.05"; fi
if [[ -z ${geno}  ]]; then geno="0.1"; fi
if [[ -z ${mind}  ]]; then mind="0.1"; fi
if [[ -z ${pop}  ]]; then pop=""; fi
if [[ ${pop} != "" ]]; then
	pop=_${pop}
fi

discovery_path=${GWASs_path}${discovery}'/'
target_path=${datasets_path}${target}"/${imp}/"
prs_path=${PRSs_path}${discovery}_${target}"/${imp}/"


if [[ ${stage} -le 1 ]]; then

echo '### QC ###'

echo "." > ${target_path}ds.dupvar
cat ${target_path}ds.bim | cut -f 2 | sort | uniq -d >> ${target_path}ds.dupvar

plink \
    --bfile ${target_path}ds \
    --exclude ${target_path}ds.dupvar \
    --keep ${datasets_path}${target}/pop${pop}.panel \
    --out ${target_path}ds${pop}.QC \
    --maf ${maf} \
    --hwe 1e-6 \
    --geno ${geno} \
    --mind ${mind} \
    --make-bed 

fi

#   --remove ${target_path}ds.excluded.populations \
#     --mind 0.7 \
#     --make-just-fam \
#     --write-snplist \

# echo '### remove highly correlated SNPs ###'
# plink \
#     --bfile ${target_path}ds \
#     --keep ${target_path}ds.QC.fam \
#     --extract ${target_path}ds.QC.snplist \
#     --indep-pairwise 400 100 0.4 \
#     --out ${target_path}ds.QC
# 
# echo Heterozygosity rates
# plink \
#     --bfile ${target_path}ds \
#     --extract ${target_path}ds.QC.prune.in \
#     --keep ${target_path}ds.QC.fam \
#     --het \
#     --out ${target_path}ds.QC
# 
# echo filter F ceofficent outliers
# Rscript ${codebase_path}filter_f_outliers.R ${2}
# 
# # echo correct mismatching SNPs
# # Rscript ${codebase_path}resolve_mismatch_SNPs_1.R ${1} ${2}
# 
# # echo Make a back up
# # mv ${target_path}ds.bim ${target_dataset}ds.bim.bk
# # ln -s ${target_path}ds.QC.adj.bim ${target_dataset}ds.bim
# 
# # echo sex check
# # 
# # {
# # plink \
# #     --bfile ${target_path}ds \
# #     --extract ${target_path}ds.QC.prune.in \
# #     --keep ${target_path}ds.valid.sample \
# #     --check-sex \
# #     --out ${target_path}ds.QC && \
# # 
# # echo assign sex && \
# # Rscript ${codebase_path}assign_sex_2.R ${2} && \
# # relatedness_input=ds.QC.valid 
# # } || {
# # relatedness_input=ds.valid.sample
# # echo error while analyzing sex. skipping...
# # }
# 
# relatedness_input=ds.valid.sample
# 
# echo '### remove related samples ###'
# plink \
#     --bfile ${target_path}ds \
#     --extract ${target_path}ds.QC.prune.in \
#     --keep ${target_path}${relatedness_input} \
#     --rel-cutoff 0.125 \
#     --out ${target_path}ds.QC
# 
# echo "### generate a QC'ed dataset ###"
# plink \
#     --bfile ${target_path}ds \
#     --make-bed \
#     --out ${target_path}ds.QC \
#     --extract ${target_path}ds.QC.snplist \
#     --keep ${target_path}ds.QC.rel.id \
# #     --exclude ${target_path}ds.mismatch


if [[ ${stage} -le 2 ]]; then

echo '### perform prunning ###'
plink \
	--bfile ${target_path}ds${pop}.QC \
	--indep-pairwise 200 50 0.25 \
	--out ${target_path}ds${pop}

fi
if [[ ${stage} -le 3 ]]; then
echo '### calculate the first 6 PCs ###'
plink \
	--bfile ${target_path}ds${pop}.QC \
	--extract ${target_path}ds${pop}.prune.in \
	--pca 6 \
	--mind 1 \
	--out ${target_path}ds${pop} \
	--geno 1

fi
