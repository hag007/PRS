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

def plot_percentile_curve(file_name_format, prs_names, imps, cols=3):

    for prs_name in prs_names:
        for imp in imps:
            ths=["0.00000005", "0.001","0.005","0.01","0.05","0.1","0.2","0.3","0.4","0.5"]
            rows=max(int(np.ceil(len(ths)/cols)),2)
            fig, ax = plt.subplots(rows ,cols,figsize=((cols+1)*15, 15*rows))

            for i, th in enumerate(ths):
                df=pd.read_csv(os.path.join(constants.PRSS_PATH,prs_name, imp, file_name_format.format(th)), sep='\t')

                ## X axis position defined by percentile intervals: e.g., converting string "20-30" to (20+30)/2
                df.loc[:,'x_values']=df.iloc[:,0].apply(lambda a: (int(a.split("-")[0])+int(a.split("-")[1]))//2)
                df.sort_values('x_values', inplace=True)
                ax[i//cols][i % cols].plot(df.loc[:,"x_values"], df.loc[:,"OR"], label=f'{d_imp_names.get(imp,imp)}', linewidth=4, color=cs[l_imps.index(imp)])
                ax[i//cols][i % cols].errorbar(df.loc[:,'x_values'], df.loc[:,"OR"], yerr=df.loc[:,["CI min", "CI max"]].values.T, fmt='-o')
                ax[i//cols][i % cols].set_yscale('log')
                ax[i//cols][i % cols].yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
                ax[i//cols][i % cols].set_yticks([0.2,0.5,1,1.5,2,2.5,3,3.5,4,7,10])
                target_title=f"T={th}"
                ax[i//cols][i % cols].set_title(target_title)
            ax[i//cols][i % cols].set_xlabel("percentiles")
            ax[i//cols][i % cols].set_ylabel("OR")
            ax[i//cols][i % cols].legend()

            plt.subplots_adjust(right=0.7)
            ax[-1][-1].legend(loc=(0.95,0))
            plt.savefig(os.path.join(constants.FIGURES_PATH, f"or_percentiles_{prs_name}_{imp}.png"))
    


if __name__=='__main__':

    target="bcac_aj"

    prs_names=[a.format("aj") for a in ["bcac_onco_eur-5pcs_bcac_onco_{}"]]
    imps=[ "impX"]

    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-p', '--prs_names', dest='prs_names', help="", default=",".join(prs_names))
    parser.add_argument('-i', '--imps', dest='imps', help="", default=",".join(imps))
    parser.add_argument('-m', '--metric_name', dest='metric_name', help="", default="OR")
    parser.add_argument('-fn', '--file_name_format', dest='file_name_format', help="", default="prs.or.percentile.{}.tsv") # prs.statistics_summary_{}.tsv

    args = parser.parse_args()
    prs_names=args.prs_names.split(',')
    imps=args.imps.split(',')
    metric_name = args.metric_name
    file_name_format = args.file_name_format
    field_name=metric_name

plot_percentile_curve(file_name_format, prs_names=prs_names, imps=imps)

