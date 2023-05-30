#!/bin/bash

source constants_.sh
source parse_args.sh "$@"

source init_args_cv.sh

prs_prefix="prs.cv.ld_${pop}_${pheno}"
ds_prefix="ds_${pop}_${pheno}"

mkdir -p ${prs_path}ldpred || true

if [[ ${stage} -le 1 ]]; then
          echo "Rscript ldpred.R --discovery=${discovery} --target=${target} --imp=${imp} --train_suffix=${train_suffix} --test_suffix=${test_suffix} --rep=${rep} --analysis_type="cv";"
    	    Rscript ldpred.R --discovery=${discovery} --target=${target} --imp=${imp} \
    	                     --train_suffix=${train_suffix} --test_suffix=${test_suffix} \
    	                     --rep=${rep} --analysis_type="cv";
fi

if [[ ${stage} -le 2 ]]; then
    for cur_hp in {1..102}; do
        if [[ -f ${prs_path}ldpred/${prs_prefix}${train_suffix}.${cur_hp}.weights ]]; then
            plink --bfile ${imp_test_path}${ds_prefix}${test_suffix}  \
                  --score ${prs_path}ldpred/${prs_prefix}${train_suffix}.${cur_hp}.weights 2 5 6 \
                  --exclude ${imp_test_path}ds.dupvar \
                  --out ${prs_path}${prs_prefix}${test_suffix}.${cur_hp}
        fi
    done
fi

if [[ ${stage} -le 3 ]]; then
     	    Rscript calc_metrics_cv_ld.R --discovery=${discovery} --target=${target} --imp=${imp} \
     	                                 --suffix=${test_suffix} --rep=${rep} --analysis_type="cv";

fi
