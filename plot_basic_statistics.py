import pandas as pd
import numpy as np
import os
import subprocess
import constants
import argparse
import simplejson
import seaborn as sns
import functools
import matplotlib.pyplot as plt
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-data', '--data_file', dest='data_file', help="", default=os.path.join(constants.DATASETS_PATH, "ukbb","ukb_code6.csv"))
    args = parser.parse_args()
    data_file=args.data_file
    df_data = pd.read_csv(data_file, sep='\t', index_col=0)
    n_cols=df_data.columns.values.shape[0]

    fig,axs=plt.subplots(int(np.ceil(np.sqrt(n_cols))), int(np.ceil(np.sqrt(n_cols))),figsize=(int(np.ceil(np.sqrt(n_cols))*10),int(np.ceil(np.sqrt(n_cols))*10)))
    for i_a, a in enumerate(df_data.columns):
        cur_ax=axs[int(i_a / np.ceil(np.sqrt(n_cols))), int(i_a % np.ceil(np.sqrt(n_cols)))]
        sns.distplot(np.array(functools.reduce(lambda a,b: a+b, [a.split(',') if type(a)==str else [a] for a in df_data.loc[:,a].dropna()], []), dtype=float), ax=cur_ax, kde=False, norm_hist=False)
        cur_ax.set_title(a)
    plt.savefig(os.path.join(constants.FIGURES_PATH, f"{os.path.basename(data_file).split('.')[0]}_statistics.png"))
