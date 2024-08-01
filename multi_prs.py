#!/usr/bin/env python
# coding: utf-8

import os
import sys
import getopt

from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, average_precision_score
from sklearn.model_selection import train_test_split
from scipy.stats import zscore
import pandas as pd
import numpy as np
# --rep_type=$rep_type

from multiprocessing import Pool

def parse_param():
    long_opts_list = ['prs_paths_lst=', 'best_hps=', 'label=', 'pheno_file_path=', 'method=', 'output_path=', 'output_prefix=', 'input_prefix=', 'include_all=', 'gwas_lst=' , 'reg_type=']

    param_dict = {'prs_paths_lst': None,'best_hps': None,'label': None,'pheno_file_path': None,'method': None,'output_path': None,'input_prefix':None, 'output_prefix':None, 'include_all':False, 'gwas_lst':None, 'reg_type':None}

    if len(sys.argv) > 1:
        try:
            opts, args = getopt.getopt(sys.argv[1:],"h", long_opts_list)   
        except:
            print('* Option not recognized.')
            sys.exit(2)
        
        for opt, arg in opts:
            if opt == "--prs_paths_lst": param_dict['prs_paths_lst'] = arg.split(',')
            elif opt == "--best_hps": param_dict['best_hps'] = arg.split(',')
            elif opt == "--label": param_dict['label'] = arg
            elif opt == "--pheno_file_path": param_dict['pheno_file_path'] = arg
            elif opt == "--method": param_dict['method'] = arg
            elif opt == "--output_path": param_dict['output_path'] = arg
            elif opt == "--input_prefix": param_dict['input_prefix'] = arg
            elif opt == "--output_prefix": param_dict['output_prefix'] = arg
            elif opt == "--include_all": param_dict['include_all'] = arg
            elif opt == "--gwas_lst": param_dict['gwas_lst'] = arg.split(',')
            elif opt == "--reg_type": param_dict['reg_type'] = arg
            # elif opt == "--": param_dict[''] = arg
    else:
       sys.exit(0)
    
    param_dict['best_hps'] = [combo.split('+') for combo in param_dict['best_hps']]

    if (param_dict['include_all'] != 'true') and any([len(param_dict['prs_paths_lst']) != len(a) for a in param_dict['best_hps']]):
        print("Error: number of hps != number of gwass")
        # print([a for a in param_dict['best_hps'] if len(a)!=2])
        # print(f"*********len of prs_paths is : {len(param_dict['prs_paths_lst'])}******")
        sys.exit(0)
    if (param_dict['include_all'] == 'true') and (len(param_dict['prs_paths_lst']) != len(param_dict['best_hps'])*len(param_dict['best_hps'][0])):
        print("Error: number of hps != number of gwass")
    if param_dict['label'] == None:
        param_dict['label'] = 'label'
    if any(value is None for value in param_dict.values()):
        print("Error: There is at least one value that is None in the dictionary.")
        sys.exit(0)

    

    return param_dict


class profile_item:
    def __init__(self, hp, gwas, index, train_profile, test_profile):
        self.hp=hp
        self.gwas=gwas
        self.index=index
        self.train_profile=train_profile
        self.test_profile=test_profile
    
    def get_train_profile_df(self):
        return self.train_profile
    
    def get_test_profile_df(self):
        return self.test_profile
    
    def get_hp(self):
        return self.hp
    
    def get_index(self):
        return self.index
    
    def get_gwas(self):
        return self.gwas
    
