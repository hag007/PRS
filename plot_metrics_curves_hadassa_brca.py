import argparse
from plot_metrics_curves_generic import plot_curves

if __name__=='__main__':

    target="hadassa_brca"

    prs_names=["bcac_onco_eur-5pcs_hadassa_brca"]
    imps=[ "impute2_1kg_eur", "impute2_1kg_eur2", "impute2_ajkg14_t101"]

    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-p', '--prs_names', dest='prs_names', help="", default=",".join(prs_names))
    parser.add_argument('-i', '--imps', dest='imps', help="", default=",".join(imps))
    parser.add_argument('-m', '--metric_name', dest='metric_name', help="", default="or_all")
    parser.add_argument('-fn', '--file_name_format', dest='file_name_format', help="", default="prs.pt.or_summary_{}.tsv") # prs.statistics_summary_{}.tsv

    args = parser.parse_args()
    prs_names=args.prs_names.split(',')
    imps=args.imps.split(',')
    metric_name = args.metric_name
    fname = args.file_name_format.format(target)
    field_name=metric_name

    plot_curves(metric_name, fname, field_name, prs_names=prs_names, imps=imps, out_suffix=f"{target}_{metric_name}")

