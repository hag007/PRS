import argparse
import os

import numpy as np
import pandas as pd

import constants

if __name__=="__main__":
    constants.DATASETS_PATH=constants.DATASETS_PATH 
    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-d', '--dataset', dest='dataset', help='', default='bcac_onco_aj')
    parser.add_argument('-p', '--population', dest='population', help="", default='')
    parser.add_argument('-ph', '--phenotype', dest='phenotype', help="", default="")
    parser.add_argument('-f', '--folds', dest='folds', help="", default="5")
    parser.add_argument('-r', '--rep', dest='rep', help="", default="1")

    args = parser.parse_args()
    dataset=args.dataset
    population = args.population
    folds = int(args.folds)
    phenotype=args.phenotype
    smpl=args.rep
    if smpl:
        pheno_folder=f'sample_{smpl}'

    all_path = os.path.join(constants.DATASETS_PATH, dataset, f'pheno_{phenotype}_{population}')


    base_case=101
    base_control=58
    additional_case=17
    additional_control=5

    df_all=pd.read_csv(all_path, sep='\t') # , index_col=0)
    for n_sample in range(1,100): # while df_case.shape[0]>=base_case+additional_case and df_control.shape[0]>=base_control+additional_control:

        try:
            os.mkdir(os.path.join(constants.DATASETS_PATH, dataset, f'{pheno_folder}_{n_sample}'))
        except OSError:
            pass

        df_sample=df_all.sample(frac=1)
        sample_path = os.path.join(constants.DATASETS_PATH, dataset, f'{pheno_folder}_{n_sample}', f'pheno_{phenotype}_{population}_1_1_sample')

        df_base.to_csv(base_sample_path, sep='\t', index=None)
        df_sample.to_csv(full_sample_path, sep='\t', index=None)

        df_case=df_case.iloc[base_case+additional_case:]
        df_control=df_control.iloc[base_control+additional_control:]

        # n_sample+=1

    n_sample=9

    try:
        os.mkdir(os.path.join(constants.DATASETS_PATH, dataset, f'{pheno_folder}'))
    except OSError:
        pass
    train_sample_path = os.path.join(constants.DATASETS_PATH, dataset, f'{pheno_folder}', f'pheno_{phenotype}_{population}_train_sample')
    df_train=pd.concat((df_case,df_control))
    df_train.to_csv(train_sample_path, sep='\t', index=None)





#     test_cv.loc[:, "IID"] = test_cv.index
#     test_cv.loc[:, "label"] = test_cv.loc[test_cv.index,"label"]

    #
    # for outer_fold in np.arange(int(folds + 1)):
    #
    #     try:
    #         os.mkdir(os.path.join(constants.DATASETS_PATH, dataset, f'{pheno_folder}_{outer_fold + 1}'))
    #     except OSError:
    #         pass
    #
    #     test_cv= df_all.iloc[outer_fold * fold_size:(outer_fold + 1) * fold_size].copy()
    #     df_train=pd.concat([df_all.iloc[:outer_fold * fold_size], df_all.iloc[(outer_fold + 1) * fold_size:]])
    #
    #
    #     test_path = os.path.join(constants.DATASETS_PATH, dataset, f'{pheno_folder}_{outer_fold + 1}', f'pheno_{phenotype}_{population}_{int(folds)}_test')
    #     test_cv.to_csv(test_path, sep='\t', index=None)
    #
    #     both_path = os.path.join(constants.DATASETS_PATH, dataset, f'{pheno_folder}_{outer_fold + 1}', f'pheno_{phenotype}_{population}_{int(folds)}_both')
    #     df_train.to_csv(both_path, sep='\t', index=None)
    #
    #     for inner_fold in np.arange(int(folds)):
    #
    #         validation_cv= df_train.iloc[inner_fold * fold_size:(inner_fold + 1) * fold_size].copy()
    #         train_cv=pd.concat([df_train.iloc[:inner_fold * fold_size].copy(), df_train.iloc[(inner_fold + 1) * fold_size:].copy()])
    #
    # #         train_cv.loc[:, "IID"] = train_cv.index
    # #         train_cv.loc[:, "label"] = train_cv.loc[train_cv.index,"label"]
    # #         validation_cv.loc[:, "IID"] = validation_cv.index
    # #         validation_cv.loc[:, "label"] = validation_cv.loc[validation_cv.index, "label"]
    #
    #         train_path = os.path.join(constants.DATASETS_PATH, dataset, f'{pheno_folder}_{outer_fold + 1}', f'pheno_{phenotype}_{population}_{int(inner_fold + 1)}_{int(folds)}_train')
    #         validation_path = os.path.join(constants.DATASETS_PATH, dataset, f'{pheno_folder}_{outer_fold + 1}', f'pheno_{phenotype}_{population}_{int(inner_fold + 1)}_{int(folds)}_validation')
    #         train_cv.to_csv(train_path, sep='\t', index=None)
    #         validation_cv.to_csv(validation_path, sep='\t', index=None)
    #
    #
