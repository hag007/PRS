import argparse
from plot_metrics_boxplots_cv_generic import plot_boxplot_cv_multi_test

if __name__=='__main__':
    method="ld"
    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-s', '--rep_start', dest='rep_start', help='', default='1')
    parser.add_argument('-e', '--rep_end', dest='rep_end', help="", default='10')
    parser.add_argument('-p', '--prs_names', dest='prs_names', help="", default="bcac_onco_eur-5pcs-country_bcac_onco_aj")
    parser.add_argument('-i', '--imps', dest='imps', help="", default="impX_new")
    parser.add_argument('-m', '--metric_name', dest='metric_name', help="", default="or_all")
    parser.add_argument('-fn', '--file_name_format', dest='file_name_format', help="", default="prs.cv.ld{}.or_summary_bcac_aj{}.tsv")

    args = parser.parse_args()
    rep_start = args.rep_start
    rep_end = args.rep_end
    prs_names=args.prs_names.split(',')
    imps=args.imps.split(',')
    metric_name = args.metric_name
    file_name_format = args.file_name_format
    field_name=metric_name

    hyperparameters=[str(a) for a in range(1,103)]
    plot_boxplot_cv_multi_test(metric_name, file_name_format, field_name, prs_names=prs_names, imps=imps, out_suffix="bcac_aj", rep_start=rep_start, rep_end=rep_end, hyperparameters=hyperparameters)
    # plot_boxplot_cv_single_test(metric_name, file_name_format, field_name, prs_names=prs_names, imps=imps, out_suffix=f"bcac_aj_{metric_name}", rep_start=1, rep_end=1, hyperparameters=ths)





#### Left only for naming purposes ####

    # prs_names= [a.format("aj") for a in ["D_bca_michailidou_2017_bcac_onco_{}", "UKB_bc_eur_bcac_onco_{}", "bcac_onco_eur_bcac_onco_{}", "bcac_onco_eur-minus-outliers_bcac_onco_{}", "bcac_onco_eur-1pcs_bcac_onco_{}", "bcac_onco_eur-2pcs_bcac_onco_{}", "bcac_onco_eur-3pcs_bcac_onco_{}", "bcac_onco_eur-4pcs_bcac_onco_{}", "bcac_onco_eur-5pcs_bcac_onco_{}", "bcac_onco_eur-6pcs_bcac_onco_{}", "bcac_onco_eur-3pcs2_bcac_onco_{}"]] + ["bcac_onco_eur-5pcs_ukbb_eur"]
    # imps=[ "impute2_1kg_eur2", "impute2_ajkg14_t101" , "impX"] #  , "impute2_1kg_afr2", "impute2_1kg_eas2", "imputeX_new", ] #, "impute2_1kg_eas"]
    # metric_name="or_all" # "or_all" # "OR_per_1SD"
    # fname="prs.pt.{}.or_summary_bcac_aj_{}.tsv" # "prs.statistics_summary_ukb.tsv" # "prs.or_summary_bcac_aj.tsv"


# metric_name="ROC_AUC"
# fname="prs.statistics_summary_ukb.tsv" # "prs.or_summary.tsv"
# field_name="roc_auc"
# plot_curves(metric_name, fname, field_name)

# metric_name="R2"
# fname="prs.statistics_summary_ukb.tsv" # "prs.or_summary.tsv"
# field_name="all_ngkR2"
# plot_curves(metric_name, fname, field_name)
   
