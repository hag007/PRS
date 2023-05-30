import os
import constants
import pandas as pd
import argparse
from aggregate_prs_statistics_generic import aggregate_statistics


if __name__=="__main__":

    target="hadassa_brca"
    method="ls"

    prs_names=["bcac_onco_eur-5pcs_hadassa_brca"]
    imps=[ "impute2_1kg_eur"] # , "impute2_1kg_eur2" , "impute2_ajkg14_t101"]

    hyperparameters=[f'{a}-{b}' for a in [0.2,0.5,0.9,1] for b in range(1,21)]

    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-p', '--prs_names', dest='prs_names', help="", default=",".join(prs_names))
    parser.add_argument('-i', '--imps', dest='imps', help="", default=",".join(imps))
    parser.add_argument('-hp', '--hyperparameters', dest='hyperparameters', help="", default=",".join(hyperparameters))
    parser.add_argument('-tc', '--target_cross', dest='target_cross', help="", default="")
    parser.add_argument('-ic', '--imp_cross', dest='imp_cross', help="", default="")

    args = parser.parse_args()
    prs_names=args.prs_names.split(',')
    imps=args.imps.split(',')
    hyperparameters=args.hyperparameters.split(',')
    target_cross=args.target_cross
    imp_cross=args.imp_cross

    aggregate_statistics(prs_names, imps, method, hyperparameters, target, type='cross', target_cross=target_cross, imp_cross=imp_cross)
