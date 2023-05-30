import os

import matplotlib

import constants

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from name_mappings import *
import pandas as pd
pd.options.mode.chained_assignment = None

import utils

font = {'size'   : 30}
matplotlib.rc('font', **font)

def plot_curves(metric_name, fname, field_name, prs_names, imps, out_suffix, cols=3):
    df=pd.read_csv(os.path.join(constants.OUTPUT_PATH, fname), sep='\t')
    utils.fix_table(df)

    if imps is None:
        imps=np.sort(df.loc[:,"imp"].unique())

    if prs_names is None:
        prs_names=np.sort(df.loc[:,"prs_name"].unique())

    rows=max(int(np.ceil(len(prs_names)/cols)),2)
    fig, ax = plt.subplots(rows ,cols,figsize=((cols+1)*15, 12*rows))
    df_all=pd.DataFrame()
    for i, prs_name in enumerate(prs_names):   
        prs_title="_".join(prs_name.split("_")[:-2])
        for j, imp in enumerate(imps):
            linestyle="solid" # ("solid" if imp.endswith("eur") else "dotted" if  "imputeX" in imp else "dashed")
            cur_curve=df[(df.loc[:,"imp"]==imp) & (df.loc[:,"prs_name"]==prs_name)]
            if cur_curve.loc[:,field_name].shape[0] >-1:
                ax[i//cols][i % cols].plot(cur_curve.loc[:,"hyperparameter"], cur_curve.loc[:,field_name], label=f'{d_imp_names.get(imp,imp)}', linestyle=linestyle, linewidth=4, color=cs[l_imps.index(imp)])
                for t in cur_curve.loc[:,"hyperparameter"]:
                    df_all.loc[f'{d_prs_names.get(prs_title,prs_title)}/{prs_name.split("_")[-1]}/{t}', f'{d_imp_names.get(imp,imp)}']=cur_curve.loc[cur_curve.loc[:,'hyperparameter']==t,field_name].max()

        target_title="_".join(prs_name.split("_")[-2:])
        ax[i//cols][i % cols].set_title(f'{d_prs_names.get(prs_title,prs_title)}/{d_target_names.get(target_title,target_title)}')
        ax[i//cols][i % cols].set_xlabel("hyperparameter")
        ax[i//cols][i % cols].set_xticklabels(cur_curve.loc[:,"hyperparameter"], rotation=60)
        ax[i//cols][i % cols].set_ylabel(" ".join(metric_name.split('_')))
        ax[i//cols][i % cols].legend()
        print(ax[i//cols][i % cols].get_xticks())
        print(ax[i//cols][i % cols].get_xticklabels())

    plt.subplots_adjust(right=0.7)
    # plt.tight_layout()
    ax[-1][-1].legend(loc=(0.95,0))
    plt.savefig(os.path.join(constants.FIGURES_PATH, f"{metric_name}_{out_suffix}.png"))
    df_all.to_csv(os.path.join(constants.OUTPUT_PATH, f"{metric_name}_{out_suffix}.tsv"), sep='\t')
