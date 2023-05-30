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


def plot_percentile_curve_multi(fname, fname_test, prs_name, imp, rep_start, rep_end, hyperparameters, method="ls", folds=5, cols=1):




    df=pd.DataFrame()
    df_test=pd.DataFrame(columns=['hyperparameter'])
    for rep in range(int(rep_start.split("_")[1]), int(rep_end.split("_")[1])+1):
        fl_name_or_all = os.path.join(constants.OUTPUT_PATH, f'prs.cv.{method}ctrl_or_all_bcac_aj_ctrl_{rep_start.split("_")[0]}_{rep}_{rep_start.split("_")[0]}_{rep}.tsv')
        fl_name_or_99 = os.path.join(constants.OUTPUT_PATH, f'prs.cv.{method}ctrl_or_99_bcac_aj_ctrl_{rep_start.split("_")[0]}_{rep}_{rep_start.split("_")[0]}_{rep}.tsv')
        print(fl_name_or_all)
        if os.path.exists(fl_name_or_all):
            df_all = pd.read_csv(fl_name_or_all, sep='\t')
            df_99 = pd.read_csv(fl_name_or_99, sep='\t')

            df_all=df_all.sort_values(by=["mean"], ascending=False)
            df_all.index=df_all.loc[:,'hyperparameter'].apply(lambda a: f"{method}_{rep}_{a}")
            df_all.loc[:,'order']=np.arange(1,df_all.shape[0]+1)
            df_99=df_99.sort_values(by=["mean"], ascending=False)
            df_99.index=df_99.loc[:,'hyperparameter'].apply(lambda a: f"{method}_{rep}_{a}")
            df_99.loc[:,'order']=np.arange(1,df_99.shape[0]+1)
            idx=(df_all.loc[:,'order']+df_99.loc[:,'order']).idxmin()
            print("idx",idx)
            # df_all.loc[idx]
            # df_99.loc[idx]


            # df_or_all = pd.concat((df_or_all,  df_all.loc[idx].to_frame().T),axis=0)
            # df_or_99 = pd.concat((df_or_99,  df_99.loc[idx].to_frame().T), axis=0)

            df_folds=pd.DataFrame()
            for fold in range(1,folds+1):
                # print(rep, hyperparameter,fold)
                cur_df=pd.read_csv(os.path.join(constants.PRSS_PATH, prs_name, imp, f'rep_{rep_start.split("_")[0]}_{rep}', fname.format(fold, folds, idx.split("_")[-1])), sep='\t')
                df_folds=pd.concat((df_folds,cur_df))
            df_folds=df_folds.groupby('Unnamed: 0').mean()
            df_folds.loc[:,'hyperparameter']=idx.split("_")[-1]
            df=pd.concat((df,df_folds))

            cur_df_test=pd.read_csv(os.path.join(constants.PRSS_PATH, prs_name, imp, f'rep_{rep_start.split("_")[0]}_{rep}', fname_test.format(folds,idx.split("_")[-1])), sep='\t')
            cur_df_test.loc[:,'hyperparameter']=idx.split("_")[-1]
            df_test=pd.concat((df_test,cur_df_test))



    print(df)
    print(df_test)

    plot_percentile_curve_generic(prs_name, imp, hyperparameters, df, df_test, cols=cols)


def plot_percentile_curve_generic(prs_name, imp, hyperparameters, df, df_test, cols=1):

    print(df)
    groupby_colname="Unnamed: 0"
    rows=1
    for set_type in ["validation", "test"]:

        fig, ax = plt.subplots(rows ,cols,figsize=(25, 17))

        if set_type=="validation":
            mn=df.groupby(groupby_colname).mean()
            sd=df.groupby(groupby_colname).std()
            print("val cols: ", df.columns)
            print(mn)
            print(sd)
        else:
            mn=df_test.groupby(groupby_colname).mean()
            sd=df_test.groupby(groupby_colname).sem()
            print("test cols: ", df_test.columns)
            print(mn)
            print(sd)
        print(mn.index)

        ## X axis position defined by percentile intervals: e.g., converting string "20-30" to (20+30)/2
        mn.loc[:,'x_values']=mn.index # mn.iloc[:,0].apply(lambda a: (int(a.split("-")[0])+int(a.split("-")[1]))//2)
        mn.loc[:,'x_sort']=mn.loc[:,'x_values'].apply(lambda a: int(a.split('-')[0]))
        mn.sort_values('x_sort', inplace=True)
        sd=sd.loc[mn.index]

        ax.grid(axis='y')
        ax.errorbar(mn.loc[:,'x_values'], mn.loc[:,"OR"], yerr=pd.concat((sd.loc[:,"OR"], sd.loc[:,"OR"]), axis=1).values.T, capsize=5, marker='o') # df.loc[:,["CI min", "CI max"]].values.T
        ax.plot(mn.loc[:,"x_values"], mn.loc[:,"OR"], label=f'{d_imp_names.get(imp,imp)}', linewidth=4, color=cs[l_imps.index(imp)], marker='o')
        ax.set_yscale('log')
        ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
        ax.set_yticks([0.4,0.5,1,1.5,2,2.5,3,4])
        ax.set_xticklabels(mn.index, rotation = 45)
        ax.set_xlabel("Hyperparameters")
        ax.set_ylabel("OR")
        # print(ax.get_xticklabels())
        # ax.legend()

        plt.subplots_adjust(right=0.7)
        # ax.legend(loc=(0.95,0))
        plt.savefig(os.path.join(constants.FIGURES_PATH, f"or_percentiles_{prs_name}_{imp}_{set_type}.png"))



if __name__=='__main__':

    target="bcac_aj"

    prs_name="bcac_onco_eur-5pcs_bcac_onco_aj"
    imp="impX_new"

    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-p', '--prs_name', dest='prs_name', help="", default=prs_name)
    parser.add_argument('-i', '--imp', dest='imp', help="", default=imp)
    parser.add_argument('-m', '--metric_name', dest='metric_name', help="", default="OR")
    parser.add_argument('-s', '--rep_start', dest='rep_start', help="", default="105_1")
    parser.add_argument('-e', '--rep_end', dest='rep_end', help="", default="105_6")
    parser.add_argument('-f', '--file_name_format', dest='file_name_format', help="", default="prs.cv.ls___{}_{}_validation.ctrl.or.percentile.{}.tsv") # prs.statistics_summary_{}.tsv
    parser.add_argument('-ft', '--file_name_format_test', dest='file_name_format_test', help="", default="prs.cv.ls___{}_test.ctrl.or.percentile.{}.tsv") # prs.statistics_summary_{}.tsv

    args = parser.parse_args()
    prs_name=args.prs_name
    imp=args.imp
    rep_start = args.rep_start
    rep_end = args.rep_end
    file_name_format = args.file_name_format
    file_name_format_test = args.file_name_format_test
    # field_name=metric_name

    hyperparameters=[f'{a}-{b}' for a in [0.2,0.5,0.9,1] for b in range(1,21)]
    # hyperparameters=[f'{a}-{b}' for a in [0.5] for b in range(9,12)]
    plot_percentile_curve_multi(file_name_format, file_name_format_test, prs_name=prs_name, imp=imp, hyperparameters=hyperparameters, rep_start=rep_start, rep_end=rep_end)

