set -e

source constants.sh
source parse_args.sh $@

if [[ -z ${imp}  ]]; then imp="original"; fi
if [[ -z ${memory}  ]]; then memory="600000"; fi
if [[ -z ${threads}  ]]; then threads="80"; fi
if [[ -z ${maf}  ]]; then maf="80"; fi
if [[ -z ${geno}  ]]; then geno="80"; fi


target_dataset="${datasets_path}${target}/${imp}/"

  echo '### QC ###'
  
  plink \
      --bfile ${target_dataset}ds \
	  --out ${target_dataset}ds.QC \
      --memory ${memory} \
      --threads ${threads} \
      --maf ${maf} \
      --hwe 1e-6 \
      --geno ${geno} \
      --exclude ${target_dataset}ds.dupvar \
      --make-bed \
      --write-snplist \


       
  #     --remove ${target_dataset}ds.excluded.populations \
  #     --mind 0.7 \
  #     --make-just-fam \
  #     --write-snplist \
  echo '### remove highly correlated SNPs ###'
  
  plink \
      --bfile ${target_dataset}ds \
      --keep ${target_dataset}ds.QC.fam \
      --extract ${target_dataset}ds.QC.snplist \
      --indep-pairwise 400 100 0.4 \
      --memory ${memory} \
      --threads ${threads} \
      --out ${target_dataset}ds.QC
  
  echo Heterozygosity rates
  plink \
      --bfile ${target_dataset}ds \
      --extract ${target_dataset}ds.QC.prune.in \
      --keep ${target_dataset}ds.QC.fam \
      --het \
      --memory ${memory} \
      --threads ${threads} \
      --out ${target_dataset}ds.QC
  
  echo filter F ceofficent outliers
  Rscript ${codebase_path}filter_f_outliers.R ${target} ${imp}
#  
#  echo correct mismatching SNPs
#  Rscript ${codebase_path}resolve_mismatch_SNPs_1.R ${1} ${2}
 
#  echo Make a back up
#  mv ${target_dataset}ds.bim ${target_dataset}ds.bim.bk
#  ln -s ${target_dataset}ds.QC.adj.bim ${target_dataset}ds.bim
#  
#  echo sex check
#  
#  {
#  plink \
#      --bfile ${target_dataset}ds \
#      --extract ${target_dataset}ds.QC.prune.in \
#      --keep ${target_dataset}ds.valid.sample \
#      --check-sex \
#      --out ${target_dataset}ds.QC && \
#  
#  echo assign sex && \
#  Rscript ${codebase_path}assign_sex_2.R ${2} && \
#  relatedness_input=ds.QC.valid 
#  } || {
#  relatedness_input=ds.valid.sample
#  echo error while analyzing sex. skipping...
#  }
 
  relatedness_input=ds.valid.sample
 
#   echo '### remove related samples ###'
#   plink \
#       --bfile ${target_dataset}ds \
#       --extract ${target_dataset}ds.QC.prune.in \
#       --keep ${target_dataset}${relatedness_input} \
#       --rel-cutoff 0.125 \
#       --memory ${memory} \
#       --threads ${threads} \
#       --out ${target_dataset}ds.QC
 
  echo "### generate a QC'ed dataset ###"
  plink \
      --bfile ${target_dataset}ds \
      --make-bed \
      -out ${target_dataset}ds.QC \
      --extract ${target_dataset}ds.QC.snplist \
      --memory ${memory} \
      --threads ${threads} \
  #     --keep ${target_dataset}ds.QC.rel.id \
  #     --exclude ${target_dataset}ds.mismatch
 
  echo '### perform prunning ###'
  plink \
      --bfile ${target_dataset}ds.QC \
      --indep-pairwise 200 50 0.25 \
      --memory ${memory} \
      --threads ${threads} \
      --out ${target_dataset}ds
 

  if [[ -z ${cn} ]]; then
      cn='EUR AFR EAS SAS AMR OCN1 OCN2'
  else
      cn="(${cn//,/ })" 
  fi

  n="$(wc -l ${target_dataset}ds.fam | awk '{print $1}')"

  if [[ ${n} -lt 10000 ]]; then 
      echo '### calculate the first 6 PCs ###'
      plink \
          --bfile ${target_dataset}ds.QC \
          --extract ${target_dataset}ds.prune.in \
          --out ${target_dataset}ds \
          --memory ${memory} \
          --threads ${threads} \
          --pca 6
#  \
#           --within ${datasets_path}${target}'/pop.panel' \
#           --pca-cluster-names ${cn}

  else
    
      plink2 \
          --bfile ${target_dataset}ds.QC \
          --extract ${target_dataset}ds.prune.in \
          --out ${target_dataset}ds \
          --memory ${memory} \
          --threads ${threads} \
          --pca approx 6 # \
#         --within ${datasets_path}${target}'/pop.panel' \
#         --pca-cluster-names ${cn}
  fi
