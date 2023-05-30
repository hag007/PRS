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

def plot_or_by_imputation(file_name_format, prs_names, targets, imps, methods=['pt', 'pt2', 'ls'], cols=3, metric="all", suffix=""):


    df_all=pd.read_csv(os.path.join(constants.OUTPUT_PATH, file_name_format), sep='\t')

    if imps is None:
        imps=df_all.loc[:,"imp"].unique()
        imps.sort()

    if prs_names is None:
        prs_names=df_all.loc[:,"prs_name"].unique()
        prs_names.sort()

    fig, axs = plt.subplots(2, 2,figsize=(35,30))
    df_all=df_all.loc[df_all.loc[:,"imp"].isin(imps),:]



    if not targets is None:
        df_all=df_all.loc[df_all.loc[:,'prs_name'].apply(lambda a : target in a),:]


    for i, method in enumerate(methods):
        df=df_all[df_all.loc[:,'method']==method]
        df_ref=df[df.loc[:,'imp']==imps[-1]]
        df_ref.index=df_ref.loc[:,'prs_name']
        # df_ref=df_ref.loc[:,f'or_{metric}']
        df['order']=df['imp'].apply(lambda a: imps.index(a))
        df=df.sort_values(by='order')
        ax=axs[i//2][i%2]

        df.loc[:,'x_values']=df.loc[:,'imp'].apply(lambda a: d_imp_names.get(a, a))
        df.loc[:,f'mean_outer_{metric}']=df_ref.reindex(df.loc[:,'prs_name']).loc[:,f'mean_outer_{metric}'].values-df.loc[:,f'mean_outer_{metric}'].values
        df=df[df.loc[:,'imp'].isin(imps[:-1])]
        errors=np.hstack((df.loc[:,[f"se_outer_{metric}"]].values,df.loc[:,[f"se_outer_{metric}"]].values)).T

        if len(df.loc[:,'x_values'].unique()) == len(df.loc[:,"x_values"]):
            ax.errorbar(df.loc[:,'x_values'], df.loc[:,f"mean_outer_{metric}"], yerr=errors, fmt='-o', linestyle="None", marker='o', markersize=12)
        else:
            sns.boxplot(x='x_values', y=f"mean_outer_{metric}", data=df, ax=ax, color=sns.color_palette('pastel')[0],  showfliers=False, showmeans=True, meanprops={"markersize":"12"}) # , fmt='-o', linestyle="None", marker='o', markersize=12)
            sns.stripplot(x='x_values', y=f"mean_outer_{metric}", data=df, ax=ax, color='blue', s=12) # , fmt='-o', linestyle="None", marker='o', markersize=12)

            ax.set_ylim(ax.get_ylim()[0],df.loc[:,'mean_outer_all'].max()+0.1)
            i=0
            for imp in imps[:-1]:
                vals=df.loc[df.loc[:,'imp']==imp,f'mean_outer_{metric}'].dropna().values
                if len(vals)!=0:
                    pval=sp.stats.ttest_1samp(vals, 0).pvalue
                    ax.text(i-0.25,df.loc[:,'mean_outer_all'].max()+0.05, f'{pval:.2e}')
                    i+=1


        plt.setp(ax.get_xticklabels(), rotation=35)
        ax.set_xlabel("imputation panels")
        ax.set_ylabel(d_metrics.get(metric,metric))
        ax.set_title(d_methods.get(method,method))
        ax.legend()


        plt.tight_layout() # subplots_adjust(right=0.7)

        # ax.legend() # (loc=(0.95,0))
        plt.savefig(os.path.join(constants.FIGURES_PATH, f"or_by_panel_diff_{metric}_{suffix}.png"))



if __name__=='__main__':


    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-p', '--prs_names', dest='prs_names', help="", default="")
    parser.add_argument('-i', '--imps', dest='imps', help="", default="")
    parser.add_argument('-m', '--metric_name', dest='metric_name', help="", default="OR")
    parser.add_argument('-fn', '--file_name_format', dest='file_name_format', help="", default="prs.cv.choose_params_{}_{}.tsv") # prs.statistics_summary_{}.tsv
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
    # target="dbg-scz19"
    # imps_super_pop=["impute2_ajkg14_t101", "impute2_1kg_eur2", "impute2_1kg_eas2", "impute2_1kg_afr2"]
    # imps_pop=["impute2_ajkg14_t101", "impute2_1kg_ceu2", "impute2_1kg_gbr2", "impute2_1kg_tsi2", "impute2_1kg_ibs2", "impute2_1kg_fin2", "impute2_1kg_eur2"]
    #
    # plot_or_by_imputation(file_name_format.format(suffix, f'{base_rep}_{rep_start}_{base_rep}_{rep_end}'), prs_names=prs_names, imps=imps_super_pop, suffix="super_pop")
    # plot_or_by_imputation(file_name_format.format(suffix, f'{base_rep}_{rep_start}_{base_rep}_{rep_end}'), prs_names=prs_names, imps=imps_pop, suffix="pop")
    #
    # plot_or_by_imputation(file_name_format.format(suffix, f'{base_rep}_{rep_start}_{base_rep}_{rep_end}'), prs_names=prs_names, imps=imps_super_pop, metric="99", suffix="super_pop")
    # plot_or_by_imputation(file_name_format.format(suffix, f'{base_rep}_{rep_start}_{base_rep}_{rep_end}'), prs_names=prs_names, imps=imps_pop, metric="99", suffix="pop")


    ### UKB: public_GWAS
    suffix="public_gwas"

    target="ukbb_afr"
    imps_super_pop=["original", "imputeX_new", "impute2_1kg_eur", "impute2_1kg_afr"]
    plot_or_by_imputation(file_name_format.format(suffix, f'{base_rep}_{rep_start}_{base_rep}_{rep_end}'), prs_names=prs_names, targets=[target], imps=imps_super_pop, suffix=f"{target}_{suffix}_super_pop")
    plot_or_by_imputation(file_name_format.format(suffix, f'{base_rep}_{rep_start}_{base_rep}_{rep_end}'), prs_names=prs_names, targets=[target], imps=imps_super_pop, metric="99", suffix=f"{target}_{suffix}_super_pop")

    target="ukbb_sas"
    imps_super_pop=["original", "imputeX_new", "impute2_1kg_eur", "impute2_1kg_sas"]
    plot_or_by_imputation(file_name_format.format(suffix, f'{base_rep}_{rep_start}_{base_rep}_{rep_end}'), prs_names=prs_names, targets=[target], imps=imps_super_pop, suffix=f"{target}_{suffix}_super_pop")
    plot_or_by_imputation(file_name_format.format(suffix, f'{base_rep}_{rep_start}_{base_rep}_{rep_end}'), prs_names=prs_names, targets=[target], imps=imps_super_pop, metric="99", suffix=f"{target}_{suffix}_super_pop")

    ### UKB: UKB GWAS
    suffix="ukb_gwas"

    target="ukbb_afr"
    imps_super_pop=["original", "imputeX_new", "impute2_1kg_eur", "impute2_1kg_afr"]
    plot_or_by_imputation(file_name_format.format(suffix, f'{base_rep}_{rep_start}_{base_rep}_{rep_end}'), prs_names=prs_names, targets=[target], imps=imps_super_pop, suffix=f"{target}_{suffix}_super_pop")
    plot_or_by_imputation(file_name_format.format(suffix, f'{base_rep}_{rep_start}_{base_rep}_{rep_end}'), prs_names=prs_names, targets=[target], imps=imps_super_pop, metric="99", suffix=f"{target}_{suffix}_super_pop")

    target="ukbb_sas"
    imps_super_pop=["original", "imputeX_new", "impute2_1kg_eur", "impute2_1kg_sas"]
    plot_or_by_imputation(file_name_format.format(suffix, f'{base_rep}_{rep_start}_{base_rep}_{rep_end}'), prs_names=prs_names, targets=[target], imps=imps_super_pop, suffix=f"{target}_{suffix}_super_pop")
    plot_or_by_imputation(file_name_format.format(suffix, f'{base_rep}_{rep_start}_{base_rep}_{rep_end}'), prs_names=prs_names, targets=[target], imps=imps_super_pop, metric="99", suffix=f"{target}_{suffix}_super_pop")
