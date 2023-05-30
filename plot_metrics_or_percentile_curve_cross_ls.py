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
import utils
cs = sns.color_palette("bright") + sns.color_palette("pastel")
font = {'size' : 30}
matplotlib.rc('font', **font)
from name_mappings import *


def plot_percentile_curve_multi(fname, fname_test, prs_name, imp, tc, ic, hyperparameters, folds=5, cols=3):

    df=pd.DataFrame()
    df_test=pd.DataFrame(columns=['hyperparameter'])
    for hyperparameter in hyperparameters:
        # print(rep, hyperparameter,fold)
        cur_df=pd.read_csv(os.path.join(constants.PRSS_PATH, prs_name, imp, f"cross_{tc}", ic, fname.format(hyperparameter)), sep='\t')
        cur_df.loc[:,'hyperparameter']=hyperparameter
        df=pd.concat((df,cur_df))

    plot_percentile_curve_generic(prs_name, imp, hyperparameters, df, cols=cols)


def plot_percentile_curve_generic(prs_name, imp, hyperparameters, df, cols=3):

    rows=max(int(np.ceil(len(hyperparameters) / cols)), 2)

    fig, ax = plt.subplots(rows ,cols,figsize=((cols+1)*17, 15*rows))

    for i, hp in enumerate(hyperparameters):

        ax[i//cols][i % cols].grid(axis='y')
        ax[i//cols][i % cols].errorbar(df.index, df.loc[:,"OR"], yerr=df.loc[:,["CI min", "CI max"]].values.T, capsize=5, marker='o') # df.loc[:,["CI min", "CI max"]].values.T
        ax[i//cols][i % cols].plot(df.loc[:,"x_values"], df.loc[:,"OR"], label=f'{d_imp_names.get(imp,imp)}', linewidth=4, color=cs[l_imps.index(imp)], marker='o')
        ax[i//cols][i % cols].set_yscale('log')
        ax[i//cols][i % cols].yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
        ax[i//cols][i % cols].set_yticks([0.2,0.3,0.4,0.5,1,1.5,2,2.5,3,4,5,6])
        target_title=f"T={hp}"
        ax[i//cols][i % cols].set_title(target_title)
        ax[i//cols][i % cols].set_xticklabels(df.index, rotation = 45)
        ax[i//cols][i % cols].set_xlabel("Hyperparameters")
        ax[i//cols][i % cols].set_ylabel("OR")

        plt.subplots_adjust(right=0.7)
        ax[-1][-1].legend(loc=(0.95,0))
        plt.savefig(os.path.join(constants.FIGURES_PATH, f"or_percentiles_{prs_name}_{imp}_cross.png"))



if __name__=='__main__':

    target="bcac_aj"

    prs_name="bcac_onco_eur-5pcs_bcac_onco_aj"
    imp="impX_new"

    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-p', '--prs_name', dest='prs_name', help="", default=prs_name)
    parser.add_argument('-i', '--imp', dest='imp', help="", default=imp)
    parser.add_argument('-m', '--metric_name', dest='metric_name', help="", default="OR")
    parser.add_argument('-tc', '--target_cross', dest='target_cross', help="", default="bcac_onco_aj")
    parser.add_argument('-ic', '--imp_cross', dest='imp_cross', help="", default="impX_new")
    parser.add_argument('-f', '--file_name_format', dest='file_name_format', help="", default="prs.cross.ls.or.percentile.{}.tsv") # prs.statistics_summary_{}.tsv
    parser.add_argument('-ft', '--file_name_format_test', dest='file_name_format_test', help="", default="prs.cross.ls.or.percentile.{}.tsv") # prs.statistics_summary_{}.tsv

    args = parser.parse_args()
    prs_name=args.prs_name
    imp=args.imp
    rep_start = int(args.rep_start)
    rep_end = int(args.rep_end)
    file_name_format = args.file_name_format
    file_name_format_test = args.file_name_format_test
    # field_name=metric_name

    # hyperparameters=[f'{a}-{b}' for a in [0.2,0.5,0.9,1] for b in range(1,21)]
    hyperparameters=[f'{a}-{b}' for a in [0.5] for b in range(9,12)]
    plot_percentile_curve_multi(file_name_format, file_name_format_test, prs_name=prs_name, imp=imp, hyperparameters=hyperparameters, rep_start=rep_start, rep_end=rep_end)

