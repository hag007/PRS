import pandas as pd
import numpy as np
import os
import subprocess
import constants
 
pheno_src_path='/specific/netapp5/gaga/gaga-pd/prs_data/datasets/dec/ukbb/pheno_bc_only_scn_w.tsv'
pheno_dest_path='/specific/netapp5/gaga/gaga-pd/prs_data/datasets/dec/ukbb/pheno'
n_iterations=100
ar_n_samples=[200, 300, 400 , 500, 750, 1000, 1500, 2000, 2500, 3000, 4000, 5000]
ar_prevalences=[0.05, 0.1, 0.25, 0.5]
discovery='D_bca_michailidou_2017'
target='ukbb'
imp='imputeX'
scripts_path='/specific/elkon/hagailevi/PRS/codebase'



df=pd.read_csv(pheno_src_path, sep='\t', index_col=0)
for n_samples in ar_n_samples:
    for prevalence in ar_prevalences:
        df_all_statistics=pd.DataFrame()
        for a in np.arange(n_iterations):
            df=df.sample(frac=1)
            df_label1=df[df.loc[:,'label']==1].iloc[np.arange(int(n_samples*prevalence)),:]
            df_label0=df[df.loc[:,'label']==0].iloc[np.arange(int(n_samples*(1-prevalence))),:]
            df_sampled=pd.concat([df_label0,df_label1])
            df_sampled.to_csv(pheno_dest_path, sep='\t')
            subprocess.Popen(f'bash calc_prs_fit.sh --discovery {discovery} --target {target} --imp {imp}', shell=True, stdout=subprocess.PIPE, cwd=scripts_path).stdout.read() 
            df_cur_statistics=pd.read_csv(os.path.join(constants.PRSS_PATH, f'{discovery}_{target}', imp, 'prs.or.summary.tsv'), index_col=0)
            df_all_statistics=pd.concat([df_all_statistics, df_cur_statistics])
        
        df_all_statistics.to_csv(os.path.join(constants.OUTPUT_PATH, f'agg_statistics_{discovery}_{target}_{imp}_{n_iterations}_{n_samples}_{prevalence}.tsv'))
        
        
              
        
