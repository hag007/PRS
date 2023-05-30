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


def plot_percentile_curve_multi(fname, fname_test, prs_name, imp, rep_start, rep_end, hyperparameters, folds=5, cols=3):

    df=pd.DataFrame()
    df_test=pd.DataFrame(columns=['hyperparameter'])
    for rep in range(rep_start,rep_end+1):
        for hyperparameter in hyperparameters:
            for fold in range(1,folds+1):
                # print(rep, hyperparameter,fold)
                cur_df=pd.read_csv(os.path.join(constants.PRSS_PATH, prs_name, imp, f'rep_{rep}', fname.format(fold, folds, hyperparameter)), sep='\t')
                cur_df.loc[:,'hyperparameter']=hyperparameter
                df=pd.concat((df,cur_df))

            cur_df_test=pd.read_csv(os.path.join(constants.PRSS_PATH, prs_name, imp, f'rep_{rep}', fname_test.format(folds,hyperparameter)), sep='\t')
            cur_df_test.loc[:,'hyperparameter']=hyperparameter
            df_test=pd.concat((df_test,cur_df_test))

    # out_file_name=f"{'.'.join(fname.format('','','').split('.')[:])}_{rep_start}_{rep_end}"
    plot_percentile_curve_generic(prs_name, imp, hyperparameters, df, df_test, cols=cols)


def plot_percentile_curve_generic(prs_name, imp, hyperparameters, df, df_test, cols=3):

    groupby_colname="Unnamed: 0"
    rows=max(int(np.ceil(len(hyperparameters) / cols)), 2)
    for set_type in ["validation", "test"]:

        fig, ax = plt.subplots(rows ,cols,figsize=((cols+1)*17, 15*rows))

        for i, hp in enumerate(hyperparameters):

            if set_type=="validation":
                mn=df[df.loc[:,'hyperparameter']==hp].groupby(groupby_colname).mean()
                sd=df[df.loc[:,'hyperparameter']==hp].groupby(groupby_colname).std()
                print("val cols: ", df.columns)
                print(mn)
            else:
                mn=df_test[df_test.loc[:,'hyperparameter']==hp].groupby(groupby_colname).mean()
                sd=df_test[df_test.loc[:,'hyperparameter']==hp].groupby(groupby_colname).std()
                print("test cols: ", df_test.columns)
                print(mn)
            print(mn.index)

            ## X axis position defined by percentile intervals: e.g., converting string "20-30" to (20+30)/2
            mn.loc[:,'x_values']=mn.index # mn.iloc[:,0].apply(lambda a: (int(a.split("-")[0])+int(a.split("-")[1]))//2)
            mn.sort_values('x_values', inplace=True)
            sd=sd.loc[mn.index]

            ax[i//cols][i % cols].grid(axis='y')
            ax[i//cols][i % cols].errorbar(mn.loc[:,'x_values'], mn.loc[:,"OR"], yerr=pd.concat((sd.loc[:,"OR"], sd.loc[:,"OR"]), axis=1).values.T, capsize=5, marker='o') # df.loc[:,["CI min", "CI max"]].values.T
            ax[i//cols][i % cols].plot(mn.loc[:,"x_values"], mn.loc[:,"OR"], label=f'{d_imp_names.get(imp,imp)}', linewidth=4, color=cs[l_imps.index(imp)], marker='o')
            ax[i//cols][i % cols].set_yscale('log')
            ax[i//cols][i % cols].yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
            ax[i//cols][i % cols].set_yticks([0.2,0.3,0.4,0.5,1,1.5,2,2.5,3,4,5,6])
            target_title=f"T={hp}"
            ax[i//cols][i % cols].set_title(target_title)
            ax[i//cols][i % cols].set_xticklabels(mn.index, rotation = 45)
            ax[i//cols][i % cols].set_xlabel("Hyperparameters")
            ax[i//cols][i % cols].set_ylabel("OR")
            # print(ax[i//cols][i % cols].get_xticklabels())
            # ax[i//cols][i % cols].legend()

        plt.subplots_adjust(right=0.7)
        ax[-1][-1].legend(loc=(0.95,0))
        plt.savefig(os.path.join(constants.FIGURES_PATH, f"or_percentiles_{prs_name}_{imp}_{set_type}.png"))



if __name__=='__main__':

    target="bcac_aj"

    prs_name="bcac_onco_eur-5pcs_bcac_onco_aj"
    imp="impX_new"

    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-p', '--prs_name', dest='prs_name', help="", default=prs_name)
    parser.add_argument('-i', '--imp', dest='imp', help="", default=imp)
    parser.add_argument('-m', '--metric_name', dest='metric_name', help="", default="OR")
    parser.add_argument('-s', '--rep_start', dest='rep_start', help="", default="71")
    parser.add_argument('-e', '--rep_end', dest='rep_end', help="", default="90")
    parser.add_argument('-f', '--file_name_format', dest='file_name_format', help="", default="prs.cv.ls___{}_{}_validation.or.percentile.{}.tsv") # prs.statistics_summary_{}.tsv
    parser.add_argument('-ft', '--file_name_format_test', dest='file_name_format_test', help="", default="prs.cv.ls___{}_test.or.percentile.{}.tsv") # prs.statistics_summary_{}.tsv

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

