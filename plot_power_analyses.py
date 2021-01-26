import pandas as pd
import numpy as np
import os
import subprocess
import constants
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

pheno_src_path='/specific/netapp5/gaga/gaga-pd/prs_data/datasets/dec/ukbb/pheno_bc_only_scn_w.tsv'
pheno_dest_path='/specific/netapp5/gaga/gaga-pd/prs_data/datasets/dec/ukbb/pheno'
n_iterations=100
ar_n_samples=[200, 300, 400, 500 , 750, 1000, 1500] #  ,2000, 2500, 3000, 4000, 5000]
ar_prevalences=[0.05, 0.1, 0.25, 0.5]
discovery='D_bca_michailidou_2017'
target='ukbb'
imp='imputeX'
scripts_path='/specific/elkon/hagailevi/PRS/codebase'


res_by_prevalences={}
res_by_n_samples={}
for prevalence in ar_prevalences:
     res_by_prevalences[prevalence]=[]

for n_samples in ar_n_samples:
     res_by_n_samples[n_samples]=[]

df=pd.read_csv(pheno_src_path, sep='\t', index_col=0)
for n_samples in ar_n_samples:
    for prevalence in ar_prevalences:
        df_all_statistics=pd.read_csv(os.path.join(constants.OUTPUT_PATH, f'agg_statistics_{discovery}_{target}_{imp}_{n_iterations}_{n_samples}_{prevalence}.tsv'), sep='\t')       
        stat_mn=df_all_statistics.mean().round(2)
        stat_std=df_all_statistics.std().round(2)
        res_by_n_samples[n_samples].append((stat_mn,stat_std))
        res_by_prevalences[prevalence].append((stat_mn,stat_std))
        # print(stat_mn)


fig,axs = plt.subplots(2,3,figsize=(30,20))
for k in res_by_n_samples:
    p=axs[0][0].plot(ar_prevalences, [cur[0].loc['or_all'] for cur in res_by_n_samples[k]], linestyle='-', marker='o', label=f'# of samples={k}') 
    axs[0][0].errorbar(ar_prevalences, [cur[0].loc['or_all'] for cur in res_by_n_samples[k]], yerr=[cur[1].loc['or_all'] for cur in res_by_n_samples[k]], color=p[0].get_color(), capsize=5, ls='None', elinewidth=0.5, label='_nolegend_', marker="_")
    axs[0][0].set_xlabel("cohort size")
    axs[0][0].set_ylabel("mean OR per 1 SD")
    axs[0][0].set_title("logistic OR per 1 SD")

    p=axs[0][1].plot(ar_prevalences, [cur[0].loc['or_95'] for cur in res_by_n_samples[k]], label=f'# of samples={k}', linestyle='-', marker='o')
    axs[0][1].errorbar(ar_prevalences, [cur[0].loc['or_95'] for cur in res_by_n_samples[k]], yerr=[cur[1].loc['or_95'] for cur in res_by_n_samples[k]], color=p[0].get_color(), capsize=5, ls='None', elinewidth=0.5, label='_nolegend_', marker="_")
    axs[0][1].yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())
    axs[0][1].yaxis.grid(True, which='both')
    axs[0][1].set_xlabel("cohort size")
    axs[0][1].set_ylabel("mean OR")
    axs[0][1].set_title("OR (95-99%)/(40-60%)")
    
    p=axs[0][2].plot(ar_prevalences, [cur[0].loc['or_99'] for cur in res_by_n_samples[k]], label=f'# of samples={k}', linestyle='-', marker='o')
    axs[0][2].errorbar(ar_prevalences, [cur[0].loc['or_99'] for cur in res_by_n_samples[k]], yerr=[cur[1].loc['or_99'] for cur in res_by_n_samples[k]], color=p[0].get_color(), capsize=5, ls='None', elinewidth=0.5, label='_nolegend_', marker="_")
    axs[0][2].yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())
    axs[0][2].yaxis.grid(True, which='both')
    axs[0][2].set_xlabel("cohort size")
    axs[0][2].set_ylabel("mean OR")
    axs[0][2].set_title("OR (99-100%)/(40-60%)")

    p=axs[1][0].plot(ar_prevalences, [cur[0].loc['power'] for cur in res_by_n_samples[k]], label=f'# of samples={k}', linestyle='-', marker='o')
    axs[1][0].errorbar(ar_prevalences, [cur[0].loc['power'] for cur in res_by_n_samples[k]], yerr=[cur[1].loc['power'] for cur in res_by_n_samples[k]], color=p[0].get_color(), capsize=5, ls='None', elinewidth=0.5, label='_nolegend_', marker="_")
    axs[1][0].set_xlabel("cohort size")
    axs[1][0].set_ylabel("mean power")
    axs[1][0].set_title("power OR logistic")

    p=axs[1][1].plot(ar_prevalences, [cur[0].loc['or_95_power'] for cur in res_by_n_samples[k]], label=f'# of samples={k}', linestyle='-', marker='o')
    axs[1][1].errorbar(ar_prevalences, [cur[0].loc['or_95_power'] for cur in res_by_n_samples[k]], yerr=[cur[1].loc['or_95_power'] for cur in res_by_n_samples[k]], color=p[0].get_color(), capsize=5, ls='None', elinewidth=0.5, label='_nolegend_', marker="_")
    axs[1][1].set_xlabel("cohort size")
    axs[1][1].set_ylabel("mean power")
    axs[1][1].set_title("power OR (95-99%)/(40-60%)")

    p=axs[1][2].plot(ar_prevalences, [cur[0].loc['or_99_power'] for cur in res_by_n_samples[k]], label=f'# of samples={k}', linestyle='-', marker='o')
    axs[1][2].errorbar(ar_prevalences, [cur[0].loc['or_99_power'] for cur in res_by_n_samples[k]], yerr=[cur[1].loc['or_99_power'] for cur in res_by_n_samples[k]], color=p[0].get_color(), capsize=5, ls='None', elinewidth=0.5, label='_nolegend_', marker="_")
    axs[1][2].set_xlabel("cohort size")
    axs[1][2].set_ylabel("mean power")
    axs[1][2].set_title("power OR (99-100%)/(40-60%)")


