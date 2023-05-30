import argparse
from aggregate_prs_statistics_generic import aggregate_statistics

if __name__=="__main__":

    target="gain"
    method="pt"

    prs_names=["PGC2_noAJ_gain_afr", "D_scz_ripke_2011_gain_afr", "D_scz_ripke_2014_gain_afr", "D_scz_pardinas_2018_gain_afr"]
    imps=["impute2_1kg_eur", "impute2_1kg_afr", "impute2_1kg_gbr", "impute2_1kg_eas"]
    hyperparameters=["0.001", "0.005", "0.01", "0.05", "0.1", "0.2", "0.3", "0.4", "0.5"]

    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-p', '--prs_names', dest='prs_names', help="", default=",".join(prs_names))
    parser.add_argument('-i', '--imps', dest='imps', help="", default=",".join(imps))
    parser.add_argument('-hp', '--hyperparameters', dest='hyperparameters', help="", default=",".join(hyperparameters))

    args = parser.parse_args()
    prs_names=args.prs_names.split(',')
    imps=args.imps.split(',')
    hyperparameters=args.hyperparameters.split(',')

    aggregate_statistics(prs_names, imps, method, hyperparameters, target)
