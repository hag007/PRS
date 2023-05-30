import os
import constants
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import mannwhitneyu
import pandas as pd
pd.options.mode.chained_assignment = None
import seaborn as sns
cs = sns.color_palette("bright") + sns.color_palette("pastel")
font = {'size'   : 30}

d_prs_names={'D2_chol_willer_2013':'Cholesterol',
       'D2_sysp_evangelou_2018':'Systolic BP',
       'D2_dias_evangelou_2018':'Diastolic BP',
       'D2_asth_zhu_2019':'Asthma',
       'D_t2d_mahajan_2018':'Type 2 Diabetes (old)',
       'D2_ldlp_willer_2013':'LDL levels',
       'D2_hdlp_willer_2013':'HDL levels',
       'D2_t2di_mahajan_2018':'Type 2 Diabetes',
       'UKB_t2d_eur':'Type 2 Diabetes (EUR-UKB)',
       'UKB_osar_eur':'Osteoarthritis (EUR-UKB)',
       'UKB_hfvr_eur':'Hay fever (EUR-UKB)',
       'UKB_chol_eur':'Cholesterol levels (EUR-UKB)',
       'UKB_ht_eur':'Hypertension (EUR-UKB)',
       'UKB_ast_eur':'Asthma (EUR-UKB)',
       'UKB_t2d_gbr':'Type 2 Diabetes (GBR-UKB)',
       'UKB_osar_gbr':'Osteoarthritis (GBR-UKB)',
       'UKB_hfvr_gbr':'Hay fever (GBR-UKB)',
       'UKB_chol_gbr':'Cholesterol levels (GBR-UKB)',
       'UKB_ht_gbr':'Hypertension (GBR-UKB)',
       'UKB_ast_gbr':'Asthma (GBR-UKB)'
}

d_imp_names={'impute2_1kg_afr':'African',
'impute2_1kg_sas':'South-Asian',
'impute2_1kg_eur':'European (500)',
'impute2_1kg_gbr':'Britain',
'impute2_1kg_ibs':'Spain',
'impute2_1kg_eur-minus-gbr':'European-without-British (400)',
'impute2_1kg_eur100-minus-gbr':'European-without-British (100)',
'impute2_1kg_eur100':'European (100)',
'imputeX_new':'UKB'}

l_imps=["impute2_1kg_eur", "impute2_1kg_sas", "impute2_1kg_afr", "impute2_1kg_gbr", "impute2_1kg_ibs", "impute2_1kg_eur-minus-gbr", "impute2_1kg_eur100", "impute2_1kg_eur100-minus-gbr"]

d_target_names={'ukbb_afr':'African',
'ukbb_sas':'South-Asian',
'ukbb_eur':'European',
'ukbb_gbr':'Britian'}

matplotlib.rc('font', **font)

