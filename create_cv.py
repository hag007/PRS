import argparse
import os

import numpy as np
import pandas as pd

import constants

if __name__=="__main__":
    constants.DATASETS_PATH=constants.DATASETS_PATH 
    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-d', '--dataset', dest='dataset', help='', default='ukbb_afr')
    parser.add_argument('-p', '--population', dest='population', help="", default='')
    parser.add_argument('-ph', '--phenotype', dest='phenotype', help="", default="")
    parser.add_argument('-f', '--folds', dest='folds', help="", default="5")
    parser.add_argument('-r', '--rep', dest='rep', help="", default="106")

    args = parser.parse_args()
    dataset=args.dataset
    population = args.population
    folds = float(args.folds)
    phenotype=args.phenotype
    rep=args.rep
    if rep:
        pheno_folder=f'rep_{rep}'

    try:
       os.mkdir(os.path.join(constants.DATASETS_PATH, dataset, pheno_folder))
    except OSError:
        pass

    all_path = os.path.join(constants.DATASETS_PATH, dataset, f'pheno_{phenotype}_{population}')


    df_all=pd.read_csv(all_path, sep='\t') # , index_col=0)
    print(df_all.shape)
    # r=np.arange(len(df_all))
    # np.random.shuffle(r)
    # df_all=df_all.loc[r]
    df_all=df_all.sample(frac=1)
    fold_size = int(len(df_all.index) / (folds)) # +1
    # test_cv=df_all.iloc[:fold_size].copy()
    # df_all=df_all.iloc[fold_size:]

#     test_cv.loc[:, "IID"] = test_cv.index
#     test_cv.loc[:, "label"] = test_cv.loc[test_cv.index,"label"]
#     test_path = os.path.join(constants.DATASETS_PATH, dataset, pheno_folder, f'pheno_{phenotype}_{population}_{int(folds)}_test')
#     test_cv.to_csv(test_path, sep='\t', index=None)

    # both_path = os.path.join(constants.DATASETS_PATH, dataset, pheno_folder, f'pheno_{phenotype}_{population}_{int(folds)}_both')
    # df_all.to_csv(both_path, sep='\t', index=None)

    for cur_fold in np.arange(int(folds)):
       
        validation_cv=df_all.iloc[cur_fold*fold_size:(cur_fold+1)*fold_size].copy()
        train_cv=pd.concat([df_all.iloc[:cur_fold*fold_size].copy(),df_all.iloc[(cur_fold+1)*fold_size:].copy()])

#         train_cv.loc[:, "IID"] = train_cv.index
#         train_cv.loc[:, "label"] = train_cv.loc[train_cv.index,"label"]
#         validation_cv.loc[:, "IID"] = validation_cv.index
#         validation_cv.loc[:, "label"] = validation_cv.loc[validation_cv.index, "label"]

        train_path = os.path.join(constants.DATASETS_PATH, dataset, pheno_folder, f'pheno_{phenotype}_{population}_{int(cur_fold+1)}_{int(folds)}_train')
        validation_path = os.path.join(constants.DATASETS_PATH, dataset, pheno_folder, f'pheno_{phenotype}_{population}_{int(cur_fold+1)}_{int(folds)}_validation')
        train_cv.to_csv(train_path, sep='\t', index=None)
        validation_cv.to_csv(validation_path, sep='\t', index=None)

     
