import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np
import constants
import os
import matplotlib
matplotlib.rcParams["xtick.labelsize"]=22
matplotlib.rcParams["ytick.labelsize"]=22
matplotlib.use('Agg')
import matplotlib.pyplot as plt

constants.OUTPUT_DIR="/specific/elkon/hagailevi/PRS/codebase/"
def get_proxies(src_fn='src_ids.txt',dest_fn='dest_ids.txt', ev_fn="", n_closest_samples=100):
    df0=pd.read_csv(ev_fn, sep='\t', index_col=0)
    df0.index=df0.index.astype(str)
    df0=df0.iloc[:,1:7]
    print(f'ev_fn: {df0.shape[0]}')
    src_ids=[a.strip() for a in open(src_fn).readlines()]
    dest_ids=[a.strip() for a in open(dest_fn).readlines()]
    print(f'n src ids {len(src_ids)}, n dest ids {len(dest_ids)}')
    src=df0.reindex(src_ids).dropna()
    dest=df0.reindex(dest_ids).dropna()
    print(dest)
    print(f'n src df {src.shape[0]}, n dest df {dest.shape[0]}')
    nbrs = NearestNeighbors(n_neighbors=50, algorithm='auto').fit(dest)
    distances, indices = nbrs.kneighbors(src)
    indices_flatten=indices.flatten()
    counts = np.bincount(indices_flatten)
    ii = np.nonzero(counts)[0]
    id_freq=sorted(zip(ii,counts[ii]), key=lambda a: a[1])
    top_id_freq=[a[0] for a in id_freq[-n_closest_samples:]]
    fig, ax = plt.subplots(figsize=(20,20))
    print(f"n src final: {src.shape[0]}")
    print(f"n dest close: {dest.iloc[top_id_freq].dropna().shape[0]}")
    print(f"n dest distant: {dest.drop(dest.index[top_id_freq]).shape[0]}")
    # ax.plot(*zip(*src.iloc[:,:2].values), marker='o', linestyle=' ', markersize=6, label='AJ',zorder=100)
    # ax.plot(*zip(*dest.iloc[top_id_freq,:2].dropna().values), marker='o', linestyle=' ', markersize=6, label='AJ proxies', zorder=101)
    # ax.plot(*zip(*dest.drop(dest.index[top_id_freq]).iloc[:,:2].values), marker='o', linestyle=' ', markersize=6, label='EUR', zorder=50)
    return src, dest.iloc[top_id_freq], dest.drop(dest.index[top_id_freq])


def save_pheno(s,d,fn):
    df0=pd.DataFrame(index=s.index)
    df1=pd.DataFrame(index=d.index)
    df0['IID']=df0.index
    df0['label']=0
    df1['IID']=df1.index
    df1['label']=1
    df_pheno=pd.concat([df0,df1],axis=0)
    df_pheno.to_csv(fn, sep='\t', index_label='FID')

def plot_pheno(s,d, dx, fn):
    fig, ax = plt.subplots(figsize=(17,17))
    print(f"n src final: {s.shape[0]}")
    print(f"n dest close: {d.shape[0]}")
    print(f"n dest distant: {dx.shape[0]}")
    ax.plot(*zip(*s.iloc[:,:2].values), marker='o', linestyle=' ', markersize=6, label='AJ',zorder=100, markerfacecolor='gray', mec='black', mew=0.1)
    ax.plot(*zip(*d.iloc[:,:2].dropna().values), marker='o', linestyle=' ', markersize=6, mew=1.0, mec='blue', label='AJ proxies', zorder=101, markerfacecolor="None")
    ax.plot(*zip(*dx.iloc[:,:2].values), marker='o', linestyle=' ', markersize=6, label='EUR', zorder=50, markerfacecolor='orange', mec='black', mew=0.1)
    ax.set_xlabel("PC1",fontsize=22)
    ax.set_ylabel("PC2",fontsize=22)
    plt.legend(fontsize=22,markerscale=4)
    plt.savefig(fn)


if __name__=="__main__":
    
#    base_output_fn=os.path.join(constants.OUTPUT_DIR, f'{os.path.splitext(os.path.basename(src_fn))[0]}_{os.path.splitext(os.path.basename(dest_fn))[0]}')
    s1,d1,dx1=get_proxies(src_fn='healthy_AJ.txt',dest_fn='B_bc.tsv', ev_fn="/specific/netapp5/gaga/gaga-pd/prs_data/datasets/dec/ukbb_ajkg14_ajkg18_dbg-scz19/impute2/ds.eigenvec", n_closest_samples=60)
    s2,d2,dx2=get_proxies(src_fn='healthy_AJ.txt',dest_fn='B_healthy.tsv', ev_fn="/specific/netapp5/gaga/gaga-pd/prs_data/datasets/dec/ukbb_ajkg14_ajkg18_dbg-scz19/impute2/ds.eigenvec", n_closest_samples=300)
    
    save_pheno(s1,d1,os.path.join(constants.OUTPUT_DIR,"AJ_healthy_B_bc.tsv"))
    save_pheno(d2,d1,os.path.join(constants.OUTPUT_DIR,"B_healthy_B_bc.tsv"))
    plot_pheno(s1,d1,dx1,os.path.join(constants.OUTPUT_DIR,"AJ_healthy_B_bc.png"))
    plot_pheno(s2,d2,dx2,os.path.join(constants.OUTPUT_DIR,"B_healthy_B_bc.png"))
