import random
random.seed(42)
import time
import pandas as pd
import numpy as np
np.random.seed(42)
import constants
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams["xtick.labelsize"]=20
matplotlib.rcParams["ytick.labelsize"]=20
import seaborn as sns
sns.set_style('white')
sns.set_style('ticks')
# import bcolz
import pandas
# import allel 
import pickle
import multiprocess
import os 
import argparse
import functools
import scipy 
import matplotlib
        
if __name__=='__main__':    
   
    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-d', '--gwass', dest='gwass', help='', default="LH_PGC-SCZ-EAS")
    parser.add_argument('-t', '--targets', dest='targets',  default="chrs_full", help='')    
    parser.add_argument('-i', '--imp', dest='imp', default="original", help='') 
    parser.add_argument('-th', '--thresholds', dest='thresholds', default="0.001,0.05,0.1,0.2,0.5,1.0", help='')    
    parser.add_argument('-ep', '--excluded_pop', dest='excluded_pop', default="", help='')   # UR,BEB,PJL,MSL,ASW,ACB,CEU
    parser.add_argument('-ip', '--included_pop', dest='included_pop', default="", help='')   # UR,BEB,PJL,MSL,ASW,ACB,CEU 
    parser.add_argument('-es', '--excluded_samples', dest='excluded_samples', default="", help='')   # UR,BEB,PJL,MSL,ASW,ACB,CEU
    parser.add_argument('-is', '--included_samples', dest='included_samples', default="", help='')   # UR,BEB,PJL,MSL,ASW,ACB,CEU 


    args = parser.parse_args()

    gwass=args.gwass.split(',')
    imp=args.imp
    targets=args.targets.split(',')
    thresholds=args.thresholds.split(',')
    excluded_populations=args.excluded_pop.split(',') if args.excluded_pop != "" else []
    included_populations=args.included_pop.split(',') if args.included_pop != "" else []
    excluded_samples=pd.read_csv(args.excluded_samples, sep='\t', index_col=0).iloc[:,0].values if args.excluded_samples != "" else []
    included_samples=pd.read_csv(args.included_samples, sep='\t', index_col=0).iloc[:,0].values if args.included_samples != "" else []
    for th in thresholds:    
        for discovery in gwass:         
            for target in targets:
           
                print(f'{discovery}_{target}')
   
                pop_panel_path=os.path.join(constants.DATASETS_PATH,target, 'pop.panel')
                df_samples_md=pd.read_csv(os.path.join(constants.DATASETS_PATH,target, imp, 'ds.fam'), delim_whitespace=True, header=None)
                df_samples_md.index=df_samples_md.iloc[:,1]
                df_samples_md.loc[:,'super_pop']=target
                df_samples_md.loc[:,'pop']=target
                if os.path.exists(pop_panel_path):
                    df_samples_md=pd.read_csv(pop_panel_path, sep='\t', index_col=1)

                df=pd.read_csv(os.path.join(constants.PRSS_PATH, f'{discovery}_{target}',imp, f'prs.{th}.profile'), delim_whitespace=True, index_col=1)
                print(df.index) 
                if len(included_populations):
                    print(f'here: {included_populations}')
                    df=df.reindex(df_samples_md.loc[:,'pop'][df_samples_md.loc[:,'pop'].isin(included_populations)].index.values).dropna()
                df=df.reindex(df_samples_md.loc[:,'pop'][~df_samples_md.loc[:,'pop'].isin(excluded_populations)].index.values).dropna()
                print(df.index)
                if len(included_samples):
                    # print(included_samples)
                    df=df.reindex(included_samples).dropna()
                print(df.index)
                df=df.drop(excluded_samples)
                print(df.index)
                super_populations=df_samples_md.loc[df.index, 'super_pop']
                populations=df_samples_md.loc[df.index, 'pop']
 
                pd.Series(index=df.index, data=df.index).to_csv(os.path.join(constants.DATASETS_PATH, target, imp, "ds.included_pop.populations"), sep='\t', header=False)
       
                super_populations_unique=np.unique(super_populations.values)
                super_pop_means=[]
                super_pop_stds=[]
                pop_means=[]
                pop_stds=[]
                fig, ax = plt.subplots(1,1,figsize=(15,15))
                ax2=ax.twinx()
                ar_vals=[]
                vals_max=-100
                vals_min=100
                super_to_pop={}
                color_palettes=['PiYG_0_0.4',  'PiYG_0.6_1', 'PuOr_0_0.4', 'PuOr_0.6_1', 'bwr_0_0.4', 'bwr_0.6_1', 'spring_0_0.4', 'spring_0.6_1', 'cool_0_0.4', 'cool_0.6_1', 'RdGy_0_0.4', 'RdGy_0.6_1', 'bone_0_0.4', 'bone_0.6_1', 'pink_0_0.4', 'pink_0.6_1', 'summer_0_0.4', 'summer_0.6_1', 'copper_0_0.4', 'copper_0.6_1']

                color_palette_dict={}
                print(f'unique_super_population: {super_populations_unique}')
                for i, a in enumerate(super_populations_unique):
                    color_palette_dict[a]=color_palettes[i]
                    super_to_pop[a]=[]

                xlim_range=df.loc[:,'SCORE'].max()-df.loc[:,'SCORE'].min()
                xlim=(df.loc[:,'SCORE'].min()-xlim_range*0.1, df.loc[:,'SCORE'].max()+xlim_range*0.1)
                print(xlim)
                bins=np.arange(xlim[0], xlim[1]+xlim_range*1.2*0.01, xlim_range*1.2*0.01)
                # ax.hist(vals, stacked=True, label=pop, bins=bins, color=sns.color_palette("dark", 8)[i])    
                # ar_vals.append(vals)
                # xlim=my_axes.get_xlim()
                # sec_ax = my_axes.twinx()
                # sns.kdeplot(vals, ax=sec_ax, bw=(xlim[1]-xlim[0])/20, color=sns.color_palette("dark", 8)[i])
                # sec_ax.set_yticks([])

                if True:

                    pop_to_super={}
                    populations_unique=np.unique(populations.values) 
                    for i, pop in enumerate(populations_unique):
                        super_pop=df_samples_md[df_samples_md.loc[:,'pop']==pop].iloc[0].loc['super_pop']
                        super_to_pop[super_pop].append(pop) 
                        pop_to_super[pop]=super_pop
                     
                    populations_unique=functools.reduce(lambda q,w: q+w, [a for a in super_to_pop.values()])
                    for i, pop in enumerate(populations_unique): # enumerate(populations_unique):
                        df_p=df.reindex(populations[populations==pop].index).loc[:,'SCORE']
                        # print(df_p)
                        vals=df_p[np.logical_and(~df_p.isnull().values, ~np.isinf(df_p.values))]
                        pop_means.append(vals.mean())
                        pop_stds.append(vals.std())                    
                        ar_vals.append(vals)
                        print(f'{pop}  {vals.shape} {df_p.shape}')
                        # print(vals)
                        # ax.hist(vals, stacked=True, bins=bins, color=sns.color_palette("pastel", 8)[i], label=pop)              
                        # sns.kdeplot(vals, ax=sec_ax, bw=(xlim[1]-xlim[0])/20, label=pop, color=sns.color_palette("pastel", 8)[i])
                        # sec_ax.set_yticks([])

                print(len(ar_vals))
                colors=[]
                for pop in populations_unique:
                    c=color_palette_dict[pop_to_super[pop]].split('_')[0]
                    s=float(color_palette_dict[pop_to_super[pop]].split('_')[1])*1
                    e=float(color_palette_dict[pop_to_super[pop]].split('_')[2])*1
                    colors.append(matplotlib.cm.get_cmap(c)(s+(e-s)*super_to_pop[pop_to_super[pop]].index(pop)/float(len(super_to_pop[pop_to_super[pop]]))))
                    print(matplotlib.cm.get_cmap(c)(s+(e-s)*super_to_pop[pop_to_super[pop]].index(pop)/float(len(super_to_pop[pop_to_super[pop]]))))
                    # colors.append(sns.color_palette(color_palette_dict[pop_to_super[pop]], len(super_to_pop[pop_to_super[pop]]))[super_to_pop[pop_to_super[pop]].index(pop)])

                 
                ax.hist(ar_vals, stacked=True, histtype='bar', bins=bins, color=colors, label=populations_unique)
                ax2.set_yticks([]) 
                ax.set_xlim(xlim)
                # sec_ax.set_xlim(xlim)
 
                for i, pop in enumerate(super_populations_unique):
                    print(df.index) 
                    df_p=df.reindex(super_populations[super_populations==pop].index).loc[:,'SCORE'].dropna()
                    vals=df_p[~np.isinf(df_p.values)]
                    print(f'df_p {pop} shape {vals.shape}')
                    if vals.shape[0] < 2: 
                        super_pop_means.append(0)
                        super_pop_stds.append(0)
                        continue                   
                    super_pop_means.append(vals.mean())
                    super_pop_stds.append(vals.std())                    
