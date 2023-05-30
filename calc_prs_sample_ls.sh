#!/bin/bash

source constants_.sh
source parse_args.sh "$@"

source init_args_sample.sh

prs_prefix="prs.ls_${pop}_${pheno}"
ds_prefix="ds_${pop}_${pheno}"

# test_suffix="__${test_suffix}"
# train_suffix="__"


mkdir -p ${prs_path}lasso ||  true

if [[ ${stage} -le 1 ]]; then
    	    Rscript lassosum_.R --discovery=${discovery} --target=${target} --imp=${imp} \
    	                       --train_suffix="__" --test_suffix="__${test_suffix}" \
    	                       --sample=${sample} --analysis_type="sample" --hp "0.5-11";
fi


test_suffix="${test_suffix}_sample"

if [[ ${stage} -le 2 ]]; then
    if [[ ${hp} == "" ]]; then
        hp="0.5"
    fi
    hp_arr=(${hp//,/ })

    for cur_hp in ${hp_arr[@]}; do

        for hp2 in {11..11}; do

            plink --bfile ${imp_test_path}${ds_prefix}${test_suffix}  \
                  --score ${prs_path}lasso/${prs_prefix}.${cur_hp}-${hp2}.weights 2 4 6 \
                  --exclude ${imp_test_path}ds.dupvar \
                  --out ${prs_path}${prs_prefix}${test_suffix}.${cur_hp}-${hp2}
        done
    done
fi


if [[ ${stage} -le 3 ]]; then
     	    Rscript calc_metrics_cv_ls.R --discovery=${discovery} --target=${target} --imp=${imp} \
     	                                 --train_suffix=${train_suffix} --test_suffix=${test_suffix}  --analysis_type="sample" --sample=${sample} --smpl=${smpl} --sub="__" ;
fi
