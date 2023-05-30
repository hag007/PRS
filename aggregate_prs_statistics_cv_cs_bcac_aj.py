import argparse
from aggregate_prs_statistics_cv_generic import aggregate_statistics_cv

if __name__=="__main__":

    target="bcac_aj"
    method="cs"

    prs_names=["D_bca_michailidou_2017_bcac_onco_aj", "UKB_bc_eur_bcac_onco_aj", "bcac_onco_eur_bcac_onco_aj", "bcac_onco_eur-minus-outliers_bcac_onco_aj", "bcac_onco_eur-1pcs_bcac_onco_aj", "bcac_onco_eur-2pcs_bcac_onco_aj", "bcac_onco_eur-3pcs_bcac_onco_aj", "bcac_onco_eur-4pcs_bcac_onco_aj", "bcac_onco_eur-5pcs_bcac_onco_aj", "bcac_onco_eur-6pcs_bcac_onco_aj", "bcac_onco_eur-3pcs2_bcac_onco_aj" , "bcac_onco_eur-5pcs_ukbb_eur"]
    imps=["impX", "impX_new", "imputeX_new"]

    hyperparameters=["0.1"]

    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-p', '--prs_names', dest='prs_names', help="", default=",".join(prs_names))
    parser.add_argument('-i', '--imps', dest='imps', help="", default=",".join(imps))
    parser.add_argument('-hp', '--hyperparameters', dest='hyperparameters', help="", default=",".join(hyperparameters))
    parser.add_argument('-fn', '--file_name_format', dest='file_name_format', help="", default="prs.cs.cv.or_summary_{}.tsv")
    parser.add_argument('-c', '--cv_folds', dest='cv_folds', help="", default="5")
    parser.add_argument('-r', '--rep', dest='rep', help="", default="10")

    args = parser.parse_args()
    prs_names=args.prs_names.split(',')
    imps=args.imps.split(',')
    hyperparameters=args.hyperparameters.split(',')
    cv_folds=int(args.cv_folds)
    rep=int(args.rep)

    suffix=target
    if rep:
        suffix+=f'_{rep}'
    aggregate_statistics_cv(prs_names, imps, method, hyperparameters, cv_folds, rep, f'{target}_{rep}')
