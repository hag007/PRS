import random
random.seed(42)
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
import os
import argparse
import functools
import scipy
        
if __name__=='__main__':    
   
    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-d', '--gwass', dest='gwass', help='', default="LH_PGC-SCZ-EAS")
    parser.add_argument('-t', '--targets', dest='targets',  default="1kg", help='')    
    parser.add_argument('-i', '--imp', dest='imp', default="original", help='') 
    parser.add_argument('-th', '--thresholds', dest='thresholds', default="0.001,0.05,0.1,0.2,0.5", help='')     # 0.001,0.05,0.1,0.2,0.5
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
   
                pheno_path=os.path.join(constants.DATASETS_PATH,target, 'pheno')
                pop_panel_path=os.path.join(constants.DATASETS_PATH,target, 'pop.panel')
                df_samples_md=pd.read_csv(os.path.join(constants.DATASETS_PATH,target, imp, 'ds.fam'), delim_whitespace=True, header=None)
                df_samples_md.index=df_samples_md.iloc[:,1]
                df_samples_md.loc[:,'super_pop']=target
                df_samples_md.loc[:,'pop']=target
                if os.path.exists(pop_panel_path):
                    df_samples_md=pd.read_csv(pop_panel_path, sep='\t', index_col=0) 
                    df_samples_md.index=df_samples_md.index.astype(str)

                df_pheno=None
                if os.path.exists(pheno_path):
                    df_pheno=pd.read_csv(pheno_path, sep='\t', index_col=0)
                    df_pheno.index=df_pheno.index.astype(str)
                    df_statistics=pd.read_csv(os.path.join(constants.PRSS_PATH, f'{discovery}_{target}',imp,'prs.statistics.tsv'), sep='\t', index_col=0)
                    df_or_percentile=pd.read_csv(os.path.join(constants.PRSS_PATH, f'{discovery}_{target}',imp,'prs.or.percentile.tsv'), sep='\t')
                    df_or_p_value=pd.read_csv(os.path.join(constants.PRSS_PATH, f'{discovery}_{target}',imp,'prs.or.p.value.tsv'), sep='\t')
                    df_or_all=pd.read_csv(os.path.join(constants.PRSS_PATH, f'{discovery}_{target}',imp,'prs.or.all.tsv'), sep='\t')


                df=pd.read_csv(os.path.join(constants.PRSS_PATH, f'{discovery}_{target}',imp, f'prs{"."+th if th!="" else ""}.profile'), delim_whitespace=True, index_col=1)
                df.index=df.index.astype(str)
                if len(included_populations):
                    df=df.reindex(df_samples_md.loc[:,'pop'][df_samples_md.loc[:,'pop'].isin(included_populations)].index.values).dropna()
                df=df.reindex(df_samples_md.loc[:,'pop'][~df_samples_md.loc[:,'pop'].isin(excluded_populations)].index.values).dropna()
                if len(included_samples):
                    df=df.reindex(included_samples).dropna()
                df=df.drop(excluded_samples)
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
                for i, a in enumerate(super_populations_unique):
                    super_to_pop[a]=[]

                xlim_range=df.loc[:,'SCORE'].max()-df.loc[:,'SCORE'].min()
                xlim=(df.loc[:,'SCORE'].min()-xlim_range*0.1, df.loc[:,'SCORE'].max()+xlim_range*0.1)
                bins=np.arange(xlim[0], xlim[1]+xlim_range*1.2*0.01, xlim_range*1.2*0.01)

                if target.startswith('hapmap') or target.startswith('chrs_full')   or True:

                    cur_pop_by_pheno_vals=[]
                    colors=[]
                    pop_to_super={}
                    populations_unique=np.unique(populations.values)  
                    for i, pop in enumerate(populations_unique):
                        super_pop=df_samples_md[df_samples_md.loc[:,'pop']==pop].iloc[0].loc['super_pop']
                        super_to_pop[super_pop].append(pop) 
                        pop_to_super[pop]=super_pop
                     
                    populations_unique=functools.reduce(lambda q,w: q+w, [a for a in super_to_pop.values()])
                    for i, pop in enumerate(populations_unique): # enumerate(populations_unique):
                        df_p=df.reindex(populations[populations==pop].index).loc[:,'SCORE']
                        pop_vals=df_p[np.logical_and(~df_p.isnull().values, ~np.isinf(df_p.values))]
                        super_pop_means.append(pop_vals.mean())
                        super_pop_stds.append(pop_vals.std())
                        if not df_pheno is None:
                            df_cur_pheno=df_pheno.reindex(pop_vals.index).loc[:, 'label'].dropna()
                            unique_pheno=np.unique(df_cur_pheno.values)
                            for cur_pheno_val in unique_pheno:
                                cur_pheno_val=int(cur_pheno_val)
                                if (cur_pheno_val==-1 or cur_pheno_val==0): continue
                                df_cur_pheno_by_val = df_cur_pheno[df_cur_pheno==cur_pheno_val]
                                clr = plt.cm.Reds(cur_pheno_val)
                                cur_pop_by_pheno_val=pop_vals.reindex(df_cur_pheno_by_val.index)
                                cur_pop_by_pheno_vals.append(cur_pop_by_pheno_val)
                                colors.append(plt.cm.Reds(50+cur_pheno_val*100))
                    ax.hist(cur_pop_by_pheno_vals, stacked=True, histtype='bar', bins=bins, color=colors)
                    ax.set_xlim(np.array(xlim))

                for i, pop in enumerate(super_populations_unique):
                    df_p=df.reindex(super_populations[super_populations==pop].index.astype(str)).loc[:,'SCORE']
                    pop_vals=df_p[~np.isinf(df_p.values)]
                    super_pop_means.append(pop_vals.mean())
                    super_pop_stds.append(pop_vals.std())
                    if not df_pheno is None:
                        df_cur_pheno=df_pheno.reindex(pop_vals.index).loc[:, 'label'].dropna()
                        unique_pheno=np.unique(df_cur_pheno.values)
                        for cur_pheno_val in unique_pheno:
                            cur_pheno_val=int(cur_pheno_val)
                            if (cur_pheno_val==-1): continue
                            df_cur_pheno_by_val = df_cur_pheno[df_cur_pheno==cur_pheno_val]
                            clr = plt.cm.Reds(int(50+cur_pheno_val*100))
                            cur_pop_by_pheno_val=pop_vals.reindex(df_cur_pheno_by_val.index)
                            ks=scipy.stats.gaussian_kde(cur_pop_by_pheno_val.values)
                            ind = np.linspace(ax.get_xlim()[0], ax.get_xlim()[1], 101)
                            kdepdf = ks.evaluate(ind)
                            ax2.plot(ind, kdepdf,lw=6, color=clr, label=f'label={cur_pheno_val} (n={cur_pop_by_pheno_val.values.shape[0]})')

                ax2.set_ylim(0, ax2.get_ylim()[1])

            ax.set_ylabel("# of individuals (bars)", fontsize=20)
            ax.set_xlabel("Score", fontsize=20)
            ax2.set_ylabel("KDE", fontsize=20)

            ax2.legend(loc='upper right', fontsize=20, markerscale=3)
            th=float(th) if th!='' else 1 
            ax.text(ax.get_xlim()[0] + (ax.get_xlim()[1]-ax.get_xlim()[0])*0.01, ax.get_ylim()[1]*0.72, f" Nagelkerke R2: {'{:.2e}'.format(df_statistics.loc[th,'all_ngkR2'])}\n p-value={'{:.2e}'.format(df_statistics.loc[th,'P'])}\n AUROC: {'{:.2}'.format(df_statistics.loc[th,'roc_auc'])}\n Top 1%: OR={'{:.2f}'.format(df_or_percentile.iloc[-1,0])} (CI: {'{:.2f}'.format(df_or_percentile.iloc[-1,1])} - {'{:.2f}'.format(df_or_percentile.iloc[-1,2])};\n p-value: {'{:.2e}'.format(df_or_p_value.iloc[-1,-1])}) \n Top 5% OR={'{:.2f}'.format(df_or_percentile.iloc[-2,0])} (CI: {'{:.2f}'.format(df_or_percentile.iloc[-2,1])} - {'{:.2f}'.format(df_or_percentile.iloc[-2,2])};\n                                p-value: {'{:.2e}'.format(df_or_p_value.iloc[-2,-1])})\n OR={'{:.2f}'.format(df_or_all.iloc[-1,0])} (CI: {'{:.2f}'.format(df_or_all.iloc[-1,1])} - {'{:.2f}'.format(df_or_all.iloc[-1,2])})", fontsize=18)
            plt.savefig(os.path.join(constants.FIGURES_PATH, f'dists_by_pheno_{discovery}_{target}_{imp}{"_"+str(th) if th!="" else ""}.png'))
            plt.clf()
