import os
import constants
import pandas as pd
import argparse
from aggregate_prs_statistics_generic import aggregate_statistics


if __name__=="__main__":

    target="hadassa_brca"
    method="pt2"

    prs_names=["bcac_onco_eur-5pcs_hadassa_brca"]
    imps=[ "impute2_1kg_eur", "impute2_1kg_eur2" , "impute2_ajkg14_t101"]

    hyperparameters=["0.00000005", "0.0000001", "0.000001", "0.00001", "0.0001", "0.001", "0.005", "0.01", "0.05", "0.1", "0.2", "0.3", "0.4", "0.5"]

    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-p', '--prs_names', dest='prs_names', help="", default=",".join(prs_names))
    parser.add_argument('-i', '--imps', dest='imps', help="", default=",".join(imps))
    parser.add_argument('-hp', '--hyperparameters', dest='hyperparameters', help="", default=",".join(hyperparameters))

    args = parser.parse_args()
    prs_names=args.prs_names.split(',')
    imps=args.imps.split(',')
    hyperparameters=args.hyperparameters.split(',')

    aggregate_statistics(prs_names, imps, method, hyperparameters, target, type='cross', target_cross='bcac_onco_aj', imp_cross='impX_new')
