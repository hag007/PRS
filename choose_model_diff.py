import os

import pandas as pd

import constants
import name_mappings
import utils
import numpy as np
from sklearn import metrics
import scipy as sp

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def choose_model(methods, rep_start, rep_end, suffix, imp_ref="impute2_ajkg14_t101", target="dbg-scz19"):

    df_result_all_methods=pd.DataFrame()

    output_fname=f"prs.cv.auc_{'' if suffix=='' else suffix+'_'}{rep_start}_{rep_end}.tsv"

    base_rep=rep_start.split("_")[0]
    rep_start=int(rep_start.split("_")[1])
    rep_end=int(rep_end.split("_")[1])+1

    for method in methods:
        df_result_cur_method=pd.DataFrame()
        for cur_rep in range(rep_start, rep_end):
            fl_name_or_all = os.path.join(constants.OUTPUT_PATH, f'prs.cv.{method}_or_all_{suffix}_{base_rep}_{cur_rep}_{base_rep}_{cur_rep}.tsv')
            fl_name_or_99 = os.path.join(constants.OUTPUT_PATH, f'prs.cv.{method}_or_99_{suffix}_{base_rep}_{cur_rep}_{base_rep}_{cur_rep}.tsv')
            # print(fl_name_or_all)
            if os.path.exists(fl_name_or_all):
                df_all = pd.read_csv(fl_name_or_all, sep='\t')
                df_99 = pd.read_csv(fl_name_or_99, sep='\t')
                print("exists: ",fl_name_or_all)
                # print(df_all.shape)
                # print(df_99.shape)

                sets=df_all.groupby(['prs_name','imp']).count().index
                # print(i)
                for prs_name,imp in sets:
                    # print(method, cur_rep, prs_name,imp)
                    df_all_filtered=df_all[(df_all.loc[:,'prs_name']==prs_name) & (df_all.loc[:,'imp']==imp)]
                    df_99_filtered=df_99[(df_99.loc[:,'prs_name']==prs_name) & (df_99.loc[:,'imp']==imp)]

                    df_all_filtered=df_all_filtered.sort_values(by=["mean"], ascending=False)
                    df_all_filtered.index=df_all_filtered.apply(lambda a: f"{method}_{cur_rep}_{a['hyperparameter']}_{a['prs_name']}_{a['imp']}", axis=1)
                    df_all_filtered.loc[:,'order']=np.arange(1,df_all_filtered.shape[0]+1) * 0.99
                    df_99_filtered=df_99_filtered.sort_values(by=["mean"], ascending=False)
                    df_99_filtered.index=df_99_filtered.apply(lambda a: f"{method}_{cur_rep}_{a['hyperparameter']}_{a['prs_name']}_{a['imp']}", axis=1)
                    df_99_filtered.loc[:,'order']=np.arange(1,df_99_filtered.shape[0]+1)
                    idx=(df_all_filtered.loc[:,'order']+df_99_filtered.loc[:,'order']).idxmin()
                    optimal=df_all_filtered.loc[idx]
                    if optimal.loc["prs_name"].startswith("D2") or optimal.loc["prs_name"].startswith("UKB"):
                        pheno=name_mappings.d_phenos_public_to_ukb.get(optimal.loc["prs_name"].split("_")[1],optimal.loc["prs_name"].split("_")[1])
                        pop=optimal.loc["prs_name"].split("_")[-1]
                        imp_ref=f"impute2_1kg_{pop}"
                        df_pheno=pd.read_csv(os.path.join(constants.DATASETS_PATH,'_'.join(optimal.loc['prs_name'].split('_')[-2:]), f'pheno_{pheno}_'), index_col=0, delim_whitespace=True)
                    else:
                        pheno=""
                        pop=""
                        df_pheno=pd.read_csv(os.path.join(constants.DATASETS_PATH,target, f'pheno_{pheno}_'), index_col=0, delim_whitespace=True)
                    fname_prs=os.path.join(constants.PRSS_PATH,optimal.loc['prs_name'], imp, f'rep_105_{cur_rep}',f'prs.cv.{method}_{pheno}__5_test.{np.format_float_positional(optimal["hyperparameter"], trim="-") if isfloat(optimal["hyperparameter"]) else optimal["hyperparameter"]}.profile')
                    # print(isfloat(optimal["hyperparameter"]), str(optimal["hyperparameter"]))

                    df_ref_all_filtered=df_all[(df_all.loc[:,'prs_name']==prs_name) & (df_all.loc[:,'imp']==imp)]
                    df_ref_99_filtered=df_99[(df_99.loc[:,'prs_name']==prs_name) & (df_99.loc[:,'imp']==imp)]

                    df_ref_all_filtered=df_ref_all_filtered.sort_values(by=["mean"], ascending=False)
                    df_ref_all_filtered.index=df_ref_all_filtered.apply(lambda a: f"{method}_{cur_rep}_{a['hyperparameter']}_{a['prs_name']}_{a['imp']}", axis=1)
                    df_ref_all_filtered.loc[:,'order']=np.arange(1,df_ref_all_filtered.shape[0]+1) * 0.99
                    df_ref_99_filtered=df_ref_99_filtered.sort_values(by=["mean"], ascending=False)
                    df_ref_99_filtered.index=df_ref_99_filtered.apply(lambda a: f"{method}_{cur_rep}_{a['hyperparameter']}_{a['prs_name']}_{a['imp']}", axis=1)
                    df_ref_99_filtered.loc[:,'order']=np.arange(1,df_ref_99_filtered.shape[0]+1)
                    idx_ref=(df_ref_all_filtered.loc[:,'order']+df_ref_99_filtered.loc[:,'order']).idxmin()
                    optimal_ref=df_ref_all_filtered.loc[idx_ref]
                    fname_ref_prs=os.path.join(constants.PRSS_PATH,optimal_ref.loc['prs_name'], imp_ref, f'rep_105_{cur_rep}',f'prs.cv.{method}_{pheno}__5_test.{np.format_float_positional(optimal_ref["hyperparameter"], trim="-") if isfloat(optimal_ref["hyperparameter"]) else optimal_ref["hyperparameter"]}.profile')
                    if not os.path.exists(fname_prs) or not os.path.exists(fname_ref_prs):
                        print(fname_prs, "or", fname_ref_prs, "does not exist")
                        continue
                    df1=pd.read_csv(fname_prs, index_col=0, delim_whitespace=True)
                    df2=pd.read_csv(fname_ref_prs, index_col=0, delim_whitespace=True)
                    score_diff=(sp.stats.zscore(df1.loc[:,'SCORE'])-sp.stats.zscore(df2.loc[:,'SCORE']))

                    df_score_pheno=pd.concat((sp.stats.zscore(df2.loc[:,'SCORE']).rename('SCORE_ref'), sp.stats.zscore(df1.loc[:,'SCORE']).rename('SCORE_cur'), score_diff,df_pheno),axis=1).dropna()
                    df_score_pheno['label']=df_score_pheno.loc[:,'label']-1
                    roc=metrics.roc_auc_score(y_true=df_score_pheno.loc[:,'label'], y_score=(df_score_pheno.loc[:,'SCORE']-df_score_pheno.loc[:,'SCORE'].min())/(df_score_pheno.loc[:,'SCORE'].max()-df_score_pheno.loc[:,'SCORE'].min()+0.0000001))
                    roc_ref=metrics.roc_auc_score(y_true=df_score_pheno.loc[:,'label'], y_score=df_score_pheno.loc[:,'SCORE_ref'])
                    roc_cur_imp=metrics.roc_auc_score(y_true=df_score_pheno.loc[:,'label'], y_score=df_score_pheno.loc[:,'SCORE_cur'])
                    # print((df_score_pheno.loc[:,'SCORE_cur'] > df_score_pheno.loc[:,'SCORE_cur'].quantile(0.9)))
                    # print((df_score_pheno.loc[:,'SCORE_cur'] > df_score_pheno.loc[:,'SCORE_cur'].quantile(0.9)).sum())

                    SCORE_cur_90=df_score_pheno.loc[df_score_pheno.loc[:,'SCORE_cur'] < df_score_pheno.loc[:,'SCORE_cur'].quantile(0.95),'label']
                    SCORE_ref_90=df_score_pheno.loc[df_score_pheno.loc[:,'SCORE_ref'] < df_score_pheno.loc[:,'SCORE_ref'].quantile(0.95),'label']
                    or_90_SCORE_ref_cur=SCORE_ref_90.sum()-SCORE_cur_90.sum()# (SCORE_ref_90.sum()/len(SCORE_ref_90))/(SCORE_cur_90.sum()/len(SCORE_cur_90))
                    # print(SCORE_cur_90.sum(), len(SCORE_cur_90), SCORE_ref_90.sum(), len(SCORE_ref_90))
                    # binary=((df_score_pheno.loc[:,'SCORE_cur'] < df_score_pheno.loc[:,'SCORE_cur'].quantile(0.9))*(df_score_pheno.loc[:,'label']-1.5)*2 * df_score_pheno.loc[:,'SCORE']/df_score_pheno.loc[:,'SCORE'].abs()).sum()
                    df_sorted_tmp=df_score_pheno.sort_values(by='SCORE_cur')
                    # print(df_sorted_tmp[df_sorted_tmp.loc[:,'label']==2])
                    # print(np.correlate(df_score_pheno.loc[:,'SCORE_cur'],df_score_pheno.loc[:,'SCORE']))
                    # print(((df_score_pheno.loc[:,'SCORE_cur'] < df_score_pheno.loc[:,'SCORE_cur'].quantile(0.1))*(df_score_pheno.loc[:,'label']-1.5)*2 * df_score_pheno.loc[:,'SCORE']/df_score_pheno.loc[:,'SCORE'].abs()))
                    # print(((df_score_pheno.loc[:,'SCORE_cur'] < df_score_pheno.loc[:,'SCORE_cur'].quantile(0.1))*(df_score_pheno.loc[:,'label']-1.5)*2 * df_score_pheno.loc[:,'SCORE']/df_score_pheno.loc[:,'SCORE'].abs()).sum())
                    # print(df_score_pheno.loc[:,'SCORE_cur'].quantile(0.5))
                    # print("binary: ",binary)
                    # print(prs_name,imp, roc)
                    # print(optimal)
                    # z=(roc_ref-roc_cur_imp)/np.sqrt(2) # -np.corrcoef(df_score_pheno.loc[:,'SCORE_ref'], df_score_pheno.loc[:,'SCORE_cur'])[0][1])
                    # auc_pval=sp.stats.norm.sf(abs(z))
                    # print(z, auc_pval)
                    df_result_cur_method=df_result_cur_method.append({'method':method, 'prs_name':optimal.loc['prs_name'], 'imp':optimal.loc['imp'], 'hyperparameter':optimal.loc['hyperparameter'], 'auc_delta': roc,  'auc_diff': roc_cur_imp-roc_ref, 'binary':or_90_SCORE_ref_cur}, ignore_index='True') # , 'auc_pval': auc_pval

        df_result_cur_method_delta_mean=df_result_cur_method.groupby(['prs_name','imp'])["auc_delta"].mean().to_frame()
        df_result_cur_method_delta_sem=(df_result_cur_method.groupby(['prs_name','imp'])["auc_delta"].std()/np.sqrt(rep_end-rep_start)).rename("delta_sem")
        df_result_cur_method_diff_mean=df_result_cur_method.groupby(['prs_name','imp'])["auc_diff"].mean().to_frame()
        df_result_cur_method_diff_sem=(df_result_cur_method.groupby(['prs_name','imp'])["auc_diff"].std()/np.sqrt(rep_end-rep_start)).rename("diff_sem")
        df_result_cur_method_binary_mean=df_result_cur_method.groupby(['prs_name','imp'])["binary"].mean().to_frame()
        df_result_cur_method_binary_sem=(df_result_cur_method.groupby(['prs_name','imp'])["binary"].std()/np.sqrt(rep_end-rep_start)).rename("binary_sem")

        df_result_cur_method=pd.concat((df_result_cur_method_delta_mean,df_result_cur_method_delta_sem, df_result_cur_method_diff_mean,df_result_cur_method_diff_sem, df_result_cur_method_binary_mean,df_result_cur_method_binary_sem),axis=1)
        df_result_cur_method.loc[:,'method']=method
        df_result_all_methods=pd.concat((df_result_all_methods, df_result_cur_method))

        # df_method_or_all.loc[:,'mean']=df_method_or_all.loc[:,'mean'].astype(float)
        # df_method_or_all.loc[:,'mean_test']=df_method_or_all.loc[:,'mean_test'].astype(float)
        # mean_inner_all=df_method_or_all.groupby(['prs_name','imp'])["mean"].mean().rename("mean_inner_all")
        # se_inner_all=df_method_or_all.groupby(['prs_name','imp'])["mean"].std().rename("se_inner_all")
        # mean_outer_all=df_method_or_all.groupby(['prs_name','imp'])["mean_test"].mean().rename("mean_outer_all")
        # se_outer_all=(df_method_or_all.groupby(['prs_name','imp'])["mean_test"].std()/np.sqrt(rep_end-rep_start)).rename("se_outer_all")
        # df_cur_or_all=pd.concat([mean_inner_all, se_inner_all, mean_outer_all, se_outer_all], axis=1)
        # df_cur_or_all.loc[:,'method']=method
        # df_or_all=pd.concat([df_or_all, df_cur_or_all])
        #
        # df_method_or_99.loc[:,'mean']=df_method_or_99.loc[:,'mean'].astype(float)
        # df_method_or_99.loc[:,'mean_test']=df_method_or_99.loc[:,'mean_test'].astype(float)
        #
        # mean_inner_99=df_method_or_99.groupby(['prs_name','imp'])["mean"].mean().rename("mean_inner_99")
        # se_inner_99=df_method_or_99.groupby(['prs_name','imp'])["mean"].std().rename("se_inner_99")
        # mean_outer_99=df_method_or_99.groupby(['prs_name','imp'])["mean_test"].mean().rename("mean_outer_99")
        # se_outer_99=(df_method_or_99.groupby(['prs_name','imp'])["mean_test"].std()/np.sqrt(rep_end-rep_start)).rename("se_outer_99")
        # print(rep_end-rep_start)
        # df_cur_or_99=pd.concat([mean_inner_99, se_inner_99, mean_outer_99, se_outer_99], axis=1)
        # df_cur_or_99.loc[:,'method']=method
        # df_or_99=pd.concat([df_or_99, df_cur_or_99])

    # df_or_all.loc[:,'prs_name']=[a[0] for a in df_or_all.index]
    # df_or_all.loc[:,'imp']=[a[1] for a in df_or_all.index]
    # df_or_99.loc[:,'prs_name']=[a[0] for a in df_or_99.index]
    # df_or_99.loc[:,'imp']=[a[1] for a in df_or_99.index]
    print(df_result_all_methods)
    df_result_all_methods.to_csv(os.path.join(constants.OUTPUT_PATH, output_fname), sep='\t')

methods=["pt","pt2" ,"ls"] # , "ld"]
rep_start="105_1"
rep_end="105_6"
suffix="scz_gain"
choose_model(methods, rep_start, rep_end, suffix)






