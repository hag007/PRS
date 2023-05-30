import argparse
from aggregate_prs_statistics_generic import aggregate_statistics

if __name__=="__main__":

    target="ukb"
    method="pt"

    prs_names_ukb_eur=["UKB_t2d_eur_ukbb_afr", "UKB_t2d_eur_ukbb_sas", "UKB_osar_eur_ukbb_afr", "UKB_osar_eur_ukbb_sas", "UKB_hfvr_eur_ukbb_afr", "UKB_hfvr_eur_ukbb_sas", "UKB_chol_eur_ukbb_afr", "UKB_chol_eur_ukbb_sas", "UKB_ht_eur_ukbb_afr", "UKB_ht_eur_ukbb_sas", "UKB_ast_eur_ukbb_afr", "UKB_ast_eur_ukbb_sas", "UKB_height_eur_ukbb_afr", "UKB_height_eur_ukbb_sas", "UKB_hyty_eur_ukbb_afr", "UKB_hyty_eur_ukbb_sas", "UKB_gerx_eur_ukbb_afr", "UKB_gerx_eur_ukbb_sas", "UKB_madd_eur_ukbb_afr", "UKB_madd_eur_ukbb_sas", "UKB_angna_eur_ukbb_afr", "UKB_angna_eur_ukbb_sas", "UKB_utfi_eur_ukbb_afr", "UKB_utfi_eur_ukbb_sas", "UKB_ctrt_eur_ukbb_afr", "UKB_ctrt_eur_ukbb_sas"]
    prs_names_gbr=["UKB_t2d_gbr_ukbb_afr", "UKB_t2d_gbr_ukbb_sas", "UKB_osar_gbr_ukbb_afr", "UKB_osar_gbr_ukbb_sas", "UKB_hfvr_gbr_ukbb_afr", "UKB_hfvr_gbr_ukbb_sas", "UKB_chol_gbr_ukbb_afr", "UKB_chol_gbr_ukbb_sas", "UKB_ht_gbr_ukbb_afr", "UKB_ht_gbr_ukbb_sas", "UKB_ast_gbr_ukbb_afr", "UKB_ast_gbr_ukbb_sas", "UKB_height_gbr_ukbb_afr", "UKB_height_gbr_ukbb_sas", "UKB_hyty_gbr_ukbb_afr", "UKB_hyty_gbr_ukbb_sas", "UKB_gerx_gbr_ukbb_afr", "UKB_gerx_gbr_ukbb_sas", "UKB_madd_gbr_ukbb_afr", "UKB_madd_gbr_ukbb_sas", "UKB_angna_gbr_ukbb_afr", "UKB_angna_gbr_ukbb_sas", "UKB_utfi_gbr_ukbb_afr", "UKB_utfi_gbr_ukbb_sas", "UKB_ctrt_gbr_ukbb_afr", "UKB_ctrt_gbr_ukbb_sas"]
    prs_names_public=["D2_chol_willer_2013_ukbb_sas", "D2_chol_willer_2013_ukbb_afr", "D2_sysp_evangelou_2018_ukbb_sas", "D2_sysp_evangelou_2018_ukbb_afr", "D2_dias_evangelou_2018_ukbb_afr", "D2_dias_evangelou_2018_ukbb_sas",  "UKB_ht_EUR_ukbb_afr", "UKB_ht_EUR_ukbb_sas", "D2_asth_zhu_2019_ukbb_sas", "D2_asth_zhu_2019_ukbb_afr", "UKB_ast_EUR_ukbb_sas", "UKB_ast_EUR_ukbb_afr", "D_t2d_mahajan_2018_ukbb_afr", "D_t2d_mahajan_2018_ukbb_sas","D2_t2di_mahajan_2018_ukbb_sas", "D2_t2di_mahajan_2018_ukbb_afr", "D2_hdlp_willer_2013_ukbb_sas", "D2_hdlp_willer_2013_ukbb_afr", "D2_ldlp_willer_2013_ukbb_sas", "D2_ldlp_willer_2013_ukbb_afr", "D2_hght_yengo_2018_ukbb_afr", "D2_hght_yengo_2018_ukbb_sas", "D2_gerx_an_2019_ukbb_afr", "D2_gerx_an_2019_ukbb_sas", "D2_madd_howard_2019_ukbb_afr", "D2_madd_howard_2019_ukbb_sas", "GC_utfi_morton_2019_ukbb_afr"]
    prs_names=prs_names_ukb_eur+prs_names_gbr+prs_names_public

    imps=["impute2_1kg_eur100", "impute2_1kg_eur100-minus-gbr", "impute2_1kg_eur-minus-gbr", "impute2_1kg_ibs", "impute2_1kg_gbr", "impute2_1kg_eur", "impute2_1kg_afr", "impute2_1kg_sas", "imputeX_new"]

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