def plot_curves(metric_name, fname, field_name, prs_names, imps, out_suffix, cols=3):
    df=pd.read_csv(os.path.join(constants.OUTPUT_PATH, fname), sep='\t')

    if imps is None:
        imps=df.loc[:,"imp"].unique()
        imps.sort()

    if prs_names is None:
        prs_names=df.loc[:,"prs_name"].unique()
        prs_names.sort()

    ths=[0.00000005, 0.001,0.005,0.01,0.05,0.1,0.2,0.3,0.4,0.5]
    df_eur_imp=pd.DataFrame()
    df_non_eur_imp=pd.DataFrame()
    df_stats=pd.DataFrame()
    rows=int(np.ceil(len(prs_names)/cols))
    fig, ax = plt.subplots(rows ,cols,figsize=((cols+1)*15, 12*rows))
    df_all=pd.DataFrame()
    for i, prs_name in enumerate(prs_names):   
        prs_title="_".join(prs_name.split("_")[:-2])
        for j, imp in enumerate(imps):
            linestyle="solid" # ("solid" if imp.endswith("eur") else "dotted" if  "imputeX" in imp else "dashed")
            cur_curve=df[(df.loc[:,"imp"]==imp) & (df.loc[:,"prs_name"]==prs_name) & (df.loc[:,"threshold"]>=0.00000005)]
            cur_curve_all=df[(df.loc[:,"imp"]==imp) & (df.loc[:,"prs_name"]==prs_name)]
            if cur_curve.loc[:,field_name].shape[0] >-1:
                ax[i//cols][i % cols].plot(cur_curve.loc[:,"threshold"], cur_curve.loc[:,field_name], label=f'{d_imp_names.get(imp,imp)}', linestyle=linestyle, linewidth=4, color=cs[l_imps.index(imp)])
                df_all.loc[f'{d_prs_names.get(prs_title,prs_title)}/{prs_name.split("_")[-1]}', f'{d_imp_names.get(imp,imp)}']=cur_curve_all.loc[:,field_name].max()
                # new_row=cur_curve.loc[:,field_name]
                # new_row=new_row.to_frame()  
                # new_row.columns=[f'{prs_name}_{imp}']
                # new_row.index=ths
                # new_row.loc["max"]=new_row.max()
                # new_row.loc["prs_name"]=prs_name
                # new_row.loc["imp"]=imp
                # new_row=new_row.T
                # if imp.endswith("eur"):
                #     df_eur_imp=pd.concat((df_eur_imp,new_row))
                # else:
                #     df_non_eur_imp=pd.concat((df_non_eur_imp, new_row))
        target_title="_".join(prs_name.split("_")[-2:])
        ax[i//cols][i % cols].set_title(f'{d_prs_names.get(prs_title,prs_title)}/{d_target_names.get(target_title,target_title)}')
        ax[i//cols][i % cols].set_xlabel("threshold")
        ax[i//cols][i % cols].set_ylabel(" ".join(metric_name.split('_')))

        # df_cur_prs_name_with_metadata=df_non_eur_imp.loc[df_non_eur_imp.loc[:,"prs_name"][df_non_eur_imp.loc[:,"prs_name"]==prs_name].index,ths+["prs_name", "imp"]].copy()
        # eur_row=df_eur_imp.loc[df_eur_imp.loc[:,"prs_name"][df_eur_imp.loc[:,"prs_name"]==prs_name].index,ths+["max"]].values.flatten()
        # if len(list(eur_row))==0:
        #    print(f'Warning: encountered zero-values for PRS {prs_name}')
        #    continue
        # df_stats=pd.concat((df_stats, df_cur_prs_name_with_metadata.apply(lambda row: pd.Series([row["prs_name"], row["imp"], mannwhitneyu(list(row.drop(["prs_name","imp"])), list(eur_row))[1], np.mean(eur_row)-np.mean(row.drop(["prs_name","imp"])), np.max(eur_row)-np.max(row.drop(["prs_name","imp"]))]).to_frame().T,axis=1)))
            
        # df_non_eur_imp.loc[df_non_eur_imp.loc[:,"prs_name"][df_non_eur_imp.loc[:,"prs_name"]==prs_name].index,ths+["max"]]-=eur_row
    # df_stats=pd.concat([pd.DataFrame()]+[a for a in df_stats.iloc[:,0]])
    # df_stats.columns=["prs_name", "imp","mann", "mean_diff", "max_diff"]
    # df_non_eur_imp.loc[:,ths+["max"]]=df_non_eur_imp.loc[:,ths+["max"]]*-1 
    # df_non_eur_imp_bool=df_non_eur_imp.copy()
    # df_non_eur_imp_bool.loc[:,ths+["max"]]=df_non_eur_imp_bool.loc[:,ths+["max"]]>0
    # df_non_eur_imp.to_csv(f"or_diff_{metric_name}_{out_suffix}.tsv", sep='\t')
    # df_non_eur_imp_bool.to_csv(f"or_diff_bool_{metric_name}_{out_suffix}.tsv", sep='\t')

    # df_stats.to_csv(f"stats_{metric_name}_{out_suffix}.tsv", sep='\t')
    plt.subplots_adjust(right=0.7)
    # plt.tight_layout()
    plt.legend(loc=(1.05,0))
    plt.savefig(os.path.join(constants.OUTPUT_PATH, f"{metric_name}_{out_suffix}.png"))
    df_all.to_csv(os.path.join(constants.OUTPUT_PATH, f"{metric_name}_{out_suffix}.tsv"), sep='\t')
    
# metric_name="ROC_AUC"
# fname="prs.statistics_summary_ukb.tsv" # "prs.or_summary.tsv"
# field_name="roc_auc"
# plot_curves(metric_name, fname, field_name)

# metric_name="R2"
# fname="prs.statistics_summary_ukb.tsv" # "prs.or_summary.tsv"
# field_name="all_ngkR2"
# plot_curves(metric_name, fname, field_name)




fname="prs.statistics_summary_ukb.tsv"
field_name="all_R2"
metric_name="all_R2"

prs_names=[a.format("afr") for a in ["UKB_t2d_eur_ukbb_{}", "UKB_osar_eur_ukbb_{}", "UKB_hfvr_eur_ukbb_{}", "UKB_chol_eur_ukbb_{}", "UKB_ht_eur_ukbb_{}", "UKB_ast_eur_ukbb_{}", "UKB_height_eur_ukbb_{}" ]]
imps=["impute2_1kg_sas", "impute2_1kg_eur", "impute2_1kg_afr", "impute2_1kg_gbr", "impute2_1kg_ibs", "impute2_1kg_eur-minus-gbr", "impute2_1kg_eur100", "impute2_1kg_eur100-minus-gbr"] # , "imputeX_new"]
plot_curves(metric_name, fname, field_name, prs_names=prs_names, imps=imps, out_suffix="ukb_eur_afr")

prs_names=[a.format("afr") for a in ["UKB_t2d_gbr_ukbb_{}", "UKB_osar_gbr_ukbb_{}", "UKB_hfvr_gbr_ukbb_{}", "UKB_chol_gbr_ukbb_{}", "UKB_ht_gbr_ukbb_{}", "UKB_ast_gbr_ukbb_{}", "UKB_height_gbr_ukbb_{}" ]]
imps=["impute2_1kg_sas", "impute2_1kg_eur", "impute2_1kg_afr", "impute2_1kg_gbr", "impute2_1kg_ibs", "impute2_1kg_eur-minus-gbr", "impute2_1kg_eur100", "impute2_1kg_eur100-minus-gbr"] # , "imputeX_new"]
plot_curves(metric_name, fname, field_name, prs_names=prs_names, imps=imps, out_suffix="ukb_gbr_afr")

prs_names=[a.format("afr") for a in ["D2_chol_willer_2013_ukbb_{}", "D2_sysp_evangelou_2018_ukbb_{}", "D2_dias_evangelou_2018_ukbb_{}", "D2_asth_zhu_2019_ukbb_{}", "D2_ldlp_willer_2013_ukbb_{}", "D2_t2di_mahajan_2018_ukbb_{}", "D2_hght_yengo_2018_ukbb_{}"]] # "D2_hdlp_willer_2013_ukbb_{}" "D2_t2di_mahajan_2018_ukbb_{}"
imps=["impute2_1kg_sas", "impute2_1kg_eur", "impute2_1kg_afr", "impute2_1kg_gbr", "impute2_1kg_eur-minus-gbr", "impute2_1kg_eur100", "impute2_1kg_eur100-minus-gbr"] # , "impute2_1kg_ibs"] # , "imputeX_new"]
plot_curves(metric_name, fname, field_name, prs_names=prs_names, imps=imps, out_suffix="public_afr")


prs_names=[a.format("sas") for a in ["UKB_t2d_eur_ukbb_{}", "UKB_osar_eur_ukbb_{}", "UKB_hfvr_eur_ukbb_{}", "UKB_chol_eur_ukbb_{}", "UKB_ht_eur_ukbb_{}", "UKB_ast_eur_ukbb_{}", "UKB_height_eur_ukbb_{}" ]]
imps=["impute2_1kg_sas", "impute2_1kg_eur", "impute2_1kg_afr", "impute2_1kg_gbr", "impute2_1kg_ibs", "impute2_1kg_eur-minus-gbr", "impute2_1kg_eur100", "impute2_1kg_eur100-minus-gbr"] # , "imputeX_new"]
plot_curves(metric_name, fname, field_name, prs_names=prs_names, imps=imps, out_suffix="ukb_eur_sas")

prs_names=[a.format("sas") for a in ["UKB_t2d_gbr_ukbb_{}", "UKB_osar_gbr_ukbb_{}", "UKB_hfvr_gbr_ukbb_{}", "UKB_chol_gbr_ukbb_{}", "UKB_ht_gbr_ukbb_{}", "UKB_ast_gbr_ukbb_{}", "UKB_height_gbr_ukbb_{}" ]]
imps=["impute2_1kg_sas", "impute2_1kg_eur", "impute2_1kg_afr", "impute2_1kg_gbr", "impute2_1kg_ibs", "impute2_1kg_eur-minus-gbr", "impute2_1kg_eur100", "impute2_1kg_eur100-minus-gbr"] # , "imputeX_new"]
plot_curves(metric_name, fname, field_name, prs_names=prs_names, imps=imps, out_suffix="ukb_gbr_sas")

prs_names=[a.format("sas") for a in ["D2_chol_willer_2013_ukbb_{}", "D2_sysp_evangelou_2018_ukbb_{}", "D2_dias_evangelou_2018_ukbb_{}", "D2_asth_zhu_2019_ukbb_{}", "D2_ldlp_willer_2013_ukbb_{}", "D2_t2di_mahajan_2018_ukbb_{}", "D2_hght_yengo_2018_ukbb_{}"]] # "D2_hdlp_willer_2013_ukbb_{}" , "D2_t2di_mahajan_2018_ukbb_{}"] ]
imps=["impute2_1kg_sas", "impute2_1kg_eur", "impute2_1kg_afr", "impute2_1kg_gbr", "impute2_1kg_eur-minus-gbr", "impute2_1kg_eur100", "impute2_1kg_eur100-minus-gbr"] # , "impute2_1kg_ibs"] # , "imputeX_new"]
plot_curves(metric_name, fname, field_name, prs_names=prs_names, imps=imps, out_suffix="public_sas")


prs_names=[c for b in [[a.format("eur","afr"),a.format("eur","sas"),a.format("gbr","afr"),a.format("gbr","sas")] for a in ["UKB_t2d_{}_ukbb_{}", "UKB_osar_{}_ukbb_{}", "UKB_hfvr_{}_ukbb_{}", "UKB_chol_{}_ukbb_{}", "UKB_ht_{}_ukbb_{}", "UKB_ast_{}_ukbb_{}", "UKB_height_{}_ukbb_{}"]] for c in b] # "D2_hdlp_willer_2013_ukbb_{}" , "D2_t2di_mahajan_2018_ukbb_{}"] ]
imps=["impute2_1kg_eur", "impute2_1kg_gbr", "impute2_1kg_ibs", "impute2_1kg_eur-minus-gbr", "impute2_1kg_eur100", "impute2_1kg_eur100-minus-gbr"] # , "imputeX_new"]
plot_curves(metric_name, fname, field_name, prs_names=prs_names, imps=imps, out_suffix="ukb_all", cols=4)


prs_names=[c for b in [[a.format("gbr","afr"),a.format("gbr","sas")] for a in ["UKB_t2d_{}_ukbb_{}", "UKB_osar_{}_ukbb_{}", "UKB_hfvr_{}_ukbb_{}", "UKB_chol_{}_ukbb_{}", "UKB_ht_{}_ukbb_{}", "UKB_ast_{}_ukbb_{}", "UKB_height_eur_ukbb_{}"]] for c in b] # "D2_hdlp_willer_2013_ukbb_{}" , "D2_t2di_mahajan_2018_ukbb_{}"] ]
imps=["impute2_1kg_eur", "impute2_1kg_gbr", "impute2_1kg_ibs", "impute2_1kg_eur-minus-gbr", "impute2_1kg_eur100", "impute2_1kg_eur100-minus-gbr"] # , "imputeX_new"]
plot_curves(metric_name, fname, field_name, prs_names=prs_names, imps=imps, out_suffix="ukb_gbr_all", cols=4)

prs_names=[c for b in [[a.format("eur","afr"),a.format("eur","sas")] for a in ["UKB_t2d_{}_ukbb_{}", "UKB_osar_{}_ukbb_{}", "UKB_hfvr_{}_ukbb_{}", "UKB_chol_{}_ukbb_{}", "UKB_ht_{}_ukbb_{}", "UKB_ast_{}_ukbb_{}", "UKB_height_{}_ukbb_{}"]] for c in b] # "D2_hdlp_willer_2013_ukbb_{}" , "D2_t2di_mahajan_2018_ukbb_{}"] ]
imps=["impute2_1kg_eur", "impute2_1kg_gbr", "impute2_1kg_ibs", "impute2_1kg_eur-minus-gbr", "impute2_1kg_eur100", "impute2_1kg_eur100-minus-gbr"] # , "imputeX_new"]
plot_curves(metric_name, fname, field_name, prs_names=prs_names, imps=imps, out_suffix="ukb_eur_all", cols=4)

