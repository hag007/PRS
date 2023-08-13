import os

import pandas as pd

import constants
import utils
import itertools




def fetch_n_snps(discovery, method, pheno, cv_suffix, hp, path):
     if method=='ls':
         snp_file=os.path.join(path, 'lasso',f'prs.cv.{method}___{cv_suffix}.{hp}.weights')
         print(snp_file)
         weights = pd.read_csv(snp_file, header=None, sep='\t')
         print(weights.iloc[:, -1])
         weights = weights.loc[weights.iloc[:, -1] > 0]
         n_snps=len(weights)
         print(f'ls s_snps: {n_snps}')
     elif method=='ld':
         snp_file=os.path.join(path, 'ldpred',f'prs.cv.{method}___{cv_suffix}.{hp}.weights')
         weights=pd.read_csv(snp_file, header=None, sep='\t')
         weights=weights.loc[weights.iloc[:,-1]>0]
         n_snps=len(weights)
         print(f'ld s_snps: {n_snps}')
     elif method=='pt3':
         snp_pvalue_file=os.path.join(constants.GWASS_PATH, discovery, 'SNP.pvalue')
         df_snp_pvalue=pd.read_csv(snp_pvalue_file, sep=' ', index_col=0)
         snp_file=os.path.join(path, f'prs.cv.{method}__eur_ld.valid.snp')
         df_snp=pd.read_csv(snp_file, header=None)
         df_relevant_snps=df_snp_pvalue.reindex(df_snp.iloc[:,0])
         n_snps=len(df_relevant_snps.loc[df_relevant_snps.iloc[:,0]<=float(hp)])
     elif method=='pt2':
         snp_pvalue_file=os.path.join(constants.GWASS_PATH, discovery, 'SNP.pvalue')
         df_snp_pvalue=pd.read_csv(snp_pvalue_file, sep=' ', index_col=0)
         snp_file=os.path.join(path, f'prs.cv.{method}___{cv_suffix}.valid.snp')
         df_snp=pd.read_csv(snp_file, header=None)
         df_relevant_snps=df_snp_pvalue.reindex(df_snp.iloc[:,0])
         n_snps=len(df_relevant_snps.loc[df_relevant_snps.iloc[:,0]<=float(hp)])


     else:
         raise ValueError(f"Cannot count # of SNPs for method {method}")

     return n_snps
 


def aggregate_statistics_cv(discoveries, targets, imps, method, hyperparameters, cv_folds, rep, suffix):
    df_statistics_all=pd.DataFrame()
    df_statistics_test=pd.DataFrame()
    df_or_all=pd.DataFrame()
    df_or_test=pd.DataFrame()


    cv_ids=[f"{a}_{cv_folds}_validation" for a in range(1,cv_folds+1)]


    for i, discovery in enumerate(discoveries):
        for target in targets:
            prs_name= f'{discovery}_{target}'
            pheno=constants.gwas_to_pheno.get(discoveries[i],"")
            for imp in imps:
                path = os.path.join(constants.PRSS_PATH, prs_name, imp, f"rep_{rep}")
                for hp in hyperparameters:                  
                    fl_name=os.path.join(path,f"prs.cv.{method}_{pheno}__{cv_folds}_test.ctrl.statistics.{hp}.tsv")
                    if os.path.exists(fl_name):
                        if os.stat(fl_name).st_size == 0:
#                             print(f'File {fl_name} is empty. Removing..')
                            os.remove(fl_name)
                        else:
                            n_snps=fetch_n_snps(discovery, method, pheno, f'{cv_folds}_both' ,hp,path)
#                             print(f'read file {fl_name}')
                            df=pd.read_csv(fl_name, sep='\t')
                            df['imp']=imp
                            df['prs_name']=prs_name
                            df['n_snps']=n_snps
                            df_statistics_test=pd.concat([df_statistics_test, utils.fix_table(df).iloc[-1:]])
