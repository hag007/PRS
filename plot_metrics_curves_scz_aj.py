import argparse
from plot_metrics_curves_generic import plot_curves

if __name__=='__main__':

    target="scz_aj"

    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-p', '--prs_names', dest='prs_names', help="", default="")
    parser.add_argument('-i', '--imps', dest='imps', help="", default="")
    parser.add_argument('-m', '--metric_name', dest='metric_name', help="", default="or_all")
    parser.add_argument('-fn', '--file_name_format', dest='file_name_format', help="", default="prs.or_summary_{}.tsv") # prs.statistics_summary_{}.tsv

    args = parser.parse_args()
    prs_names=args.prs_names.split(',')
    imps=args.imps.split(',')
    metric_name = args.metric_name
    fname = "prs.mono.pt.or_summary_scz_aj.tsv"#args.file_name_format.format(target)
    field_name=metric_name

    imps=["impute2_1kg_eur2", "impute2_1kg_eas2", "impute2_1kg_afr2", "impute2_ajkg14_t101"]
    plot_curves(metric_name, fname, field_name, prs_names=None, imps=imps, out_suffix=f"{target}_{metric_name}_super_pop")

    imps=["impute2_1kg_ceu2", "impute2_1kg_gbr2", "impute2_1kg_fin2", "impute2_1kg_tsi2", "impute2_1kg_ibs2", "impute2_ajkg14_t101"]
    plot_curves(metric_name, fname, field_name, prs_names=None, imps=imps, out_suffix=f"{target}_{metric_name}_pop")