plt.legend(loc=(1.1,0.9))
plt.savefig(os.path.join(constants.FIGURES_PATH, "res_by_prevalences.png"))


fig,axs = plt.subplots(2,3,figsize=(30,20))
for k in res_by_prevalences:
    p=axs[0][0].plot(ar_n_samples, [cur[0].loc['or_all'] for cur in res_by_prevalences[k]], linestyle='-', marker='o', label=f'prevalence={k}')
    axs[0][0].errorbar(ar_n_samples, [cur[0].loc['or_all'] for cur in res_by_prevalences[k]], yerr=[cur[1].loc['or_all'] for cur in res_by_prevalences[k]], color=p[0].get_color(), capsize=5, ls='None', elinewidth=0.5, label='_nolegend_', marker="_")
    axs[0][0].set_xlabel("prevalence")
    axs[0][0].set_ylabel("OR per 1 SD")
    axs[0][0].set_title("logistic OR per 1 SD")

    p=axs[0][1].plot(ar_n_samples, [cur[0].loc['or_95'] for cur in res_by_prevalences[k]], label=f'prevalence={k}', linestyle='-', marker='o')
    axs[0][1].errorbar(ar_n_samples, [cur[0].loc['or_95'] for cur in res_by_prevalences[k]], yerr=[cur[1].loc['or_95'] for cur in res_by_prevalences[k]], color=p[0].get_color(), capsize=5, ls='None', elinewidth=0.5, label='_nolegend_', marker="_")
    axs[0][1].yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())
    axs[0][1].yaxis.grid(True, which='both')
    axs[0][1].set_xlabel("prevalence")
    axs[0][1].set_ylabel("OR")
    axs[0][1].set_title("OR (95-99%)/(40-60%)")

    p=axs[0][2].plot(ar_n_samples, [cur[0].loc['or_99'] for cur in res_by_prevalences[k]], label=f'prevalence={k}', linestyle='-', marker='o')
    axs[0][2].errorbar(ar_n_samples, [cur[0].loc['or_99'] for cur in res_by_prevalences[k]], yerr=[cur[1].loc['or_99'] for cur in res_by_prevalences[k]], color=p[0].get_color(), capsize=5, ls='None', elinewidth=0.5, label='_nolegend_', marker="_")
    axs[0][2].yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())
    axs[0][2].yaxis.grid(True, which='both')
    axs[0][2].set_xlabel("prevalence")
    axs[0][2].set_ylabel("OR")
    axs[0][2].set_title("OR (99-100%)/(40-60%)")

    p=axs[1][0].plot(ar_n_samples, [cur[0].loc['power'] for cur in res_by_prevalences[k]], label=f'prevalence={k}', linestyle='-', marker='o')
    axs[1][0].errorbar(ar_n_samples, [cur[0].loc['power'] for cur in res_by_prevalences[k]], yerr=[cur[1].loc['power'] for cur in res_by_prevalences[k]], color=p[0].get_color(), capsize=5, ls='None', elinewidth=0.5, label='_nolegend_', marker="_")
    axs[1][0].set_xlabel("prevalence")
    axs[1][0].set_ylabel("mean power")
    axs[1][0].set_title("power OR logistic")

    p=axs[1][1].plot(ar_n_samples, [cur[0].loc['or_95_power'] for cur in res_by_prevalences[k]], label=f'prevalence={k}', linestyle='-', marker='o')
    axs[1][1].errorbar(ar_n_samples, [cur[0].loc['or_95_power'] for cur in res_by_prevalences[k]], yerr=[cur[1].loc['or_95_power'] for cur in res_by_prevalences[k]], color=p[0].get_color(), capsize=5, ls='None', elinewidth=0.5, label='_nolegend_', marker="_")
    axs[1][1].set_xlabel("prevalence")
    axs[1][1].set_ylabel("mean power")
    axs[1][1].set_title("power OR (95-99%)/(40-60%)")

    p=axs[1][2].plot(ar_n_samples, [cur[0].loc['or_99_power'] for cur in res_by_prevalences[k]], label=f'prevalence={k}', linestyle='-', marker='o')
    axs[1][2].errorbar(ar_n_samples, [cur[0].loc['or_99_power'] for cur in res_by_prevalences[k]], yerr=[cur[1].loc['or_99_power'] for cur in res_by_prevalences[k]], color=p[0].get_color(), capsize=5, ls='None', elinewidth=0.5, label='_nolegend_', marker="_")
    axs[1][2].set_xlabel("prevalence")
    axs[1][2].set_ylabel("mean power")
    axs[1][2].set_title("power OR (99-100%)/(40-60%)")


plt.legend(loc=(1.1,0.9))
plt.savefig(os.path.join(constants.FIGURES_PATH, "res_by_n_samples.png"))

         
        
        
              
        
