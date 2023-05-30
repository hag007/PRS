import argparse
from plot_metrics_curves_generic import plot_curves

if __name__=='__main__':

    target="bcac_aj"

    prs_names=[a.format("aj") for a in ["D_bca_michailidou_2017_bcac_onco_{}", "UKB_bc_eur_bcac_onco_{}", "bcac_onco_eur_bcac_onco_{}", "bcac_onco_eur-minus-outliers_bcac_onco_{}", "bcac_onco_eur-1pcs_bcac_onco_{}", "bcac_onco_eur-2pcs_bcac_onco_{}", "bcac_onco_eur-3pcs_bcac_onco_{}", "bcac_onco_eur-4pcs_bcac_onco_{}", "bcac_onco_eur-5pcs_bcac_onco_{}", "bcac_onco_eur-6pcs_bcac_onco_{}", "bcac_onco_eur-3pcs2_bcac_onco_{}"]] + ["bcac_onco_eur-5pcs_ukbb_eur"]
    imps=[ "impute2_1kg_eur2", "impute2_ajkg14_t101" , "impX"] #  , "impute2_1kg_afr2", "impute2_1kg_eas2", "imputeX_new", ] #, "impute2_1kg_eas"]

    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-p', '--prs_names', dest='prs_names', help="", default=",".join(prs_names))
    parser.add_argument('-i', '--imps', dest='imps', help="", default=",".join(imps))
    parser.add_argument('-m', '--metric_name', dest='metric_name', help="", default="or_all")
    parser.add_argument('-fn', '--file_name_format', dest='file_name_format', help="", default="prs.or_summary_{}.tsv") # prs.statistics_summary_{}.tsv

    args = parser.parse_args()
    prs_names=args.prs_names.split(',')
    imps=args.imps.split(',')
    metric_name = args.metric_name
    fname = args.file_name_format.format(target)
    field_name=metric_name

    plot_curves(metric_name, fname, field_name, prs_names=prs_names, imps=imps, out_suffix=f"{target}_{metric_name}")

