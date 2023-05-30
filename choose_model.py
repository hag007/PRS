import os

import pandas as pd

import constants
import utils
import numpy as np

def choose_model(methods, rep_start, rep_end, suffix):

    df_or_all=pd.DataFrame()
    df_or_99=pd.DataFrame()

    output_fname=f"prs.cv.choose_params.ctrl_{'' if suffix=='' else suffix+'_'}{rep_start}_{rep_end}.tsv"
    base_rep=rep_start.split("_")[0]
    rep_start=int(rep_start.split("_")[1])
    rep_end=int(rep_end.split("_")[1])+1

    for method in methods:
        df_method_or_all=pd.DataFrame()
        df_method_or_99=pd.DataFrame()
        for cur_rep in range(rep_start, rep_end):
            fl_name_or_all = os.path.join(constants.OUTPUT_PATH, f'prs.cv.{method}ctrl_or_all_{suffix}_{base_rep}_{cur_rep}_{base_rep}_{cur_rep}.tsv')
            fl_name_or_99 = os.path.join(constants.OUTPUT_PATH, f'prs.cv.{method}ctrl_or_99_{suffix}_{base_rep}_{cur_rep}_{base_rep}_{cur_rep}.tsv')
            print(f'fl_name_or_all: {fl_name_or_all}')
            if os.path.exists(fl_name_or_all):
                df_all = pd.read_csv(fl_name_or_all, sep='\t')
                df_99 = pd.read_csv(fl_name_or_99, sep='\t')
                print("exists: ",fl_name_or_all)

                sets=df_all.groupby(['prs_name','imp']).count().index
                # print(i)
                for prs_name,imp in sets:
                    # print(prs_name,imp)
                    df_all_filtered=df_all[(df_all.loc[:,'prs_name']==prs_name) & (df_all.loc[:,'imp']==imp)]
                    df_99_filtered=df_99[(df_99.loc[:,'prs_name']==prs_name) & (df_99.loc[:,'imp']==imp)]
                    # print(df_all_filtered)
                    df_all_filtered=df_all_filtered.sort_values(by=["mean"], ascending=False)
                    df_all_filtered.index=df_all_filtered.apply(lambda a: f"{method}_{cur_rep}_{a['hyperparameter']}_{a['prs_name']}_{a['imp']}", axis=1)
                    df_all_filtered.loc[:,'order']=np.arange(1,df_all_filtered.shape[0]+1) * 0.99
                    df_99_filtered=df_99_filtered.sort_values(by=["mean"], ascending=False)
                    df_99_filtered.index=df_99_filtered.apply(lambda a: f"{method}_{cur_rep}_{a['hyperparameter']}_{a['prs_name']}_{a['imp']}", axis=1)
                    df_99_filtered.loc[:,'order']=np.arange(1,df_99_filtered.shape[0]+1)
                    idx=(df_all_filtered.loc[:,'order']+df_99_filtered.loc[:,'order']).idxmin()
                    # df_all.loc[idx]
                    # df_99.loc[idx]
                    print(df_all_filtered.loc[idx].to_frame().T)
                    df_method_or_all = pd.concat((df_method_or_all,  df_all_filtered.loc[idx].to_frame().T),axis=0)
                    # print(df_method_or_99)
                    # print(df_99.loc[idx])
                    df_method_or_99 = pd.concat((df_method_or_99,  df_99_filtered.loc[idx].to_frame().T), axis=0)
        # print(df_method_or_all)
        # print(df_method_or_99)
        # quit()
        # print(df_method_or_all)
        # print(df_method_or_99)
        # df_or_all=df_or_all.append({"method": method,
        #                 "mean_inner_all": df_method_or_all.loc[:,"mean"].mean(),
        #                 "se_inner_all": df_method_or_all.loc[:,"mean"].std(),
        #                 "mean_outer_all": df_method_or_all.loc[:,"mean_test"].mean(),
        #                 "se_outer_all": df_method_or_all.loc[:,"mean_test"].std()/np.sqrt(df_method_or_all.shape[0])}, ignore_index=True)

        print(fl_name_or_all)
        print(df_method_or_all) 
        df_method_or_all.loc[:,'mean']=df_method_or_all.loc[:,'mean'].astype(float)
        df_method_or_all.loc[:,'mean_test']=df_method_or_all.loc[:,'mean_test'].astype(float)
        df_method_or_all.loc[:,'n_snps_mean']=df_method_or_all.loc[:,'n_snps_mean'].astype(float)
        df_method_or_all.loc[:,'n_snps_mean_test']=df_method_or_all.loc[:,'n_snps_mean_test'].astype(float)
        mean_inner_all=df_method_or_all.groupby(['prs_name','imp'])["mean"].mean().rename("mean_inner_all")
        se_inner_all=df_method_or_all.groupby(['prs_name','imp'])["mean"].std().rename("se_inner_all")
        print(df_method_or_all.loc[:,"n_snps_mean"].dtype)
        n_snps_mean_inner_all=df_method_or_all.groupby(['prs_name','imp'])["n_snps_mean"].mean().rename("n_snps_mean_inner_all")
        n_snps_median_inner_all=df_method_or_all.groupby(['prs_name','imp'])["n_snps_mean"].median().rename("n_snps_median_inner_all")
        n_snps_se_inner_all=df_method_or_all.groupby(['prs_name','imp'])["n_snps_mean"].std().rename("n_snps_se_inner_all")
        mean_outer_all=df_method_or_all.groupby(['prs_name','imp'])["mean_test"].mean().rename("mean_outer_all")
        se_outer_all=(df_method_or_all.groupby(['prs_name','imp'])["mean_test"].std()/np.sqrt(rep_end-rep_start)).rename("se_outer_all")
        n_snps_mean_outer_all=df_method_or_all.groupby(['prs_name','imp'])["n_snps_mean_test"].mean().rename("n_snps_mean_outer_all")
        n_snps_median_outer_all=df_method_or_all.groupby(['prs_name','imp'])["n_snps_mean_test"].median().rename("n_snps_median_outer_all")
        n_snps_se_outer_all=(df_method_or_all.groupby(['prs_name','imp'])["n_snps_mean_test"].std()/np.sqrt(rep_end-rep_start)).rename("n_snps_se_outer_all")
        df_cur_or_all=pd.concat([mean_inner_all, se_inner_all, n_snps_mean_inner_all, n_snps_se_inner_all, n_snps_median_inner_all, mean_outer_all, se_outer_all, n_snps_mean_outer_all, n_snps_se_outer_all, n_snps_median_outer_all], axis=1)
        df_cur_or_all.loc[:,'method']=method
        df_or_all=pd.concat([df_or_all, df_cur_or_all])

        df_method_or_99.loc[:,'mean']=df_method_or_99.loc[:,'mean'].astype(float)
        df_method_or_99.loc[:,'mean_test']=df_method_or_99.loc[:,'mean_test'].astype(float)

        mean_inner_99=df_method_or_99.groupby(['prs_name','imp'])["mean"].mean().rename("mean_inner_99")
        se_inner_99=df_method_or_99.groupby(['prs_name','imp'])["mean"].std().rename("se_inner_99")
        mean_outer_99=df_method_or_99.groupby(['prs_name','imp'])["mean_test"].mean().rename("mean_outer_99")
        se_outer_99=(df_method_or_99.groupby(['prs_name','imp'])["mean_test"].std()/np.sqrt(rep_end-rep_start)).rename("se_outer_99")
        # print(rep_end-rep_start)
        df_cur_or_99=pd.concat([mean_inner_99, se_inner_99, mean_outer_99, se_outer_99], axis=1)
        df_cur_or_99.loc[:,'method']=method
        df_or_99=pd.concat([df_or_99, df_cur_or_99])

    # df_or_all.loc[:,'prs_name']=[a[0] for a in df_or_all.index]
    # df_or_all.loc[:,'imp']=[a[1] for a in df_or_all.index]
    # df_or_99.loc[:,'prs_name']=[a[0] for a in df_or_99.index]
    # df_or_99.loc[:,'imp']=[a[1] for a in df_or_99.index]

    df_out=pd.merge(df_or_all, df_or_99, on=['method', 'prs_name', 'imp'])
    df_out.to_csv(os.path.join(constants.OUTPUT_PATH, output_fname), sep='\t')

methods=["pt2", "pt3", "ls", "ld"] #"pt2","ls","ld"]
rep_start="105_1"
rep_end="105_6"
suffix="bcac_minus_pl_pl_ctrl"
choose_model(methods, rep_start, rep_end, suffix)






