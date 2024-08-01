import random
random.seed(42)
import pandas as pd
import numpy as np
np.random.seed(42)
import constants
import matplotlib.pyplot as plt
import matplotlib
font = {'size'   : 40}
matplotlib.rc('font', **font)
import seaborn as sns
sns.set_style('white')
sns.set_style('ticks')
import os
import argparse
import functools
import scipy as sp

if __name__=='__main__':

    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-d', '--gwass', dest='gwass', help='', default="PC_glcm_craig_2020")
    parser.add_argument('-t', '--targets', dest='targets',  default="ukb_afr", help='')
    parser.add_argument('-i', '--imp', dest='imp', default="imputeX", help='')
    parser.add_argument('-th', '--thresholds', dest='thresholds', default="-1", help='')     # 0.001,0.05,0.1,0.2,0.5
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
                df_samples_md=pd.read_csv(os.path.join(constants.DATASETS_PATH,target, imp, 'ds.QC.fam'), delim_whitespace=True, header=None)
                df_samples_md.index=df_samples_md.iloc[:,1]
                df_samples_md.loc[:,'super_pop']=target
                df_samples_md.loc[:,'pop']=target
                if os.path.exists(pop_panel_path):
                    df_samples_md=pd.read_csv(pop_panel_path, sep='\t', index_col=0)
                    df_samples_md.index=df_samples_md.index.astype(str)

                df_pheno=None


                df_statistics=pd.DataFrame()
                df_or_percentile=pd.DataFrame()
                df_or_p_value=pd.DataFrame()
                df_or_all=pd.DataFrame()
                df=pd.DataFrame()
                rep=105
                rep_start=1
                rep_end=1
                for a in range(rep_start,rep_end+1):
                    if os.path.exists(pheno_path):
                        df_pheno=pd.read_csv(pheno_path, sep='\t') # , index_col=0
                        # df_pheno.index=df_pheno.index.astype(str)
                        df_statistics=pd.concat((df_statistics, pd.read_csv(os.path.join(constants.PRSS_PATH, f'{discovery}_{target}',imp, f"rep_{rep}_{a}", f'prs.cv.ls___5_test.ctrl.statistics.{th}.tsv'), sep='\t'))) # , index_col=0
                        df_or_percentile=pd.concat((df_or_percentile, pd.read_csv(os.path.join(constants.PRSS_PATH, f'{discovery}_{target}',imp,f"rep_{rep}_{a}",f'prs.cv.ls___5_test.ctrl.or.percentile.{th}.tsv'), sep='\t')))
                        df_or_p_value=pd.concat((df_or_p_value, pd.read_csv(os.path.join(constants.PRSS_PATH, f'{discovery}_{target}',imp,f"rep_{rep}_{a}",f'prs.cv.ls___5_test.ctrl.or.p.value.{th}.tsv'), sep='\t')))
                        df_or_all=pd.concat((df_or_all, pd.read_csv(os.path.join(constants.PRSS_PATH, f'{discovery}_{target}',imp,f"rep_{rep}_{a}",f'prs.cv.ls___5_test.ctrl.or.all.{th}.tsv'), sep='\t')))

                    # print(os.path.join(constants.PRSS_PATH, f'{discovery}_{target}',imp, "rep_72", f'prs.cv.ls___5_test{"."+th if th!="" else ""}.profile'))
                    df_prs=pd.read_csv(os.path.join(constants.PRSS_PATH, f'{discovery}_{target}',imp, f"rep_105_{a}", f'prs.cv.ls___5_test{"."+th if th!="" else ""}.profile'), delim_whitespace=True)
                    df_prs.loc[:,'SCORE']=sp.stats.zscore(df_prs.loc[:,'SCORE'])
                    df=pd.concat((df, df_prs)) # , index_col=0



                # df.index=df.index.astype(str)
                print(df.index)

                if len(included_populations):
                    df=df.reindex(df_samples_md.loc[:,'pop'][df_samples_md.loc[:,'pop'].isin(included_populations)].index.values).dropna()

                if len(excluded_populations):
                    df=df.reindex(df_samples_md.loc[:,'pop'][~df_samples_md.loc[:,'pop'].isin(excluded_populations)].index.values).dropna()
                if len(included_samples):
                    df=df.reindex(included_samples).dropna()
                print(df.iloc[:,0])
                df=df.drop(excluded_samples)

                super_populations=df_samples_md.loc[df.iloc[:,0], 'super_pop']
                populations=df_samples_md.loc[df.iloc[:,0], 'pop']

                # pd.Series(index=df.iloc[:,0], data=df.iloc[:,0]).to_csv(os.path.join(constants.DATASETS_PATH, target, imp, "ds.included_pop.populations"), sep='\t', header=False)

                super_populations_unique=np.unique(super_populations.values)
                super_pop_means=[]
                super_pop_stds=[]
                pop_means=[]
                pop_stds=[]
                fig, ax = plt.subplots(1,1,figsize=(30,20))
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
                        if len(populations_unique)>1:
                            df_p=df.reindex(populations[populations==pop].index)
                        else:
                            df_p=df

                        pop_vals=df_p[np.logical_and(~df_p.loc[:,'SCORE'].isnull().values, ~np.isinf(df_p.loc[:,'SCORE'].values))]
                        super_pop_means.append(pop_vals.mean())
                        super_pop_stds.append(pop_vals.std())
                        print("pop_vals shape:", np.unique(pop_vals.loc[:,'FID']).shape)
                        print("df_pheno shape:", np.unique(df_pheno.loc[:,'FID']).shape)
                        if not df_pheno is None:
                            df_cur_pheno=  pd.merge(pop_vals, df_pheno, on='FID').dropna()
                            print("df_cur_pheno shape:", np.unique(df_cur_pheno.loc[:,'FID']).shape)
                            unique_pheno=np.unique(df_cur_pheno.loc[:, 'label'].values)
                            for cur_pheno_val in unique_pheno:
                                cur_pheno_val=int(cur_pheno_val)
                                # print("cur_pheno_val: ", cur_pheno_val)
                                # if (cur_pheno_val<2): continue
                                df_cur_pheno_by_val = df_cur_pheno[df_cur_pheno.loc[:, 'label']==cur_pheno_val]
                                clr = plt.cm.Reds(cur_pheno_val/np.max(unique_pheno))
                                # print("df_cur_pheno_by_val", df_cur_pheno_by_val)
                                cur_pop_by_pheno_val=pop_vals[pop_vals.iloc[:,0].isin(df_cur_pheno_by_val.iloc[:, 0])]
                                # print("shape 0:", df_cur_pheno.shape)
                                # print("shape 1:", df_cur_pheno[df_cur_pheno.loc[:, 'label']==1].shape)
                                # print("shape 2:", df_cur_pheno[df_cur_pheno.loc[:, 'label']==2].shape)
                                # print("cur_pop_by_pheno_val shape", cur_pop_by_pheno_val.shape)

                                cur_pop_by_pheno_vals.append(cur_pop_by_pheno_val.loc[:,'SCORE'])
                                colors.append(plt.cm.Reds(20+cur_pheno_val*80))
                    # print("cur_pop_by_pheno_vals shapes: ", cur_pop_by_pheno_vals[0].shape, cur_pop_by_pheno_vals[1].shape)
                    ax.hist(cur_pop_by_pheno_vals, stacked=True, histtype='bar', bins=bins, color=colors)
                    ax.set_xlim(np.array(xlim))

                for i, pop in enumerate(super_populations_unique):
                    print(f"pop: {pop}")
                    if len(super_populations_unique)>1:
                        df_p=df.reindex(super_populations[super_populations==pop].index.astype(str)).loc[:,'SCORE']
                    else:
                        df_p=df
                    pop_vals=df_p[~np.isinf(df_p.loc[:,'SCORE'].values)]
                    super_pop_means.append(pop_vals.loc[:,'SCORE'].mean())
                    super_pop_stds.append(pop_vals.loc[:,'SCORE'].std())
                    if not df_pheno is None:
                        df_cur_pheno=pd.merge(pop_vals, df_pheno, on='FID').dropna() # df_pheno.reindex(pop_vals.index).loc[:, 'label'].dropna()

                        unique_pheno=np.unique(df_cur_pheno.loc[:,'label'].values)
                        for cur_pheno_val in unique_pheno:
                            cur_pheno_val=int(cur_pheno_val)
                            if (cur_pheno_val==-1): continue
                            df_cur_pheno_by_val = df_cur_pheno[df_cur_pheno.loc[:, 'label']==cur_pheno_val]

                            clr = plt.cm.Reds(int(20+cur_pheno_val*80))
                            cur_pop_by_pheno_val=pop_vals[pop_vals.iloc[:,0].isin(df_cur_pheno_by_val.iloc[:, 0])] # pop_vals.reindex(df_cur_pheno_by_val.index)
                            ks=sp.stats.gaussian_kde(cur_pop_by_pheno_val.loc[:,"SCORE"].values)
                            ind = np.linspace(ax.get_xlim()[0], ax.get_xlim()[1], 101)
                            kdepdf = ks.evaluate(ind)
                            if set(unique_pheno)==set([1,2]):
                                label=("case" if cur_pheno_val==2 else "control")
                            else:
                                label=f'label={cur_pheno_val}'
                            ax2.plot(ind, kdepdf,lw=6, color=clr, label= f'{label} (n={cur_pop_by_pheno_val.values.shape[0]})')

                ax2.set_ylim(0, ax2.get_ylim()[1])

            plt.subplots_adjust(right=0.7)
            ax.set_ylabel("# of individuals (bars)")
            ax2.set_ylabel("KDE")
            ax.set_ylabel("# individuals")
            ax.set_xlabel('Normalized Risk score')
            plt.setp(ax.get_xticklabels(), rotation=35)
            ax2.legend(loc=(1.15,0), ncol=1)

            # th=float(th) if th!='' else 1
            # ax.text(ax.get_xlim()[0] + (ax.get_xlim()[1]-ax.get_xlim()[0])*0.01, ax.get_ylim()[1]*0.8, f" Nagelkerke R2: {'{:.2e}'.format(df_statistics.loc[th,'all_ngkR2'])}\n p-value={'{:.2e}'.format(df_statistics.loc[th,'P'])}\n AUROC: {'{:.2}'.format(df_statistics.loc[th,'roc_auc'])}\n Top 1%: OR={'{:.2f}'.format(df_or_percentile.iloc[-1,0])} (CI: {'{:.2f}'.format(df_or_percentile.iloc[-1,1])} - {'{:.2f}'.format(df_or_percentile.iloc[-1,2])};\n p-value: {'{:.2e}'.format(df_or_p_value.iloc[-1,-1])}) \n Top 5% OR={'{:.2f}'.format(df_or_percentile.iloc[-2,0])} (CI: {'{:.2f}'.format(df_or_percentile.iloc[-2,1])} - {'{:.2f}'.format(df_or_percentile.iloc[-2,2])};\n                                p-value: {'{:.2e}'.format(df_or_p_value.iloc[-2,-1])})\n OR={'{:.2f}'.format(df_or_all.iloc[-1,0])} (CI: {'{:.2f}'.format(df_or_all.iloc[-1,1])} - {'{:.2f}'.format(df_or_all.iloc[-1,2])})", fontsize=22)
            plt.tight_layout()
            plt.savefig(os.path.join(constants.FIGURES_PATH, f'dists_by_pheno_{discovery}_{target}_{imp}{"_"+str(th) if th!="" else ""}.png'))
            plt.clf()
