import itertools
import os

import matplotlib

import constants

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None
from name_mappings import *
cs = sns.color_palette("bright") + sns.color_palette("pastel")
font = {'size': 30}
matplotlib.rc('font', **font)
import utils


def plot_boxplot_cv_multi_test(metric_name, fname, field_name, discoveries, targets, imps, out_suffix, rep_start, rep_end, hyperparameters ,cols=3):



    df=pd.DataFrame()
    df_test=pd.DataFrame(columns=['prs_name', 'imp', 'hyperparameter'])
    start=int(rep_start.split("_")[1] if "_" in rep_start else rep_start)
    end=int(rep_end.split("_")[1] if "_" in rep_end else rep_end)
    for rep in range(start,end+1):

        suffix=("_"+rep_start.split("_")[0]+"_"+str(rep) if "_" in rep_start else "_"+str(rep))
        print("here train:", fname.format("",suffix))
        cur_df=pd.read_csv(os.path.join(constants.OUTPUT_PATH, fname.format(".ctrl",suffix)), sep='\t')
        utils.fix_table(cur_df)
        df=pd.concat((df,cur_df))
        cur_df_test=pd.read_csv(os.path.join(constants.OUTPUT_PATH, fname.format(".test.ctrl",suffix)), sep='\t')
        utils.fix_table(cur_df_test)
        df_test=pd.concat((df_test,cur_df_test))

    out_file_name=f"{'.'.join(fname.format('ctrl','').split('.')[:3])}_{metric_name}_{out_suffix}_{rep_start}_{rep_end}"
    prs_names=[f'{a}_{b}' for a, b in itertools.product(discoveries, targets)]
    plot_boxplot_cv_test(metric_name, field_name, prs_names, imps, rep_start, rep_end, hyperparameters, df, df_test, out_file_name, cols=cols)


def plot_boxplot_cv_single_test(metric_name, fname, field_name, discoveries, targets, imps, out_suffix, rep_start, rep_end, hyperparameters, cols=3):

    print("here test:", os.path.join(constants.OUTPUT_PATH, fname.format(".ctrl","")))

    df=pd.read_csv(os.path.join(constants.OUTPUT_PATH, fname.format(".ctrl","")), sep='\t')
    utils.fix_table(df)
    df_test=pd.read_csv(os.path.join(constants.OUTPUT_PATH, fname.format(".test.ctrl","")), sep='\t')
    utils.fix_table(df_test)

    out_file_name=f"{'.'.join(fname.format('ctrl','').split('.')[:2])}_{metric_name}_{out_suffix}"
    prs_names=[f'{a}_{b}' for a, b in itertools.product(discoveries, targets)]
    plot_boxplot_cv_test(metric_name, field_name, prs_names, imps, rep_start, rep_end, hyperparameters, df, df_test, out_file_name, cols=cols)

