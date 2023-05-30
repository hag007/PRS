source constants_.sh
source gwas_pheno_mapper.sh
source parse_args.sh "$@"

if [[ -z ${discoveries} ]]; then
    echo "discovery sets were not provided. Fall back to default..."
    discoveries="D2_sysp_evangelou_2018,D2_dias_evangelou_2018,D2_asth_zhu_2019,D2_chol_willer_2013,D2_ldlp_willer_2013,,D2_t2di_mahajan_2018,D2_gerx_an_2019,D2_madd_howard_2019"
    # discoveries="UKB_ht_eur,UKB_chol_eur,UKB_hfvr_eur,UKB_hyty_eur,UKB_madd_eur,UKB_osar_eur,UKB_t2d_eur,UKB_utfi_eur,UKB_gerx_eur,UKB_angna_eur,UKB_ast_eur,UKB_ctrt_eur"
    echo "discoveries=${discoveries}"
fi
if [[ -z ${targets} ]]; then
    echo "target sets were not provided. Fall back to default..."
    targets="ukbb_afr,ukbb_sas"
    echo "targets=${targets}"
fi
if [[ -z ${imps} ]]; then
    echo "imputation panels were not provided. Fall back to default..."
    imps="original,impute2_1kg_sas,impute2_1kg_afr,impute2_1kg_eur,impute2_1kg_gbr,imputeX_new"
    echo "imps=${imps}"
fi
if [[ -z ${stage} ]]; then stage=1; fi

base_rep=105
folds=5

## aggregate_prs_statistics
if [[ ${stage} -le 1 ]]; then
    for cur_rep in {1..6}; do
        python aggregate_prs_statistics_cv_${method}.py --discoveries ${discoveries} --targets ${targets} --imps ${imps} --rep ${base_rep}_${cur_rep} --suffix ${targets};
    done;
fi

# plot + average results
if [[ ${stage} -le 2 ]]; then
    for cur_rep in {1..6}; do
        python plot_metrics_boxplots_cv_${method}.py --discoveries ${discoveries} --targets ${targets} --imps ${imps} --rep_start ${base_rep}_${cur_rep} --rep_end ${base_rep}_${cur_rep} --suffix ${targets};
        python plot_metrics_boxplots_cv_${method}.py --discoveries ${discoveries} --targets ${targets} --imps ${imps} --rep_start ${base_rep}_${cur_rep} --rep_end ${base_rep}_${cur_rep} --suffix ${targets} --metric or_99;
        # python plot_metrics_boxplots_cv_${method}.py --discoveries ${discoveries} --targets ${targets} --imps ${imps} --rep_start ${base_rep}_${cur_rep} --rep_end ${base_rep}_${cur_rep} --metric or_99;
    done;
fi
