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

if [[ -z ${mem} ]]; then 
    mem=500000
fi

target_dataset="${datasets_path}${target}/${imp}/"
ref_dataset="${datasets_path}${target%%_*}/${imp}/" 
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
# 
# n="$(wc -l ${target_dataset}ds.fam | awk '{print $1}')"
# echo $n
# 
# echo '### perform prunning ###'
# plink \
#     --bfile ${target_dataset}ds.QC \
#     --indep-pairwise 200 50 0.25 \
#     --out ${target_dataset}ds

echo '### calc ref pca'
plink2 --bfile ${ref_dataset}ds.QC \
       --extract ${ref_dataset}ds.prune.in \
       --freq counts \
       --pca approx allele-wts 6 \
       --out ${ref_dataset}ds.ref \
       --memory ${mem}

plink2 --bfile ${target_dataset}ds.QC \
       --extract ${ref_dataset}ds.prune.in \
       --read-freq ${ref_dataset}ds.ref.acount \
       --score ${ref_dataset}ds.ref.eigenvec.allele 2 5 header-read no-mean-imputation \
               variance-standardize \
       --score-col-nums 6-11 \
       --out ${target_dataset}ds.pca \
       --memory ${mem}

