import pandas as pd
import numpy as np
import os
import subprocess
import constants
import argparse

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-s', '--pheno_src_path', dest='pheno_src_path', help='', default=os.path.join(constants.DATASETS_PATH, "ukbb","pheno_bc_only_scn_w.tsv"))
    parser.add_argument('-d', '--pheno_dest_path', dest='pheno_dest_path', help="", default=os.path.join(constants.DATASETS_PATH, "ukbb","pheno"))
    parser.add_argument('-i', '--n_iterations', dest='n_iterations', default="100", help='')
    parser.add_argument('-n', '--n_samples', dest='n_samples', default="200, 300, 400, 500, 750, 1000, 1500, 2000, 2500, 3000, 4000, 5000", help='')
    parser.add_argument('-p', '--prevalences', dest='prevalences', default="0.05, 0.1, 0.25, 0.5", help='')
    parser.add_argument('-g', '--discovery', dest='discovery', default="D_bca_michailidou_2017", help='')   # UR,BEB,PJL,MSL,ASW,ACB,CEU
    parser.add_argument('-t', '--target', dest='target', default="ukbb", help='')   # UR,BEB,PJL,MSL,ASW,ACB,CEU
    parser.add_argument('-imp', '--imp', dest='imp', default="imputeX", help='')   # UR,BEB,PJL,MSL,ASW,ACB,CEU
    parser.add_argument('-p', '--scripts_path', dest='scripts_path', default=os.path.join(constants.PUBLIC_BASE_PATH,"codebase"), help='')   # UR,BEB,PJL,MSL,ASW,ACB,CEU

    args = parser.parse_args()
    pheno_src_path=args.pheno_src_path
    pheno_dest_path = args.pheno_dest_path
    n_iterations=int(args.n_iterations)
    ar_n_samples = [int(a) for a in args.n_samples.split(',')]
    ar_prevalences = [float(a) for a in args.prevalences.split(',')]
    discovery=args.discovery
    target = args.target
    imp = args.imp
    scripts_path = args.scripts_path

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




