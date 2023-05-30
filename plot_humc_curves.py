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

def plot_curves(fname, y_names, pop, x_name, cols=1):
    fname=fname.format(pop.lower())
    df=pd.read_csv(os.path.join(constants.OUTPUT_PATH, fname), sep='\t')
    fig, ax=plt.subplots(1,1, figsize=(20,20))
    for y_name in y_names:
        ax.plot(df.loc[:,x_name], df.loc[:,y_name], label=y_name, linewidth=4)


    ax.set_xlabel(x_name)
    ax.set_xscale('log')
    ax.set_ylabel("OR per 1SD")
    ax.legend()

    # plt.subplots_adjust(right=0.7)
    # # plt.tight_layout()
    # ax[-1][-1].legend(loc=(0.95,0))
    plt.savefig(os.path.join(constants.FIGURES_PATH, fname.split(".")[0]+".png"))


pop='IL'
plot_curves(f"humc-like_compare_{pop.lower()}.tsv", [f"HUMC-like {pop}",f"BCAC-{pop}"], pop, "Hyperparameter (T)") #