# load all profiles into dict
def prepare(prs_path_lst, best_hps_lst, input_prefix, gwas_lst, output_prefix):
    
    print("reading data into dataframes: ")
    check_no_dups=set()
    profiles_lst=[]
    for i in range(len(best_hps_lst)):
        input_profile_path=f'{prs_path_lst[i]}{input_prefix}.{best_hps_lst[i]}.profile' # train
        print(input_profile_path)
        output_profile_path=f'{prs_path_lst[i]}{output_prefix}.{best_hps_lst[i]}.profile' # test
        # make sure train and test profiles exist
        if not os.path.exists(input_profile_path):
            print("there is no profile for the hp "+str(best_hps_lst[i])+" under the path: "+input_profile_path)
            print("multi profile for combo "+'+'.join(best_hps_lst)+" will not be created.")
            return 
        if not os.path.exists(output_profile_path):
            print("there is no profile for the hp "+str(best_hps_lst[i])+" under the path: "+output_profile_path)
            print("multi profile for combo "+'+'.join(best_hps_lst)+" will not be created.")
            return 
        if input_profile_path not in check_no_dups:
            input_profile_df=pd.read_csv(input_profile_path, delimiter=r'\s+', header=0)
            output_profile_df=pd.read_csv(output_profile_path, delimiter=r'\s+', header=0)
            if (input_profile_df['SCORE'] == 0).all() or (output_profile_df['SCORE'] == 0).all():
                print(f'values too low for hp {best_hps_lst}, interpretated as NAN --> exit. These hps will not be used in the output')
                return
            check_no_dups.add(input_profile_path)
            item=profile_item(best_hps_lst[i], gwas_lst[i], i, input_profile_df, output_profile_df)
            profiles_lst.append(item)

    return profiles_lst


# prepare dataframes to create the model
#input: a list of all profiles to be used to create the regression, and a list of the hps that was used to create each profile.
def read_and_merge_df(pheno_file_path, label, profiles_lst):

    print(f'READ {pheno_file_path}')
    pheno_df=pd.read_csv(pheno_file_path, delimiter='\t', header=0)
    print("adjusting pheno from 1,2 to 0,1")
    pheno_df[label]=pheno_df[label]-1
    phenotype=pheno_df

    included_features=[]

    print("normalize the data and merge the data frames")
    for i in range(len(profiles_lst)):
        profile_df=profiles_lst[i].get_train_profile_df()
        profile_df['SCORE']=zscore(profile_df['SCORE'])
        new_header=f'SCORE_prs{profiles_lst[i].get_hp()}_{profiles_lst[i].get_gwas()}'
        profile_df=profile_df.rename(columns={'SCORE': new_header})
        phenotype=pd.merge(phenotype,profile_df[["FID", "IID", new_header]], on=["FID","IID"])
    
        included_features.append(new_header)
    
    print("phenotype dataframe was created successfully.")
    return phenotype, included_features



# calc pseudo r2
def efron_rsquare(y, y_pred):
    n = float(len(y))
    t1 = np.sum(np.power(y - y_pred, 2.0))
    t2 = np.sum(np.power((y - (np.sum(y) / n)), 2.0))
    return 1.0 - (t1 / t2)


### create the regression model
def fit_model(dataframe, included_features, label, best_hps_lst, best_hps_index, reg_type):
    dataframe=dataframe[included_features+["FID", "IID", label]]
        
    X=dataframe[included_features]
    y=dataframe[label]
    
    try:
        if reg_type=='linear':
            clf = LinearRegression().fit(X, y)
            alphas=clf.coef_
        if reg_type=='logistic':
            clf = LogisticRegression(random_state=0).fit(X, y)
            alphas=clf.coef_[0]
        score=clf.score(X, y)
    except ValueError:
        print(f'values too low for hp {best_hps_lst}, interpretated as NAN --> exit. These hps will not be used in the output')
        return
        # alphas=[0 for i in range(len(best_hps_lst))]
        # score=0

    
    # extract all needed data into a dataframe
    df=pd.DataFrame()
    df['hp']=[best_hps_index]
    print("................................")
    for i in range(len(included_features)): 
        print(f"alpha {i}: {alphas[i]}  (the coefficient of {included_features[i]})")
        df[f'alpha_{included_features[i]}']=[alphas[i]]


    # for the ranking file:
    rank_df=pd.DataFrame()
    rank_df['hp']=[best_hps_index]
    rank_df['score']=[score]

    return df, rank_df, clf



def rank_score_file(df_hps_all):
    df_hps_all['rank']=(df_hps_all['score']).rank(method='max')
    df_hps_all['rank']=len(df_hps_all['rank'])-df_hps_all['rank']+1
    return



# this function recieves the profiles and the clf_model in order to create the multi_profile ->the result of the regression.

