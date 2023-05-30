import argparse
from aggregate_prs_statistics_generic import aggregate_statistics

if __name__=="__main__":

    target="bcac_aj"
    method="ld"

    prs_names=["bcac_onco_eur-5pcs-country_bcac_onco_aj"] # ["D_bca_michailidou_2017_bcac_onco_aj", "UKB_bc_eur_bcac_onco_aj", "bcac_onco_eur_bcac_onco_aj", "bcac_onco_eur-minus-outliers_bcac_onco_aj", "bcac_onco_eur-1pcs_bcac_onco_aj", "bcac_onco_eur-2pcs_bcac_onco_aj", "bcac_onco_eur-3pcs_bcac_onco_aj", "bcac_onco_eur-4pcs_bcac_onco_aj", "bcac_onco_eur-5pcs_bcac_onco_aj", "bcac_onco_eur-6pcs_bcac_onco_aj", "bcac_onco_eur-3pcs2_bcac_onco_aj" , "bcac_onco_eur-5pcs_ukbb_eur"]
    imps=["impX_new"] # ["impute2_ajkg14_t101", "impX", "imputeX_new", "impX_new", "impX_gf", "impute2_1kg_eur2", "impute2_1kg_eas2", "impute2_1kg_afr2"]
    hyperparameters=[str(a) for a in range(1,103)]

    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-p', '--prs_names', dest='prs_names', help="", default=",".join(prs_names))
    parser.add_argument('-i', '--imps', dest='imps', help="", default=",".join(imps))
    parser.add_argument('-hp', '--hyperparameters', dest='hyperparameters', help="", default=",".join(hyperparameters))

    args = parser.parse_args()
    prs_names=args.prs_names.split(',')
    imps=args.imps.split(',')
    hyperparameters=args.hyperparameters.split(',')

    aggregate_statistics(prs_names, imps, method, hyperparameters, target)
