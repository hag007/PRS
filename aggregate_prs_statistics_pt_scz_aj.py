import argparse
from aggregate_prs_statistics_generic import aggregate_statistics
if __name__=="__main__":

    target="scz_aj"
    method="pt"

    prs_names=["PGC2_noAJ_dbg-scz19"]
    ths=["0.00000005", "0.0000001", "0.000001", "0.00001", "0.001", "0.001", "0.001", "0.005", "0.01", "0.05", "0.1", "0.2", "0.3", "0.4", "0.5"]

    imps_pop = [f"impute2_1kg_{a}2" for a in ["tsi", "ibs", "gbr", "fin", "ceu"]]+["impute2_1kg_ceu-gbr2"]
    pop_aj=["impute2_ajkg14_t101"]
    pop_eur=["impute2_1kg_eur2", "impute2_1kg_eur-ajkg14-t101-merged"]
    pop_kdv=["impute2_1kg_kdv2"]
    pop_eas=["impute2_1kg_eas2"]
    pop_afr=["impute2_1kg_afr2"]
    imps_minus = [f"impute2_1kg_eur-minus-{a}2" for a in ["tsi", "ibs", "gbr", "fin", "ceu"]]
    imps_merged = [f"impute2_1kg_eur-minus-{a}-ajkg14-t101-merged" for a in ["tsi", "ibs", "gbr", "fin", "ceu"]]
    imps_combined = [] # [f"impute2_1kg_eur-minus-{a}-aj-snps_ajkg14_t101" for a in ["tsi", "ibs", "gbr", "fin", "ceu"]]

    # imps_pop = [f"impute2_1kg_{a}" for a in ["tsi", "ibs", "gbr", "fin", "ceu"]]
    # pop_aj=["impute2_ajkg14_t101"]
    # pop_eur=["impute2_1kg_eur", "impute2_1kg_eur-ajkg14-t101-merged"]
    # pop_kdv=["impute2_1kg_kdv"]
    # imps_minus = [f"impute2_1kg_eur-minus-{a}-aj-snps" for a in ["tsi", "ibs", "gbr", "fin", "ceu"]]
    # imps_merged = [f"impute2_1kg_eur-minus-{a}-ajkg14-t101-merged" for a in ["tsi", "ibs", "gbr", "fin", "ceu"]]
    # imps_combined = [f"impute2_1kg_eur-minus-{a}-aj-snps_ajkg14_t101" for a in ["tsi", "ibs", "gbr", "fin", "ceu"]]

    imps=imps_pop+pop_aj+pop_eur+pop_kdv+imps_minus+imps_merged+imps_combined+pop_eas+pop_afr

    hyperparameters=["0.00000005","0.0000001","0.000001","0.00001","0.0001","0.001", "0.001", "0.005", "0.01", "0.05", "0.1", "0.2", "0.3", "0.4", "0.5"]

    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-p', '--prs_names', dest='prs_names', help="", default=",".join(prs_names))
    parser.add_argument('-i', '--imps', dest='imps', help="", default=",".join(imps))
    parser.add_argument('-hp', '--hyperparameters', dest='hyperparameters', help="", default=",".join(hyperparameters))


    args = parser.parse_args()
    prs_names=args.prs_names.split(',')
    imps=args.imps.split(',')
    hyperparameters=args.hyperparameters.split(',')

    aggregate_statistics(prs_names, imps, method, hyperparameters, target)

