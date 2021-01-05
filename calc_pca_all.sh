set -e
source constants.sh
source parse_args.sh $@

maf=${maf}
geno=${geno}

if [[ -z ${imp} ]]; then
    imp="original"
fi

if [[ -z ${cn} ]]; then
    cn='EUR AFR EAS SAS AMR OCN1 OCN2'
fi

target_dataset="${datasets_path}${target}/${imp}/"

# echo '### QC ###'
# plink \
#     --bfile ${target_dataset}ds \
#     --maf ${maf} \
#     --hwe 1e-3 \
#     --geno ${geno} \
#     --make-bed \
#     --out ${target_dataset}ds.QC
# #   --remove ${target_dataset}ds.excluded.populations \
# #     --mind 0.7 \
# #     --make-just-fam \
# #     --write-snplist \

n="$(wc -l ${target_dataset}ds.fam | awk '{print $1}')"
echo $n

# echo '### perform prunning ###'
# plink \
#     --bfile ${target_dataset}ds.QC \
#     --indep-pairwise 200 50 0.25 \
#     --out ${target_dataset}ds

echo '### calculate the first 6 PCs ###'
plink \
    --bfile ${target_dataset}ds.QC \
    --extract ${target_dataset}ds.prune.in \
    --mind 0.1 \
    --out ${target_dataset}ds \
    --geno 0.1 \
    --pca 6 
#     --within ${datasets_path}${target}'/pop.panel' \
#     --pca-cluster-names ${cn}
 
