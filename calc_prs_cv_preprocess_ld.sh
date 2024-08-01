#!/bin/bash

source constants_.sh
source parse_args.sh "$@"

source init_args_cv.sh

prs_prefix="prs.cv.ld__${pop}"
prs_prefix_adapter="prs.cv.ld_${pheno}_${pop}"
ds_prefix="ds__${pop}"

mkdir -p ${prs_path}ldpred || true

if [[ ! -f ${imp_train_path}${ds_prefix}${train_suffix}.bim ]]; then
    echo "${imp_train_path}${ds_prefix}${train_suffix}.bim" does not exists. Skipping...
    exit 0
fi

if [[ ${stage} -le 1 ]]; then
          echo "Rscript ldpred_preprocess.R --discovery=${discovery} --target=${target} --imp=${imp} --train_suffix=${train_suffix} --test_suffix=${test_suffix} --rep=${rep} --analysis_type="cv";"
    	    Rscript ldpred_preprocess.R --discovery=${discovery} --target=${target} --imp=${imp} \
    	                     --train_suffix=${train_suffix} --test_suffix=${test_suffix} \
    	                     --rep=${rep} --analysis_type="cv";
fi