#                     sns.distplot(vals, label=pop, hist=False, norm_hist=False, kde_kws={'lw':6}, ax=ax2, color=sns.color_palette(color_palette_dict[pop], 2)[1])
                    ks=scipy.stats.gaussian_kde(vals)
                    ind = np.linspace(ax.get_xlim()[0], ax.get_xlim()[1], 101)
                    kdepdf = ks.evaluate(ind)
                    c=color_palette_dict[pop].split('_')[0]
                    s=float(color_palette_dict[pop].split('_')[1])*1
                    e=float(color_palette_dict[pop].split('_')[2])*1
                    color=matplotlib.cm.get_cmap(c)(s+(e-s)*0.5)
                    ax2.plot(ind, kdepdf,lw=6, color=color, label=f'{pop} (n={len(vals)})')
                
                ax2.set_ylim(0, ax2.get_ylim()[1])


                pd.Series(super_pop_means, index=super_populations_unique).to_csv(os.path.join(constants.OUTPUT_PATH, f'dist_super_pop_means_{discovery}_{target}_{th}.tsv'), sep='\t')
                pd.Series(super_pop_stds, index=super_populations_unique).to_csv(os.path.join(constants.OUTPUT_PATH, f'dist_super_pop_stds_{discovery}_{target}_{th}.tsv'), sep='\t')
                pd.Series(pop_means, index=populations_unique).to_csv(os.path.join(constants.OUTPUT_PATH, f'dist_pop_means_{discovery}_{target}_{th}.tsv'), sep='\t')
                pd.Series(pop_stds, index=populations_unique).to_csv(os.path.join(constants.OUTPUT_PATH, f'dist_pop_stds_{discovery}_{target}_{th}.tsv'), sep='\t')
            ax.legend(loc='upper left', ncol=1, fontsize=20)
            ax2.legend(loc='upper right', ncol=1, fontsize=20)
            plt.savefig(os.path.join(constants.FIGURES_PATH, f'dists_by_pop_{discovery}_{target}_{imp}_{th}.png'))
            plt.clf()