def plot_boxplot_cv_test(metric_name, field_name, prs_names, imps, rep_start, rep_end, hyperparameters, df, df_test, out_file_name, folds=5, cols=3):

    if imps is None:
        imps=df.loc[:,"imp"].unique()
        imps.sort()

    if prs_names is None:
        prs_names=df.loc[:,"prs_name"].unique()
        prs_names.sort()

    if len(df_test)>0:
        df_test.index=np.arange(len(df_test))
        df_test=df_test.sort_values(by='hyperparameter')
        df_test.loc[:,'test_type']='test'

    rows=max(int(np.ceil(len(prs_names)/cols)),2)
    fig, ax = plt.subplots(rows ,cols,figsize=((cols+1)*15, 12*rows))
    df_all=pd.DataFrame()
    for i, prs_name in enumerate(prs_names):
        prs_title="_".join(prs_name.split("_")[:-2])
        for j, imp in enumerate(imps):
            cur_df=df.loc[(df.loc[:,'prs_name']==prs_name) & (df.loc[:,'imp']==imp)]
            print(prs_name, imp, cur_df.shape)
            ### DO NOT DELETE
            mns=cur_df.groupby('hyperparameter')[field_name].mean().rename('mean')
            mds=cur_df.groupby('hyperparameter')[field_name].median().rename('median')
            n_snps_mns=cur_df.groupby('hyperparameter')['n_snps'].mean().rename('n_snps_mean')
            n_snps_sd=cur_df.groupby('hyperparameter')['n_snps'].std().rename('n_snps_sd')/np.sqrt(folds)
            sd=cur_df.groupby('hyperparameter')[field_name].std().rename('sd')/np.sqrt(folds)
            ###
            # mx=cur_df.groupby('fold')[field_name].max().rename('max')
            # mx=pd.DataFrame(columns=["mean", "sd"], data=[[mx.mean(),mx.std()/np.sqrt(mx.shape[0])]])
            cur_all=pd.concat((mns, mds, sd, n_snps_mns, n_snps_sd), axis=1)
            if len(cur_df)==0:
                continue

            cur_df.loc[:,'test_type']='validation'

            if len(df_test)!=0:
                cur_df_test=df_test.loc[(df_test.loc[:,'prs_name']==prs_name) &(df_test.loc[:,'imp']==imp)]
                # sns.boxplot(y=field_name,x='hyperparameter', data=cur_df, ax=ax[i//cols][i % cols], color='white', showmeans=True, order=[a for a in hyperparameters if a in cur_df.loc[:,'hyperparameter'].values])
                # sns.stripplot(y=field_name,x='hyperparameter', data=cur_df, ax=ax[i//cols][i % cols], color='green', order=[a for a in hyperparameters if a in cur_df_test.loc[:,'hyperparameter'].values])
                # print(cur_df_test.groupby('hyperparameter')[field_name].count())

                cur_all=pd.concat((cur_df,cur_df_test))

                sns.boxplot(y=field_name,x='hyperparameter', hue='test_type', data=cur_all, ax=ax[i//cols][i % cols], palette="pastel", showmeans=True, order=[a for a in hyperparameters if a in cur_df.loc[:,'hyperparameter'].values])

            if len(df_test)!=0:

                # sns.stripplot(y=field_name,x='hyperparameter', data=cur_df_test, ax=ax[i//cols][i % cols], color='red', order=[a for a in hyperparameters if a in cur_df_test.loc[:,'hyperparameter'].values])

                ### DO NOT DELETE
                mns_test=cur_df_test.groupby('hyperparameter')[field_name].mean().rename('mean_test')
                n_snps_mns_test=cur_df_test.groupby('hyperparameter')['n_snps'].mean().rename('n_snps_mean_test')
                mds_test=cur_df_test.groupby('hyperparameter')[field_name].median().rename('median_test')
                ###
                # mx_test=cur_df_test
                # print(mx_test)

                # ax[i//cols][i % cols].scatter(cur_df_test.loc[:, 'hyperparameter'], cur_df_test.loc[:, field_name], color='red') # np.array([[a]*(rep_end-rep_start+1) for a in np.arange(1, len(mns_test)+1)]).flatten() # cur_df_test.loc[:, 'hyperparameter']
                # ax[i//cols][i % cols].scatter(np.arange(len(mns_test.index)), mns_test[[a for a in hyperparameters if a in mns_test.index.values]], color='red', marker='^') # np.arange(1, len(hyperparameters)+1) # mns_test.index
                # ax[i//cols][i % cols].scatter(np.arange(len(mns_test.index)), mds_test[[a for a in hyperparameters if a in mns_test.index.values]], color='red', marker='_', s=300)  # mns_test.index
                ax[i//cols][i % cols].set_xticklabels(ax[i//cols][i % cols].get_xticklabels(), rotation = 45)

                cur_df=pd.concat((mns, mds, sd, n_snps_mns, n_snps_sd, mns_test.reindex(mns.index), mds_test.reindex(mns.index), n_snps_mns_test.reindex(mns.index) ), axis=1)
            else:
                cur_df=cur_all
            cur_df.loc[:,'prs_name']=prs_name
            cur_df.loc[:,'imp']=imp
            df_all=pd.concat((df_all, cur_df))

        target_title="_".join(prs_name.split("_")[-2:])
        ax[i//cols][i % cols].set_title(f'{d_prs_names.get(prs_title,prs_title)}/{d_target_names.get(target_title,target_title)}')
        ax[i//cols][i % cols].set_xlabel('hyperparameter')
        ax[i//cols][i % cols].set_ylabel(" ".join(metric_name.split('_')))

    # df_stats.to_csv(f"stats_{metric_name}_{out_suffix}.tsv", sep='\t')
    plt.subplots_adjust(right=0.7)
    plt.tight_layout()
    ax[-1][-1].legend(loc=(0.95,0))
    plt.savefig(os.path.join(constants.FIGURES_PATH, out_file_name+".png"))
    ## DO NOT DELETE
    df_all.to_csv(os.path.join(constants.OUTPUT_PATH, f"{out_file_name}.tsv"), sep='\t')
    ##

    # mx.to_csv(os.path.join(constants.OUTPUT_PATH, f"{out_file_name}_mx.tsv"), sep='\t')
    # mx_test.to_csv(os.path.join(constants.OUTPUT_PATH, f"{out_file_name}_mx_test.tsv"), sep='\t')

    # df_all_test.to_csv(os.path.join(constants.OUTPUT_PATH, out_file_name+"_test.tsv"), sep='\t')
