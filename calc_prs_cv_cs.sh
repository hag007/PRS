#!/bin/bash

source constants_.sh
source parse_args.sh "$@"

source init_args_cv.sh

prs_prefix="prs.cv.cs_${pop}_${pheno}"
ds_prefix="ds_${pop}_${pheno}"

if [[ ${hp} == "" ]]; then
    hp="1-0.5"
fi

hp_arr=(${hp//,/ })

for cur_hp in ${hp_arr[@]}; do

    param_a=${hp%-*}
    param_b=${hp#*-}


    if [[ ${stage} -le 1 ]]; then

       mkdir -p ${prs_path}/prscs/ || true
       cd $PRS_TOOLS/PRScs/

       $PRS_CODEBASE/../prs-python2/bin/python $PRS_TOOLS/PRScs/PRScs.py \
         --ref_dir=$ELKON_SCRATCH/PRScs_LD/ldblk_1kg_eur \
         --bim_prefix=${imp_train_path}${ds_prefix}${train_suffix} \
         --sst_file=${discovery_path}gwas_cs.tsv \
         --a=${param_a} \
         --b=${param_b} \
         --n_gwas=100000 \
         --out_dir=${prs_path}prscs/out

       cd $PRS_CODEBASE
    fi

    if [[ ${stage} -le 2 ]]; then
        mkdir -p ${prs_path}prscs/ || true
        rm ${prs_path}prscs/out_all || true
        ls -tr ${prs_path}prscs/out* | xargs -n 100 cat > ${prs_path}prscs/out_all
    fi

    if [[ ${stage} -le 3 ]]; then
                plink --bfile ${imp_test_path}${ds_prefix}${test_suffix}  \
                      --score ${prs_path}/prscs/out_all 2 4 6 \
                      --out ${prs_path}${prs_prefix}${test_suffix}.${cur_hp}
    fi

    if [[ ${stage} -le 4 ]]; then
              Rscript calc_metrics_cv_cs.R --discovery=${discovery} --target=${target} --imp=${imp} \
                                           --suffix=${test_suffix} --rep=${rep} --analysis_type="cv" \
                                           --grid_ids=${cur_hp};
    fi

done