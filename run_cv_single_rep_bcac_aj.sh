source constants_.sh
source parse_args.sh "$@"

if [[ -z ${folds} ]]; then  folds=5; fi
if [[ -z ${discovery} ]]; then discovery='bcac_onco_eur-5pcs-country'; fi
if [[ -z ${target} ]]; then target='bcac_onco_aj'; fi
if [[ -z ${imp} ]]; then imp='impX_new'; fi
if [[ -z ${stage} ]]; then stage=1; fi
if [[ -z ${fold_start}  ]]; then fold_start=1; fi

for fold in `seq ${fold_start} ${folds}`; do
    bash calc_prs_cv_${method}.sh --discovery ${discovery} --target ${target} --imp ${imp} --cv ${fold}_${folds} --stage ${stage} --rep ${rep};
done