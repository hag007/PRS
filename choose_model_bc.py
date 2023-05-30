import os

import pandas as pd

import constants
import utils
import numpy as np

def choose_model(methods, rep_start, rep_end):

    df_or_all=pd.DataFrame()
    df_or_99=pd.DataFrame()

    for method in methods:
        df_method_or_all=pd.DataFrame()
        df_method_or_99=pd.DataFrame()
        for rep in range(int(rep_start.split("_")[1]), int(rep_end.split("_")[1])+1):
            fl_name_or_all = os.path.join(constants.OUTPUT_PATH, f'prs.cv.{method}_or_all_bcac_aj_{rep_start.split("_")[0]}_{rep}_{rep_start.split("_")[0]}_{rep}.tsv')
            fl_name_or_99 = os.path.join(constants.OUTPUT_PATH, f'prs.cv.{method}_or_99_bcac_aj_{rep_start.split("_")[0]}_{rep}_{rep_start.split("_")[0]}_{rep}.tsv')
            print(fl_name_or_all)
            if os.path.exists(fl_name_or_all):
                df_all = pd.read_csv(fl_name_or_all, sep='\t')
                df_99 = pd.read_csv(fl_name_or_99, sep='\t')

                df_all=df_all.sort_values(by=["mean"], ascending=False)
                df_all.index=df_all.loc[:,'hyperparameter'].apply(lambda a: f"{method}_{rep}_{a}")
                df_all.loc[:,'order']=np.arange(1,df_all.shape[0]+1) * 0.99
                df_99=df_99.sort_values(by=["mean"], ascending=False)
                df_99.index=df_99.loc[:,'hyperparameter'].apply(lambda a: f"{method}_{rep}_{a}")
                df_99.loc[:,'order']=np.arange(1,df_99.shape[0]+1)
                idx=(df_all.loc[:,'order']+df_99.loc[:,'order']).idxmin()
                # df_all.loc[idx]
                # df_99.loc[idx]
                df_method_or_all = pd.concat((df_method_or_all,  df_all.loc[idx].to_frame().T),axis=0)
                # print(df_method_or_99)
                # print(df_99.loc[idx])
                df_method_or_99 = pd.concat((df_method_or_99,  df_99.loc[idx].to_frame().T), axis=0)
        # print(df_method_or_all)
        # print(df_method_or_99)
        # quit()
        # print(df_method_or_all)
        # print(df_method_or_99)
        print(df_method_or_99.loc[:,"mean"])
        df_or_all=df_or_all.append({"method": method,
                        "mean_inner_all": df_method_or_all.loc[:,"mean"].mean(),
                        "se_inner_all": df_method_or_all.loc[:,"mean"].std(),
                        "mean_outer_all": df_method_or_all.loc[:,"mean_test"].mean(),
                        "se_outer_all": df_method_or_all.loc[:,"mean_test"].std()/np.sqrt(df_method_or_all.shape[0])}, ignore_index=True)

        df_or_99=df_or_99.append({"method": method,
                        "mean_inner_99": df_method_or_99.loc[:,"mean"].mean(),
                        "se_inner_99": df_method_or_99.loc[:,"mean"].std(),
                        "mean_outer_99": df_method_or_99.loc[:,"mean_test"].mean(),
                        "se_outer_99": df_method_or_99.loc[:,"mean_test"].std()/np.sqrt(df_method_or_99.shape[0])}, ignore_index=True)


    df_out=pd.merge(df_or_all, df_or_99, on='method')
    df_out.to_csv(os.path.join(constants.OUTPUT_PATH, f"prs.cv.choose_params.tsv"), sep='\t')

methods= ["pt","pt2","ls", "ld"]
rep_start="105_1"
rep_end="105_6"
choose_model(methods, rep_start, rep_end)