#                             print("statistics test")
#                             print(df_statistics_test)
 

                    for cv_i, cv_suffix in enumerate(cv_ids):
                        fl_name=os.path.join(path,f"prs.cv.{method}_{pheno}__{cv_suffix}.ctrl.statistics.{hp}.tsv")
                        if os.path.exists(fl_name):
                            if os.stat(fl_name).st_size == 0:
                                print(f'File {fl_name}  is empty. Removing..')
                                os.remove(fl_name)
                            else:
                                n_snps=fetch_n_snps(discovery, method, pheno, cv_suffix.replace('validation','train'), hp, path)
                                df=pd.read_csv(fl_name, sep='\t')
                                df['imp']=imp
                                df['prs_name']=prs_name
                                df['fold']=cv_i+1
                                df['n_snps']=n_snps
                                df_statistics_all=pd.concat([df_statistics_all, utils.fix_table(df).iloc[-1:]])
#                                 print("statistics train")
#                                 print(utils.fix_table(df))  
#                                 print(df_statistics_all)

                        else:
                            print('warning:', fl_name, 'was not found')


    for i, discovery in enumerate(discoveries):
        for target in targets:
            prs_name= f'{discovery}_{target}'
            pheno=constants.gwas_to_pheno.get(discoveries[i],"")
            for imp in imps:
                path = os.path.join(constants.PRSS_PATH, prs_name, imp, f"rep_{rep}")
                for hp in hyperparameters:
                    fl_name = os.path.join(path, f"prs.cv.{method}_{pheno}__{cv_folds}_test.ctrl.or.summary.{hp}.tsv")
                    if os.path.exists(fl_name):
                        if os.stat(fl_name).st_size == 0:
                            print(f'File {fl_name}  is empty. Removing..')
                            os.remove(fl_name)
                        else:
                            n_snps=fetch_n_snps(discovery, method, pheno, f'{cv_folds}_both', hp, path)
                            df = pd.read_csv(fl_name, sep='\t')
                            df['imp'] = imp
                            df['prs_name']=prs_name
                            df['n_snps']=n_snps
                            df_or_test = pd.concat([df_or_test, utils.fix_table(df)])
#                             print("or test")
#                             print(df_or_test)
                    else:
                            print('warning:', fl_name, 'was not found')

                    for cv_i, cv_suffix in enumerate(cv_ids):
                        fl_name = os.path.join(path, f"prs.cv.{method}_{pheno}__{cv_suffix}.ctrl.or.summary.{hp}.tsv")
#                         print(fl_name)
                        if os.path.exists(fl_name):
                            if os.stat(fl_name).st_size == 0:
                                print(f'File {fl_name}  is empty. Removing..')
                                os.remove(fl_name)
                            else:
                                n_snps=fetch_n_snps(discovery, method, pheno, cv_suffix.replace('validation','train'), hp, path)
                                df = pd.read_csv(fl_name, sep='\t')
                                df['imp'] = imp
                                df['prs_name']=prs_name
                                df['fold']=cv_i+1
                                df['n_snps']=n_snps
                                df_or_all = pd.concat([df_or_all, utils.fix_table(df)])
#                                 print("or train")
#                                 print(df_or_all)
                        else:
                            print('warning:', fl_name, 'was not found')



    df_statistics_all.to_csv(os.path.join(constants.OUTPUT_PATH, f"prs.cv.{method}.ctrl.statistics_summary_{suffix}.tsv"), sep='\t')
    df_or_all.to_csv(os.path.join(constants.OUTPUT_PATH, f"prs.cv.{method}.ctrl.or_summary_{suffix}.tsv"), sep='\t')
    df_statistics_test.to_csv(os.path.join(constants.OUTPUT_PATH, f"prs.cv.ctrl.{method}.test.statistics_summary_{suffix}.tsv"), sep='\t')
    df_or_test.to_csv(os.path.join(constants.OUTPUT_PATH, f"prs.cv.{method}.test.ctrl.or_summary_{suffix}.tsv"), sep='\t')

    print(os.path.join(constants.OUTPUT_PATH, f"prs.cv.{method}.or_summary_{suffix}.tsv"))
    print("df_or_all", df_or_all.shape)

    print(os.path.join(constants.OUTPUT_PATH, f"prs.cv.{method}.test.or_summary_{suffix}.tsv"))
    print("df_or_test", df_or_test.shape)


