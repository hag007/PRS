import random
random.seed(42)
import time
import pandas as pd
import numpy as np
np.random.seed(42)

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('white')
sns.set_style('ticks')
import bcolz
import pandas
import allel 
import pickle
import multiprocess
import os 
import argparse
import scipy
from scipy.stats import friedmanchisquare
import scikit_posthocs as sp

        
if __name__=='__main__':    
   
    BASE_PATH='/specific/elkon/hagailevi/PRS/'
    GWASS_PATH=os.path.join(BASE_PATH,'GWASs/')
    DATASETS_PATH=os.path.join(BASE_PATH, 'datasets/')
    PRSS_PATH=os.path.join(BASE_PATH, 'PRSs/')
    OUTPUT_PATH=os.path.join(BASE_PATH, 'output/')
    FIGURES_PATH=os.path.join(OUTPUT_PATH, 'figures/')

    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-g', '--gwass', dest='gwass', help='', default="LH_PGC-SCZ-EAS")
    parser.add_argument('-t', '--targets', dest='targets',  default="chrs_full,hapmap_r3", help='')    
    parser.add_argument('-th', '--thresholds', dest='thresholds', default="0.001,0.05,0.1,0.2,0.5,1.0", help='')
    parser.add_argument('-p', '--pop_type', dest='pop_type', default="super_pop", help='')   
    parser.add_argument('-ep', '--excluded_pop', dest='excluded_pop', default="", help='')
    parser.add_argument('-ip', '--included_pop', dest='included_pop', default="", help='')
    parser.add_argument('-es', '--excluded_samples', dest='excluded_samples', default="", help='')
    parser.add_argument('-is', '--included_samples', dest='included_samples', default="", help='') 

    args = parser.parse_args()

    gwass=args.gwass.split(',')
    targets=args.targets.split(',')
    thresholds=args.thresholds.split(',')
    included_populations=args.included_pop.split(',')
    excluded_populations=args.excluded_pop.split(',')
    pop_type=args.pop_type

    for th in thresholds:
        pop_type=args.pop_type
        for th in thresholds:    
            df_means=pd.DataFrame()
            df_stds=pd.DataFrame()
            df_ranks=pd.DataFrame()
            df_corr=pd.DataFrame()
            for discovery in gwass:         
                for target in targets:
           
                    s_means=pd.read_csv(os.path.join(OUTPUT_PATH, f'dist_{pop_type}_means_{discovery}_{target}_{th}.tsv'), sep='\t', index_col=0).iloc[:,0].to_frame(f'{discovery}_{target}').rename(index={'MEX' : 'MXL'}).dropna()    
                    df_means=pd.concat([df_means, s_means], axis=1)
                    df_ranks=pd.concat([df_ranks, s_means.apply(lambda a: s_means.shape[0]-scipy.stats.rankdata(s_means))], axis=1)
                    s_stds=pd.read_csv(os.path.join(OUTPUT_PATH, f'dist_{pop_type}_stds_{discovery}_{target}_{th}.tsv'), sep='\t', index_col=0).iloc[:,0].to_frame(f'{discovery}_{target}').rename(index={'MEX' : 'MXL'})
                    df_stds=pd.concat([df_stds, s_stds], axis=1)
        
                
                for i, target_1 in enumerate(targets):
                    for j, target_2 in enumerate(targets[i+1:]):
                        print(f"{df_means.loc[:,f'{discovery}_{target_1}']}, {df_means.loc[:,f'{discovery}_{target_2}']}")
                        df_corr.loc[discovery, f'{target_1}_{target_2}_r']=scipy.stats.pearsonr(df_means.loc[:,f'{discovery}_{target_1}'], df_means.loc[:,f'{discovery}_{target_2}'])[0]
                        df_corr.loc[discovery, f'{target_1}_{target_2}_p']=scipy.stats.pearsonr(df_means.loc[:,f'{discovery}_{target_1}'], df_means.loc[:,f'{discovery}_{target_2}'])[1] 
            df_stds.to_csv(os.path.join(OUTPUT_PATH, f'dist_{pop_type}_stds_{th}.tsv'), sep='\t')                  
            df_means.to_csv(os.path.join(OUTPUT_PATH, f'dist_{pop_type}_means_{th}.tsv'), sep='\t')
            df_ranks.to_csv(os.path.join(OUTPUT_PATH, f'dist_{pop_type}_ranks_{th}.tsv'), sep='\t') 
            df_corr.to_csv(os.path.join(OUTPUT_PATH, f'dist_{pop_type}_corr_{th}.tsv'), '\t') 
        #         print(df_means.values)
        #         friedman=friedmanchisquare(*df_means.values)
        #         print(friedman)
        #         posthoc_conover=sp.posthoc_conover_friedman(df_means, p_adjust="fdr_bh")
        #         print(posthoc_conover) # post_conover.to_csv()) 
        #         wilcoxon_posthoc = sp.posthoc_wilcoxon(df_means, p_adjust="fdr_bh")
        #         print(wilcoxon_posthoc)
