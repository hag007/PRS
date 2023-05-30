source constants_.sh
source parse_args.sh "$@"

if [[ -z ${folds} ]]; then folds=5; fi
if [[ -z ${discovery} ]]; then discovery='bcac_onco_eur-5pcs-country'; fi
if [[ -z ${target} ]]; then target='bcac_onco_aj'; fi
if [[ -z ${imp} ]]; then imp='impX_new'; fi 
# stage=1

bash calc_prs_cv_${method}.sh --discovery ${discovery} --target ${target} --imp ${imp} --cv ${folds} --stage ${stage} --rep ${rep}
