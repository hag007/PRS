import constants
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp

title_format="BCAC-{}, T={}"
combs=[("bcac_onco_eur-5pcs", "bcac_onco_aj", "impX_new", "prs.cross.pt3.0.1.profile", title_format.format("IL", "0.1")), ("bcac_onco_eur-5pcs", "bcac_onco_aj", "impX_new", "prs.cross.pt3.0.00000005.profile", title_format.format("IL", "5e-8")), ("bcac_onco_eur-minus-pl", "bcac_onco_aj", "impX_new", "prs.cross.pt3.0.1.profile", title_format.format("IL", "0.1")), ("bcac_onco_eur-minus-pl", "bcac_onco_pl", "impX_new", "prs.cross.pt3.0.1.profile", title_format.format("PL", "0.1"))] #  ("bcac_onco_eur-minus-pl", "bcac_onco_aj", "impX_new", "prs.cross.pt3.0.00000005.profile", title_format.format("IL", "5e-8")), ("bcac_onco_eur-minus-pl", "bcac_onco_pl", "impX_new", "prs.cross.pt3.0.00000005.profile", title_format.format("PL", "5e-8"))] # , ("bca_313", "impX_new", "prs.pt.profile")] # , ("bca_313", "impute2_1kg_eur-multi", "prs.pt.profile"), ("bca_313", "impute2_1kg_eur-multi", "prs.pt.profile"),]

print(len(combs))
fig,axs=plt.subplots(len(combs)//2, 2, figsize=((7, 7)))
for i, (discovery, target, imp, prs_fname, title) in enumerate(combs):
    ax=axs[i//2][i%2]
    # discovery="bca_313" # "bca_313" # "bca_313"# "bcac_onco_eur-minus-uk-5pcs" # "bcac_onco_eur-5pcs"
    # target="bcac_onco_uk"
    # imp="impX_new"
    path=os.path.join(f"cross_{target}","impX_new")
    # fname="prs.pt.profile" # "prs.pt.profile" # "prs.pt.profile" "prs.cross.pt.0.001.profile"

    df0=pd.read_csv(os.path.join(constants.DATASETS_PATH,target,"cov2"),sep='\t')
    ## df1=pd.read_csv(os.path.join(constants.PRSS_PATH,"bcac_onco_eur-minus-uk-5pcs_bcac_onco_uk","impX_new","cross_bcac_onco_uk","impX_new","prs.cross.pt.0.0000001.profile"),delim_whitespace=True)
    print(df0.shape)
    df1=pd.read_csv(os.path.join(constants.PRSS_PATH,f"{discovery}_{target}",imp,path,prs_fname),delim_whitespace=True)
    df1.loc[:,'SCORE']=sp.stats.zscore(df1.loc[:,'SCORE'])
    # df1=pd.read_csv(os.path.join(constants.PRSS_PATH,f"{discovery}_{target}",imp,f"cross_{target}",imp,path,fname),delim_whitespace=True)

    df2=pd.merge(df0.loc[:,['FID', 'age']], df1.loc[:,['FID','SCORE']],on='FID')
    df2=df2.rename(columns={'SCORE': 'PRS'})
    bins=[0, 45, 75, 120] # [0, 40, 50,60,70,80,120]
    df2.loc[:,'Age interval']= pd.cut(df2.loc[:,'age'], bins=bins, include_lowest=True) # [0,45,75,120] [0,30, 40, 50,60,70,80,120]
    df2.loc[:,'Age interval']=df2.loc[:,'Age interval'].apply(lambda a: f'0-{int(a.right)}' if a.left<=bins[0] else a)
    df2.loc[:,'Age interval']=df2.loc[:,'Age interval'].apply(lambda a: f'{int(a.left)}+' if type(a) != str and a.right>=bins[-1] else a)
    df2.loc[:,'Age interval']=df2.loc[:,'Age interval'].apply(lambda a: f'{int(a.left)}-{int(a.right)}' if type(a) != str else a)
    print(df2.shape)
    sns.pointplot(y='PRS', x='Age interval', color='gray',data=df2 , showmeans=True, ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation = 45)
    ax.set_title(title)
    ax.set_ylabel('Normalized risk score')

    print(pd.concat((df2.groupby('Age interval')['PRS'].mean(), df2.groupby('Age interval')['PRS'].count()),axis=1))
plt.tight_layout()
plt.savefig(os.path.join(constants.FIGURES_PATH, f'prs_by_age_{discovery}_{target}_{imp}_{prs_fname}.png'))


