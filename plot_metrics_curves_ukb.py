import argparse
from plot_metrics_curves_generic import plot_curves

if __name__=='__main__':

    target="ukb"

    prs_names=[a.format("aj") for a in ["D_bca_michailidou_2017_bcac_onco_{}", "UKB_bc_eur_bcac_onco_{}", "bcac_onco_eur_bcac_onco_{}", "bcac_onco_eur-minus-outliers_bcac_onco_{}", "bcac_onco_eur-1pcs_bcac_onco_{}", "bcac_onco_eur-2pcs_bcac_onco_{}", "bcac_onco_eur-3pcs_bcac_onco_{}", "bcac_onco_eur-4pcs_bcac_onco_{}", "bcac_onco_eur-5pcs_bcac_onco_{}", "bcac_onco_eur-6pcs_bcac_onco_{}", "bcac_onco_eur-3pcs2_bcac_onco_{}"]] + ["bcac_onco_eur-5pcs_ukbb_eur"]
    imps=[ "impute2_1kg_eur2", "impute2_ajkg14_t101" , "impX"] #  , "impute2_1kg_afr2", "impute2_1kg_eas2", "imputeX_new", ] #, "impute2_1kg_eas"]

    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-p', '--prs_names', dest='prs_names', help="", default=",".join(prs_names))
    parser.add_argument('-i', '--imps', dest='imps', help="", default=",".join(imps))
    parser.add_argument('-m', '--metric_name', dest='metric_name', help="", default="or_all")
    parser.add_argument('-fn', '--file_name_format', dest='file_name_format', help="", default="prs.or_summary_{}.tsv") # prs.statistics_summary_{}.tsv

    args = parser.parse_args()
    prs_names=args.prs_names.split(',')
    imps=args.imps.split(',')
    metric_name = args.metric_name
    fname = args.file_name_format.format(target)
    field_name=metric_name

    prs_names=[a.format("afr") for a in ["UKB_t2d_eur_ukbb_{}", "UKB_osar_eur_ukbb_{}", "UKB_hfvr_eur_ukbb_{}", "UKB_chol_eur_ukbb_{}", "UKB_ht_eur_ukbb_{}", "UKB_ast_eur_ukbb_{}",  "UKB_gerx_eur_ukbb_{}", "UKB_madd_eur_ukbb_{}", "UKB_angna_eur_ukbb_{}", "UKB_utfi_eur_ukbb_{}", "UKB_ctrt_eur_ukbb_{}"]] # "UKB_hyty_eur_ukbb_{}",
    imps=["impute2_1kg_sas", "impute2_1kg_eur", "impute2_1kg_afr", "impute2_1kg_gbr", "impute2_1kg_ibs", "impute2_1kg_eur-minus-gbr", "impute2_1kg_eur100", "impute2_1kg_eur100-minus-gbr"] # , "imputeX_new"]
    plot_curves(metric_name, fname, field_name, prs_names=prs_names, imps=imps, out_suffix="ukb_eur_afr")

    prs_names=[a.format("afr") for a in ["UKB_t2d_gbr_ukbb_{}", "UKB_osar_gbr_ukbb_{}", "UKB_hfvr_gbr_ukbb_{}", "UKB_chol_gbr_ukbb_{}", "UKB_ht_gbr_ukbb_{}", "UKB_ast_gbr_ukbb_{}" , "UKB_hyty_gbr_ukbb_{}", "UKB_gerx_gbr_ukbb_{}", "UKB_madd_gbr_ukbb_{}", "UKB_angna_gbr_ukbb_{}", "UKB_utfi_gbr_ukbb_{}", "UKB_ctrt_gbr_ukbb_{}"]]
    imps=["impute2_1kg_sas", "impute2_1kg_eur", "impute2_1kg_afr", "impute2_1kg_gbr", "impute2_1kg_ibs", "impute2_1kg_eur-minus-gbr", "impute2_1kg_eur100", "impute2_1kg_eur100-minus-gbr"] # , "imputeX_new"]
    plot_curves(metric_name, fname, field_name, prs_names=prs_names, imps=imps, out_suffix="ukb_gbr_afr")

    prs_names=[a.format("afr") for a in ["D2_chol_willer_2013_ukbb_{}", "D2_sysp_evangelou_2018_ukbb_{}", "D2_dias_evangelou_2018_ukbb_{}", "D2_asth_zhu_2019_ukbb_{}", "D2_ldlp_willer_2013_ukbb_{}", "D2_t2di_mahajan_2018_ukbb_{}", "D2_gerx_an_2019_ukbb_{}", "D2_madd_howard_2019_ukbb_{}", "GC_utfi_morton_2019_ukbb_{}"]] # "D2_hdlp_willer_2013_ukbb_{}" "D2_t2di_mahajan_2018_ukbb_{}"
    imps=["impute2_1kg_sas", "impute2_1kg_eur", "impute2_1kg_afr", "impute2_1kg_gbr", "impute2_1kg_eur-minus-gbr", "impute2_1kg_eur100", "impute2_1kg_eur100-minus-gbr"] # , "impute2_1kg_ibs"] # , "imputeX_new"]
    plot_curves(metric_name, fname, field_name, prs_names=prs_names, imps=imps, out_suffix="public_afr")


    prs_names=[a.format("sas") for a in ["UKB_t2d_eur_ukbb_{}", "UKB_osar_eur_ukbb_{}", "UKB_hfvr_eur_ukbb_{}", "UKB_chol_eur_ukbb_{}", "UKB_ht_eur_ukbb_{}", "UKB_ast_eur_ukbb_{}", "UKB_hyty_eur_ukbb_{}", "UKB_gerx_eur_ukbb_{}", "UKB_madd_eur_ukbb_{}", "UKB_angna_eur_ukbb_{}", "UKB_ctrt_eur_ukbb_{}"]] # , "UKB_utfi_eur_ukbb_{}"
    imps=["impute2_1kg_sas", "impute2_1kg_eur", "impute2_1kg_afr", "impute2_1kg_gbr", "impute2_1kg_ibs", "impute2_1kg_eur-minus-gbr", "impute2_1kg_eur100", "impute2_1kg_eur100-minus-gbr"] # , "imputeX_new"]
    plot_curves(metric_name, fname, field_name, prs_names=prs_names, imps=imps, out_suffix="ukb_eur_sas")

    prs_names=[a.format("sas") for a in ["UKB_t2d_gbr_ukbb_{}", "UKB_osar_gbr_ukbb_{}", "UKB_hfvr_gbr_ukbb_{}", "UKB_chol_gbr_ukbb_{}", "UKB_ht_gbr_ukbb_{}", "UKB_ast_gbr_ukbb_{}" , "UKB_hyty_gbr_ukbb_{}", "UKB_gerx_gbr_ukbb_{}", "UKB_madd_gbr_ukbb_{}", "UKB_angna_gbr_ukbb_{}", "UKB_utfi_gbr_ukbb_{}", "UKB_ctrt_gbr_ukbb_{}"]]
    imps=["impute2_1kg_sas", "impute2_1kg_eur", "impute2_1kg_afr", "impute2_1kg_gbr", "impute2_1kg_ibs", "impute2_1kg_eur-minus-gbr", "impute2_1kg_eur100", "impute2_1kg_eur100-minus-gbr"] # , "imputeX_new"]
    plot_curves(metric_name, fname, field_name, prs_names=prs_names, imps=imps, out_suffix="ukb_gbr_sas")

    prs_names=[a.format("sas") for a in ["D2_chol_willer_2013_ukbb_{}", "D2_sysp_evangelou_2018_ukbb_{}", "D2_dias_evangelou_2018_ukbb_{}", "D2_asth_zhu_2019_ukbb_{}", "D2_ldlp_willer_2013_ukbb_{}", "D2_t2di_mahajan_2018_ukbb_{}", "D2_gerx_an_2019_ukbb_{}", "D2_madd_howard_2019_ukbb_{}"]] # "D2_hdlp_willer_2013_ukbb_{}" , "D2_t2di_mahajan_2018_ukbb_{}"] ]
    imps=["impute2_1kg_sas", "impute2_1kg_eur", "impute2_1kg_afr", "impute2_1kg_gbr", "impute2_1kg_eur-minus-gbr", "impute2_1kg_eur100", "impute2_1kg_eur100-minus-gbr"] # , "impute2_1kg_ibs"] # , "imputeX_new"]
    plot_curves(metric_name, fname, field_name, prs_names=prs_names, imps=imps, out_suffix="public_sas")


    prs_names=[c for b in [[a.format("eur","afr"),a.format("eur","sas"),a.format("gbr","afr"),a.format("gbr","sas")] for a in ["UKB_t2d_{}_ukbb_{}", "UKB_osar_{}_ukbb_{}", "UKB_hfvr_{}_ukbb_{}", "UKB_chol_{}_ukbb_{}", "UKB_ht_{}_ukbb_{}", "UKB_ast_{}_ukbb_{}", "UKB_hyty_{}_ukbb_{}", "UKB_gerx_{}_ukbb_{}", "UKB_madd_{}_ukbb_{}", "UKB_angna_{}_ukbb_{}", "UKB_utfi_{}_ukbb_{}", "UKB_ctrt_{}_ukbb_{}"]] for c in b] # "D2_hdlp_willer_2013_ukbb_{}" , "D2_t2di_mahajan_2018_ukbb_{}"] ]
    imps=["impute2_1kg_eur", "impute2_1kg_gbr", "impute2_1kg_ibs", "impute2_1kg_eur-minus-gbr", "impute2_1kg_eur100", "impute2_1kg_eur100-minus-gbr"] # , "imputeX_new"]
    plot_curves(metric_name, fname, field_name, prs_names=prs_names, imps=imps, out_suffix="ukb_all", cols=4)


    prs_names=[c for b in [[a.format("gbr","afr"),a.format("gbr","sas")] for a in ["UKB_t2d_{}_ukbb_{}", "UKB_osar_{}_ukbb_{}", "UKB_hfvr_{}_ukbb_{}", "UKB_chol_{}_ukbb_{}", "UKB_ht_{}_ukbb_{}", "UKB_ast_{}_ukbb_{}", "UKB_hyty_{}_ukbb_{}", "UKB_gerx_{}_ukbb_{}", "UKB_madd_{}_ukbb_{}", "UKB_angna_{}_ukbb_{}", "UKB_utfi_{}_ukbb_{}", "UKB_ctrt_{}_ukbb_{}"]] for c in b] # "D2_hdlp_willer_2013_ukbb_{}" , "D2_t2di_mahajan_2018_ukbb_{}"] ]
    imps=["impute2_1kg_eur", "impute2_1kg_gbr", "impute2_1kg_ibs", "impute2_1kg_eur-minus-gbr", "impute2_1kg_eur100", "impute2_1kg_eur100-minus-gbr"] # , "imputeX_new"]
    plot_curves(metric_name, fname, field_name, prs_names=prs_names, imps=imps, out_suffix="ukb_gbr_all", cols=4)

    prs_names=[c for b in [[a.format("eur","afr"),a.format("eur","sas")] for a in ["UKB_t2d_{}_ukbb_{}", "UKB_osar_{}_ukbb_{}", "UKB_hfvr_{}_ukbb_{}", "UKB_chol_{}_ukbb_{}", "UKB_ht_{}_ukbb_{}", "UKB_ast_{}_ukbb_{}", "UKB_hyty_{}_ukbb_{}", "UKB_gerx_{}_ukbb_{}", "UKB_madd_{}_ukbb_{}", "UKB_angna_{}_ukbb_{}", "UKB_utfi_{}_ukbb_{}", "UKB_ctrt_{}_ukbb_{}"]] for c in b] # "D2_hdlp_willer_2013_ukbb_{}" , "D2_t2di_mahajan_2018_ukbb_{}"] ]
    imps=["impute2_1kg_eur", "impute2_1kg_gbr", "impute2_1kg_ibs", "impute2_1kg_eur-minus-gbr", "impute2_1kg_eur100", "impute2_1kg_eur100-minus-gbr"] # , "imputeX_new"]
    plot_curves(metric_name, fname, field_name, prs_names=prs_names, imps=imps, out_suffix="ukb_eur_all", cols=4)

