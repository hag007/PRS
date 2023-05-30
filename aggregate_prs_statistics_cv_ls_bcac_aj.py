import argparse
from aggregate_prs_statistics_cv_generic import aggregate_statistics_cv

if __name__=="__main__":

    target="bcac_aj"
    method="ls"

    prs_names=["bcac_onco_eur-5pcs-country_bcac_onco_aj"]
    imps=["impX", "impX_new", "imputeX_new"]

    hyperparameters=[f'{a}-{b}' for a in [0.2,0.5,0.9,1] for b in range(1,21)]

    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-p', '--prs_names', dest='prs_names', help="", default=",".join(prs_names))
    parser.add_argument('-i', '--imps', dest='imps', help="", default=",".join(imps))
    parser.add_argument('-hp', '--hyperparameters', dest='hyperparameters', help="", default=",".join(hyperparameters))
    parser.add_argument('-fn', '--file_name_format', dest='file_name_format', help="", default="prs.ls.cv.or_summary_{}.tsv")
    parser.add_argument('-c', '--cv_folds', dest='cv_folds', help="", default="5")
    parser.add_argument('-r', '--rep', dest='rep', help="", default="10")

    args = parser.parse_args()
    prs_names=args.prs_names.split(',')
    imps=args.imps.split(',')
    hyperparameters=args.hyperparameters.split(',')
    cv_folds=int(args.cv_folds)
    rep=args.rep

    suffix=target
    if rep:
        suffix+=f'_{rep}'
    aggregate_statistics_cv(prs_names, imps, method, hyperparameters, cv_folds, rep, f'{target}_{rep}')
