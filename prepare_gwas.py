import pandas as pd
import os
import argparse
import constants
import multiprocess

def reformat_gwas(args):
    discovery=args[0]
    print(f'starting reformatting {discovery}')
    df=pd.read_csv(os.path.join(GWASS_PATH, discovery, 'gwas_raw.tsv'), delim_whitespace=True)
    headers=pd.read_csv(os.path.join(GWASS_PATH, 'GIANT_1', 'gwas.tsv'), sep='\t').columns

    print(list(df.columns))    
    frq_a_label=None
    frq_u_label=None
    for a in df.columns:
        if a.startswith('FRQ_A'):
            frq_a_label=a
            frq_a_n=int(a.split('_')[2])
    
        if a.startswith('FRQ_U'):
            frq_u_label=a
            frq_u_n=int(a.split('_')[2])
    
    if not frq_a_label is None:     
         df.loc[:,"MAF"]=(df.loc[:,frq_a_label]*frq_a_n + df.loc[:,frq_u_label]*frq_u_n)/(frq_a_n+frq_u_n)
         df.loc[:,"N"]=frq_a_n+frq_u_n 
    
#     for a in ['EAF']:
#          if a in df.columns:
#              df.loc[:,'MAF']=df.loc[:,a]

    for a in ['Beta', 'OR(A1)', 'effect_size', 'or', 'beta']: 
         if a in df.columns:       
              df.loc[:,'OR']=df.loc[:,a]
   
    for a in ['MarkerName', 'SNPID', 'rs_id', 'snpid', 'variant_id']:
         if a in df.columns:
              df.loc[:,'SNP']=df.loc[:,a]
    
    for a in ['Chr', 'Chromosome', 'chr', 'chromosome']:
         if a in df.columns:
              df.loc[:,'CHR']=df.loc[:,a]

    for a in ['Effect_allele', 'effect_allele', 'a1']:
        if a in df.columns:
              df.loc[:,'A1']=df.loc[:,a]

    for a in ['Non_Effect_allele', 'noneffect_allele', 'a2', 'other_allele']:
         if a in df.columns:
              df.loc[:,'A2']=df.loc[:,a]

    for a in ['sample_size']:
         if a in df.columns:
              df.loc[:, 'N']=df.loc[:,a]

    for a in ['P-val', 'Pval', 'Pvalue', 'pval', 'pvalue', 'p.value']:
         if a in df.columns:
             df.loc[:,'P']=df.loc[:,a]

    for a in ['POS', 'Position(hg19)', 'Position', 'pos', 'base_pair_location_grch37']:
         if a in df.columns:
             df.loc[:,'BP']=df.loc[:,a]

    for a in ['standared error', 'se', 'standard_error']:
        if a in df.columns:
             df.loc[:,'SE']=df.loc[:,a]


    if not 'INFO' in df.columns:
         df.loc[:,'INFO']=1.0

    if not 'MAF' in df.columns:
         print('start merging MAF')
   
         df_maf=pd.read_csv(os.path.join(DATASETS_PATH, '1000genomes', 'ds.frq.strat'), delim_whitespace=True)
         df_maf=df_maf[df_maf.loc[:,'CLST']==discovery_population]
         df=df.merge(df_maf.loc[:,['SNP','MAF']], how='left', on='SNP')
         df.loc[:,'MAF'][df.loc[:,'MAF'].isnull()]=0.05
         print('end merging MAF')    

    if not N is None and not 'N' in df.columns:
         df.loc[:,'N']=N 

 
    if not 'SE' in df.columns:
         df.loc[:,'SE']=0.005

    df.reindex(headers,axis=1).to_csv(os.path.join(GWASS_PATH, discovery, 'gwas.tsv'), index=False, sep='\t')  
    print(f'done reformatting {discovery}')        
    



if __name__=='__main__':

    BASE_PATH='/specific/elkon/hagailevi/PRS/'
    GWASS_PATH=os.path.join(BASE_PATH,'GWASs/')
    DATASETS_PATH=os.path.join(BASE_PATH, 'datasets/')
    PRSS_PATH=os.path.join(BASE_PATH, 'PRSs/')
    OUTPUT_PATH=os.path.join(BASE_PATH, 'output/')
    FIGURES_PATH=os.path.join(OUTPUT_PATH, 'figures/')

    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-g', '--gwass', dest='gwass', help='', default="LH_PGC-SCZ-EAS")
    parser.add_argument('-n', '--N', dest='N', help='', default=None)
    parser.add_argument('-dp', '--discovery_population', dest='discovery_population', help='', default='EUR')
    args = parser.parse_args()
    gwass=args.gwass.split(',')  
    N=args.N
    discovery_population=args.discovery_population
    params=[]
    for discovery in gwass:
        params.append([discovery])
        reformat_gwas(params[-1])
    # p=multiprocess.Pool(5)    
    # p.map(reformat_gwas, params)
   



