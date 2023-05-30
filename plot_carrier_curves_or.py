import os

import matplotlib

import constants

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from name_mappings import *
import pandas as pd
pd.options.mode.chained_assignment = None
import seaborn as sns
cs = sns.color_palette("bright")

import utils

font = {'size'   : 30}
matplotlib.rc('font', **font)

def plot_curves(fname_format, metric, x_name, cols=1):

    # d={'or_all':[0.],
    #    'or_99':np.arange(8)/2,}


    fig, axs=plt.subplots(1,2, figsize=(30,15))
    for i, cur_metric in enumerate(["or_all", "or_99"]):
        ax=axs[i]
        for j, cur_set in enumerate(["with_carriers", "without_carriers"]):
            fname=fname_format.format(cur_set)
            df=pd.read_csv(os.path.join(constants.OUTPUT_PATH, fname), sep='\t')
            errbar=pd.concat((df.loc[:,cur_metric]-df.loc[:,f'{cur_metric}_ci_min'], df.loc[:,f'{cur_metric}_ci_max']-df.loc[:,cur_metric]), axis=1).values.T
            ax.errorbar(df.loc[:,"threshold"], df.loc[:,cur_metric], yerr=errbar, capsize=5, marker='o', color=cs[j], alpha=0.4, label=" ".join(cur_set.split("_")))

        ax.legend()
        ax.set_xlabel(x_name)
        ax.set_xscale('log')
        # ax.set_ylim(0, ax.get_ylim()[1])
        ax.set_ylabel("OR")

    plt.savefig(os.path.join(constants.FIGURES_PATH, "prs_carriers.png"))


metric='all' # 'per_1sd'
plot_curves("bcac_onco_aj_pt_{}.tsv", metric, "Hyperparameter (T)") #
