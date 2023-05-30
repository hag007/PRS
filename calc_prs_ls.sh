#!/bin/bash

source constants_.sh
source parse_args.sh "$@"
source init_args_prs.sh

prs_prefix="prs.mono.ls${sub}"
ds_prefix="ds${sub}"

echo "Start pipeline"
mkdir -p $prs_path || echo ""
mkdir -p $rep_path || echo ""
mkdir -p $rep_imp_path || echo ""


if [[ ${stage} -le 1 ]]; then
    	    Rscript lassosum.R ${discovery} ${target} ${imp} "${sub}" ${hp};
fi

if [[ ${stage} -le 2 ]]; then
    	    Rscript calc_metrics_ls.R ${discovery} ${target} ${imp} "${sub}" ${hp} ;
fi

if [[ ${stage} -le 3 ]]; then
    if [[ -f "${datasets_path}${target}/pheno${sub}" ]]; then
            echo Finding the best-fit PRS with binary phenotypes
            Rscript calc_metrics_ls.R --discovery=${discovery} \
            --target_train=${target_train} --imp_train=${imp_train} \
            --target_test=${target_test} --imp_test=${imp_test} \
            --suffix=${suffix} --rep=${rep} --analysis_type="mono";
    else
        echo "No pheno named pheno${sub} was found under ${target}"
    fi
fi

