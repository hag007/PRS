import argparse
import os

import matplotlib
import constants

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None
import seaborn as sns
cs = sns.color_palette("bright") + sns.color_palette("pastel")
font = {'size' : 30}
matplotlib.rc('font', **font)
from name_mappings import *
import scipy as sp

def plot_or_by_imputation(file_name_format, prs_names, discoveries, targets, imps, methods=['pt', 'pt2', 'ls'], cols=3, metric="auc_diff", suffix=""):


    df_all=pd.read_csv(os.path.join(constants.OUTPUT_PATH, file_name_format), sep='\t')
    if imps is None:
        imps=df_all.loc[:,"imp"].unique()
        imps.sort()

    fig, axs = plt.subplots(2, 2,figsize=(35,30))
    df_all=df_all.loc[df_all.loc[:,"imp"].isin(imps),:]

    if not targets is None:
        df_all=df_all.loc[df_all.loc[:,'prs_name'].apply(lambda a : any([a.endswith(t) for t in targets])),:]

    if not discoveries is None:
        df_all=df_all.loc[df_all.loc[:,'prs_name'].apply(lambda a : any([a.startswith(d) for d in discoveries])),:]


    df_agg=pd.DataFrame()
    for i, method in enumerate(methods):
        df=df_all[df_all.loc[:,'method']==method]
        df_ref=df[df.loc[:,'imp'].isin(imps[-len(targets):])]
        df_ref.index=df_ref.loc[:,'prs_name']
        # df_ref=df_ref.loc[:,f'or_{metric}']
        df['order']=df['imp'].apply(lambda a: imps.index(a))
        df=df.sort_values(by='order')
        ax=axs[i//2][i%2]

        df.loc[:,'x_values']=df.loc[:,'imp'].apply(lambda a: d_imp_names.get(a, a))
        df.loc[:,metric]=df.loc[:,metric].values-df_ref.reindex(df.loc[:,'prs_name']).loc[:,metric].values
        df=df[df.loc[:,'imp'].isin(imps[:-len(targets)])]
        errors=np.hstack((df.loc[:,[f'{metric.split("_")[-1]}_sem']].values,df.loc[:,[f'{metric.split("_")[-1]}_sem']].values)).T
        df_agg=pd.concat((df_agg,df))
        if len(df.loc[:,'x_values'].unique()) == len(df.loc[:,"x_values"]):
            print(df.loc[:,metric])
            print(errors)
            ax.errorbar(df.loc[:,'x_values'], df.loc[:,metric], yerr=errors, fmt='-o', linestyle="None", marker='o', markersize=12)
        else:
            sns.boxplot(x='x_values', y=metric, data=df, ax=ax, color=sns.color_palette('pastel')[0],  showfliers=False, showmeans=True, meanprops={"markersize":"12"}) # , fmt='-o', linestyle="None", marker='o', markersize=12)
            sns.stripplot(x='x_values', y=metric, data=df, ax=ax, color='blue', s=12) # , fmt='-o', linestyle="None", marker='o', markersize=12)
            original_y_range=ax.get_ylim()[1]-ax.get_ylim()[0]
            original_ylim_max=ax.get_ylim()[1]
            ax.set_ylim(ax.get_ylim()[0],original_ylim_max+original_y_range*0.15)
            i=0
            for imp in imps[:-len(targets)]:
                vals=df.loc[df.loc[:,'imp']==imp,metric].dropna().values
                if len(vals)!=0:
                    nl=0 # (0.5 if metric=="auc_delta" else 1 if metric=='binary' else 0)
                    pval=sp.stats.ttest_1samp(vals, nl).pvalue
                    ax.text(i-0.25,original_ylim_max+original_y_range*0.05, f'{pval:.2e}')
                    i+=1


        plt.setp(ax.get_xticklabels(), rotation=35)
        ax.set_xlabel("imputation panels")
        ax.set_ylabel(d_metrics.get(metric,metric))
        ax.set_title(d_methods.get(method,method))
        ax.legend()


    ####################
    ax=axs[-1][-1]
    sns.boxplot(x='x_values', y=metric, data=df_agg, ax=ax, color=sns.color_palette('pastel')[0],  showfliers=False, showmeans=True, meanprops={"markersize":"14", "markerfacecolor": "red"}) # , fmt='-o', linestyle="None", marker='o', markersize=12)
    sns.stripplot(x='x_values', y=metric, data=df_agg, ax=ax, color='blue', s=12) # , fmt='-o', linestyle="None", marker='o', markersize=12)
    mx=df_agg.loc[:,metric].max()
    ax.set_ylim(ax.get_ylim()[0],0 if pd.isna(mx) else mx+0.1)
    ax.plot([-1,len(imps)-len(targets)], [0,0], linestyle='dashed', color='black') # , fmt='-o', linestyle="None", marker='o', markersize=12)

    i=0
    for imp in imps[:-len(targets)]:
        vals=df_agg.loc[df_agg.loc[:,'imp']==imp,metric].dropna().values
        if len(vals)!=0:
            pval=sp.stats.wilcoxon(vals).pvalue
            print(f'{(vals>0).sum()}/{len(vals)}', "larger than 0")
            print(sp.stats.wilcoxon(vals))
            ax.text(i-0.25,df_agg.loc[:,metric].max()+0.05, f'{pval:.2e}')
            i+=1
    plt.setp(ax.get_xticklabels(), rotation=35)
    ax.set_xlabel("imputation panels")
    ax.set_ylabel(d_metrics.get(metric,metric))
    ax.set_title('Combined')

    ##########


    plt.tight_layout() # subplots_adjust(right=0.7)

    # ax.legend() # (loc=(0.95,0))
    plt.savefig(os.path.join(constants.FIGURES_PATH, f"or_by_panel_auc_diff_{metric}_{suffix}.png"))



if __name__=='__main__':


    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-p', '--prs_names', dest='prs_names', help="", default="")
    parser.add_argument('-i', '--imps', dest='imps', help="", default="")
    parser.add_argument('-m', '--metric_name', dest='metric_name', help="", default="OR")
    parser.add_argument('-fn', '--file_name_format', dest='file_name_format', help="", default="prs.cv.auc_{}_{}.tsv") # prs.statistics_summary_{}.tsv
    parser.add_argument('-su', '--suffix', dest='suffix', help="", default="scz") # prs.statistics_summary_{}.tsv
    parser.add_argument('-b', '--base_rep', dest='base_rep', help="", default='105')
    parser.add_argument('-s', '--rep_start', dest='rep_start', help='', default='1')
    parser.add_argument('-e', '--rep_end', dest='rep_end', help="", default='6')

    args = parser.parse_args()
    prs_names=args.prs_names.split(',')
    imps=args.imps.split(',')
    metric_name = args.metric_name
    suffix = args.suffix
    base_rep = args.base_rep
    rep_start = args.rep_start
    rep_end = args.rep_end
    file_name_format = args.file_name_format
    field_name=metric_name




    ### SCZ
    discovery="PGC2_noAJ"
    target="dbg-scz19"
    imps_super_pop=["impute2_1kg_eur2", "impute2_1kg_eas2", "impute2_1kg_afr2", "impute2_ajkg14_t101"]
    imps_pop=["impute2_1kg_ceu2", "impute2_1kg_gbr2", "impute2_1kg_tsi2", "impute2_1kg_ibs2", "impute2_1kg_fin2", "impute2_ajkg14_t101"]

    plot_or_by_imputation(file_name_format.format(suffix, f'{base_rep}_{rep_start}_{base_rep}_{rep_end}'), prs_names=prs_names, discoveries=[discovery], targets=['dbg-scz19'], imps=imps_super_pop, suffix="super_pop")
    plot_or_by_imputation(file_name_format.format(suffix, f'{base_rep}_{rep_start}_{base_rep}_{rep_end}'), prs_names=prs_names, discoveries=[discovery],  targets=['dbg-scz19'], imps=imps_pop, suffix="pop")

    # plot_or_by_imputation(file_name_format.format(suffix, f'{base_rep}_{rep_start}_{base_rep}_{rep_end}'), prs_names=prs_names, targets=['dbg-scz19'], imps=imps_super_pop, metric="99", suffix="super_pop")
    # plot_or_by_imputation(file_name_format.format(suffix, f'{base_rep}_{rep_start}_{base_rep}_{rep_end}'), prs_names=prs_names, targets=['dbg-scz19'], imps=imps_pop, metric="99", suffix="pop")


    ### UKB: public_GWAS
    suffix="public_gwas"
    discoveries=["D2_sysp_evangelou_2018","D2_chol_willer_2013","D2_t2di_mahajan_2018"] # ["D2_sysp_evangelou_2018","D2_dias_evangelou_2018","D2_asth_zhu_2019","D2_chol_willer_2013","D2_ldlp_willer_2013","D2_t2di_mahajan_2018","D2_gerx_an_2019","D2_madd_howard_2019"]

    target="ukbb_afr"
    imps_super_pop=["original", "impute2_1kg_eur", "impute2_1kg_afr"] # , "imputeX_new"
    # plot_or_by_imputation(file_name_format.format(suffix, f'{base_rep}_{rep_start}_{base_rep}_{rep_end}'), prs_names=prs_names, discoveries=discoveries, targets=[target], imps=imps_super_pop, suffix=f"{target}_{suffix}_super_pop")
    # plot_or_by_imputation(file_name_format.format(suffix, f'{base_rep}_{rep_start}_{base_rep}_{rep_end}'), prs_names=prs_names, discoveries=discoveries,targets=[target], imps=imps_super_pop, metric="99", suffix=f"{target}_{suffix}_super_pop")

    target="ukbb_sas"
    imps_super_pop=["original", "impute2_1kg_eur", "impute2_1kg_sas"] # , "imputeX_new"
    # plot_or_by_imputation(file_name_format.format(suffix, f'{base_rep}_{rep_start}_{base_rep}_{rep_end}'), prs_names=prs_names, discoveries=discoveries,targets=[target], imps=imps_super_pop, suffix=f"{target}_{suffix}_super_pop")
    # plot_or_by_imputation(file_name_format.format(suffix, f'{base_rep}_{rep_start}_{base_rep}_{rep_end}'), prs_names=prs_names, discoveries=discoveries,targets=[target], imps=imps_super_pop, metric="99", suffix=f"{target}_{suffix}_super_pop")


    targets=["ukbb_sas", "ukbb_afr"]
    imps_super_pop=["original", "impute2_1kg_eur", "impute2_1kg_sas", "impute2_1kg_afr"] # , "imputeX_new"
    # plot_or_by_imputation(file_name_format.format(suffix, f'{base_rep}_{rep_start}_{base_rep}_{rep_end}'), prs_names=prs_names, discoveries=discoveries,targets=targets, imps=imps_super_pop, suffix=f"all_pop_{suffix}_super_pop")
    # plot_or_by_imputation(file_name_format.format(suffix, f'{base_rep}_{rep_start}_{base_rep}_{rep_end}'), prs_names=prs_names, discoveries=discoveries,targets=[target], imps=imps_super_pop, metric="99", suffix=f"all_pop_{suffix}_super_pop")


    ### UKB: UKB GWAS
    suffix="ukb_gwas"
    discoveries=["UKB_ht_eur","UKB_chol_eur","UKB_hfvr_eur","UKB_hyty_eur","UKB_madd_eur","UKB_osar_eur","UKB_t2d_eur","UKB_utfi_eur","UKB_gerx_eur","UKB_angna_eur","UKB_ast_eur","UKB_ctrt_eur"]

    target="ukbb_afr"
    imps_super_pop=["original", "impute2_1kg_eur", "impute2_1kg_afr"] # , "imputeX_new"
    plot_or_by_imputation(file_name_format.format(suffix, f'{base_rep}_{rep_start}_{base_rep}_{rep_end}'), prs_names=prs_names, discoveries=discoveries, targets=[target], imps=imps_super_pop, suffix=f"{target}_{suffix}_super_pop")
    # plot_or_by_imputation(file_name_format.format(suffix, f'{base_rep}_{rep_start}_{base_rep}_{rep_end}'), prs_names=prs_names, discoveries=discoveries, targets=[target], imps=imps_super_pop, metric="99", suffix=f"{target}_{suffix}_super_pop")

    target="ukbb_sas"
    imps_super_pop=["original", "impute2_1kg_eur", "impute2_1kg_sas"] # , "imputeX_new"
    plot_or_by_imputation(file_name_format.format(suffix, f'{base_rep}_{rep_start}_{base_rep}_{rep_end}'), prs_names=prs_names, discoveries=discoveries, targets=[target], imps=imps_super_pop, suffix=f"{target}_{suffix}_super_pop")
    # plot_or_by_imputation(file_name_format.format(suffix, f'{base_rep}_{rep_start}_{base_rep}_{rep_end}'), prs_names=prs_names, discoveries=discoveries, targets=[target], imps=imps_super_pop, metric="99", suffix=f"{target}_{suffix}_super_pop")

    targets=["ukbb_sas", "ukbb_afr"]
    imps_super_pop=["original", "impute2_1kg_eur", "impute2_1kg_sas", "impute2_1kg_afr"] # , "imputeX_new"
    plot_or_by_imputation(file_name_format.format(suffix, f'{base_rep}_{rep_start}_{base_rep}_{rep_end}'), prs_names=prs_names, discoveries=discoveries, targets=targets, imps=imps_super_pop, suffix=f"all_pop_{suffix}_super_pop")
    # plot_or_by_imputation(file_name_format.format(suffix, f'{base_rep}_{rep_start}_{base_rep}_{rep_end}'), prs_names=prs_names, discoveries=discoveries, targets=[target], imps=imps_super_pop, metric="99", suffix=f"all_pop_{suffix}_super_pop")