def create_multi_profile(output_prefix,output_path, best_hps_index, clf_weights, profiles_lst, reg_type, included_features):
    all_mono_scores_df=pd.DataFrame()

    # in the future use merge for safety    
    dfs=[]
    for i in range(len(profiles_lst)):
        profile_df=profiles_lst[i].get_test_profile_df() #clf test profile
        profile_df.fillna(0, inplace=True)
        profile_df['SCORE']=zscore(profile_df['SCORE'])
        new_header=f'SCORE_prs{profiles_lst[i].get_hp()}_{profiles_lst[i].get_gwas()}'
        profile_df=profile_df.rename(columns={'SCORE': new_header})
        dfs.append(profile_df[['IID','FID',new_header]])
        # all_mono_scores_df[f'SCORE_prs{prs_index}_{profiles_lst[i].get_gwas()}']=profile_df['SCORE']
    
    all_mono_scores_df = dfs[0]
    for df in dfs[1:]:
        all_mono_scores_df = pd.merge(all_mono_scores_df, df, on=["FID","IID"])

    profile_multi=pd.DataFrame()
    profile_multi['IID']=all_mono_scores_df['IID']
    profile_multi['FID']=all_mono_scores_df['FID']
    if reg_type=='logistic':
        profile_multi['SCORE']=clf_weights.predict_proba(all_mono_scores_df[included_features])[:, 1]
    else: # linear reg
        profile_multi['SCORE']=clf_weights.predict(all_mono_scores_df[included_features])
    
    # best_hps_str='+'.join(best_hps_lst)
    profile_multi.fillna(0.0, inplace=True)
    out_file=f'{output_path}{output_prefix}.multi_{reg_type}.{best_hps_index}.profile'
    profile_multi.to_csv(out_file, sep='\t', index=False, encoding='utf-8')
    print(f"multi profile data has been written into: {out_file}")


## calling the functions!
def pipeline(params):

    print(f"pipeline with params: {params}")

    hp_combination, prs_paths_lst, pheno_file_path, label, input_prefix, output_prefix, output_path, gwas_lst, best_hps_index, reg_type = params

    profiles_lst= prepare(prs_paths_lst, hp_combination, input_prefix, gwas_lst, output_prefix)
    if profiles_lst is None:
        return
    dataframe, included_features = read_and_merge_df(pheno_file_path, label, profiles_lst)
        
    df_alpha, df_rank, clf_weights=fit_model(dataframe, included_features, label, hp_combination, best_hps_index, reg_type)
    create_multi_profile(output_prefix, output_path, best_hps_index, clf_weights, profiles_lst, reg_type, included_features)
    return pd.merge(df_alpha, df_rank, on='hp', how='outer')


if __name__=="__main__":
    ## preparing the data:
    param_dict=parse_param()
    print("recieved the following parameters:")

    for k, v in param_dict.items():
        if isinstance(v, list):
            v_str = repr(v)
            exec(f"{k} = {v_str}")
            print(f"{k} = {v_str}")
        else:
            exec(f"{k} = '{v}'")
            print (f"{k} = '{v}'")



    params=[]

    if include_all == 'true':
        # merge all hps into one list to excecute one regression
        # this list may include repetitions of hps per one discovery- to be handeled in pipeline
        best_hps_index=[('+').join(sub) for sub in best_hps]
        best_hps_index=[('_').join(best_hps_index)]
        best_hps=[[item for sublist in best_hps for item in sublist]]

    else:
        best_hps_index=[('+').join(sub) for sub in best_hps]

    for i in range(len(best_hps)):
        hp_combination=best_hps[i]
        print(f'{[hp_combination, prs_paths_lst, pheno_file_path, label, input_prefix, output_prefix, output_path, gwas_lst, best_hps_index[i], reg_type]}')
        params.append([hp_combination, prs_paths_lst, pheno_file_path, label, input_prefix, output_prefix, output_path, gwas_lst, best_hps_index[i], reg_type])
    with Pool(50) as p:
        rows=p.map(pipeline, params) 

    df_alphas_all=pd.concat(rows, ignore_index=True)

    df_alphas_all.to_csv(f'{output_path}{output_prefix}.multi_{reg_type}_hps_all_summary.tsv', sep='\t', index=False)


        
