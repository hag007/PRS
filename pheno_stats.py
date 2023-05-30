import pandas as pd
import numpy as np
import os
import subprocess
import constants
import argparse
import simplejson
from multiprocessing.pool import Pool
import pickle
import matplotlib
import matplotlib.pyplot as plt

def count_pheno(args):
    pheno_id, cur_pop_pheno = args
    # print(f"about to count pheno_id {pheno_id} in size-{len(cur_pop_pheno)} list")
    counts= cur_pop_pheno.count(pheno_id)
    # print(f'{pheno_id}={counts}')
    return int(pheno_id), counts


def get_pop_mappings(df_pop, df_data=None):

    if df_data is None:
        df_data=df_pop

    super_populations_unique = np.unique(df_data.loc[:, 'super_pop'].dropna())
    populations_unique = np.unique(df_data.loc[:,'pop'].dropna())

    color_palette_dict = {}
    super_to_pop = {}
    pop_to_super = {}
    color_palettes = ['PiYG_0_0.4', 'PiYG_0.6_1', 'PuOr_0_0.4', 'PuOr_0.6_1', 'bwr_0_0.4', 'bwr_0.6_1', 'spring_0_0.4',
                      'spring_0.6_1', 'cool_0_0.4', 'cool_0.6_1', 'RdGy_0_0.4', 'RdGy_0.6_1', 'bone_0_0.4',
                      'bone_0.6_1', 'pink_0_0.4', 'pink_0.6_1', 'summer_0_0.4', 'summer_0.6_1', 'copper_0_0.4',
                      'copper_0.6_1', 'Blues_0_0.4', 'Blues_0.6_1', 'Greens_0_0.4', 'Greens_0.6_1', 'Oranges_0_0.4',
                      'Oranges_0.6_1', 'Greens_0_0.4', 'Greens_0.6_1', 'Greens_0_0.4', 'Greens_0.6_1']

    for i, sp in enumerate(super_populations_unique):
        color_palette_dict[sp] = color_palettes[i]
        super_to_pop[sp] = []

    for i, pop in enumerate(populations_unique):
        super_pop = df_pop[df_pop.loc[:, 'pop'] == pop].iloc[0].loc['super_pop']
        super_to_pop[super_pop].append(pop)
        pop_to_super[pop] = super_pop

    return super_to_pop, pop_to_super, color_palette_dict

def get_pop_color(pop, super_to_pop, pop_to_super, color_palette_dict):
    c = (color_palette_dict[pop_to_super[pop]].split('_')[0])
    s = float(color_palette_dict[pop_to_super[pop]].split('_')[1]) * 1
    e = float(color_palette_dict[pop_to_super[pop]].split('_')[2]) * 1

    color = matplotlib.cm.get_cmap(c)(
    s + (e - s) * super_to_pop[pop_to_super[pop]].index(pop) / float(len(super_to_pop[pop_to_super[pop]])))

    return color

# def get_pop_color(super_pop, super_to_pop, pop_to_super, color_palette_dict):
#
#     c = (color_palette_dict[super_pop].split('_')[0])
#     s = float(color_palette_dict[super_pop].split('_')[1]) * 1
#     e = float(color_palette_dict[super_pop].split('_')[2]) * 1
#
#     color = matplotlib.cm.get_cmap(c)(1)
#
#     return color

if __name__=="__main__":
    constants.DATASETS_PATH=constants.DATASETS_PATH
    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-s', '--raw_pheno_src_path', dest='raw_pheno_src_path', help='', default=os.path.join(constants.DATASETS_PATH, "ukbb","ukb_code6.csv")) # "ukb_code6.csv"
#    parser.add_argument('-d', '--pheno_dest_path', dest='pheno_dest_path', help="", default=os.path.join(constants.DATASETS_PATH, "ukbb","pheno_t2d"))
    parser.add_argument('-n', '--pheno_name_path', dest='pheno_name_path', help="", default=os.path.join(constants.DATASETS_PATH, "ukbb", "data_coding_6.tsv"))
    parser.add_argument('-p', '--pop_path', dest='pop_path', help="", default=os.path.join(constants.DATASETS_PATH, "ukbb", "pop.panel"))
    parser.add_argument('-c', '--category_prefix', dest='category_prefix', help="", default="20002") # 20001



    args = parser.parse_args()
    raw_pheno_src_path=args.raw_pheno_src_path
#    pheno_dest_path=args.pheno_dest_path
    pheno_name_path = args.pheno_name_path
    pop_path = args.pop_path
    category_prefix = args.category_prefix
    df_pop = pd.read_csv(pop_path, sep='\t', index_col=0)
    df_raw_pheno=pd.read_csv(raw_pheno_src_path, sep=',',index_col=0)
    df_pheno_name = pd.read_csv(pheno_name_path, sep='\t', index_col=0)
    df_cat = pd.concat([df_pop, df_raw_pheno], axis=1)
    excluded_super_pop = ['White', 'undefined', 'Prefer not to answer', 'Other ethnic group', 'Do not know', ]
    df_pheno_pop = df_cat.loc[~df_cat.loc[:, "super_pop"].isin(excluded_super_pop).values, :]

    super_to_pop, pop_to_super, color_palette_dict = get_pop_mappings(df_pop)

    pheno_headers = [a for a in df_raw_pheno.columns.values if a.startswith(category_prefix+'-')]
    df_pheno = df_pheno_pop.loc[:, pheno_headers]
    phenos = list(df_pheno.values.flatten()[~np.isnan(df_pheno.values.flatten())].astype(np.int32))
    limit= np.unique(phenos).shape[0]
    top=limit
    phenos_unique = np.unique(phenos)[:limit]

    # p = Pool(20)
    pheno_counts_list = []
    print(f"starts counting phenos in entire cohort for {phenos_unique.shape[0]} phenotypes")
    # results = p.map(count_pheno, [(a, phenos) for a in phenos_unique])
    # p.close()
    results=[]
    args = [(a, phenos) for a in phenos_unique]
    for arg in args:
        results.append(count_pheno(arg))

    print("done")
    print(list(df_pheno_name.index))
    for k, v in results:
        # print(f"cur id: {v}")
        pheno_counts_list.append((k, df_pheno_name.loc[k, 'name'], v))
    pheno_counts_list.sort(key=lambda a: -a[2])
    print(pheno_counts_list)
    pheno_counts_list_top_ids=[a[0] for a in pheno_counts_list[:top]]


    ind = np.arange(top)
    fig,ax=plt.subplots(1,1, figsize=(30,10))
    pop_to_count_dict={}
    for cur_super_pop in np.unique(df_pheno_pop.loc[:, 'super_pop'].dropna().values):
        print(f"cur_super_pop: {cur_super_pop}")
        if cur_super_pop in excluded_super_pop:
            continue
        for cur_pop in np.unique(df_pop[df_pop.loc[:, 'super_pop'] == cur_super_pop].dropna().loc[:, 'pop']):
            print(f"cur_pop: {cur_pop}")
            df_cur_pop=df_pheno_pop[df_pheno_pop.loc[:,'pop']==cur_pop].loc[:,pheno_headers]
            df_cur_pop_pheno = df_cur_pop.loc[:, pheno_headers]
            cur_pop_pheno = list(df_cur_pop_pheno.values.flatten()[~np.isnan(df_cur_pop_pheno.values.flatten())].astype(np.int32))
            # p=Pool(20)
            # results=p.map(count_pheno, [(a,cur_pop_pheno) for a in pheno_counts_list_top_ids])
            # p.close()
            args=[(a,cur_pop_pheno) for a in pheno_counts_list_top_ids]
            results=[]
            for arg in args:
                results.append(count_pheno(arg))

            pheno_counts_dict={}
            pheno_counts_list=[]
            print(df_pheno_name)
            for k,v in results:
                pheno_counts_dict[df_pheno_name.loc[k,'name']]=v
                pheno_counts_list.append((df_pheno_name.loc[k,'name'],v))
            pop_to_count_dict[f'{cur_super_pop}_{cur_pop}']=pheno_counts_list
            print(pheno_counts_list)

    positional_bar=np.zeros(top)
    df=pd.DataFrame(columns=["super_pop"]+[df_pheno_name.loc[a,'name'] for a in pheno_counts_list_top_ids])
    for k,v in pop_to_count_dict.items():
        cur_pop=k.split("_")[1]
        cur_bar=np.array([a[1] for a in v])
        ax.bar(ind, cur_bar, 0.35, bottom=positional_bar, color=get_pop_color(cur_pop, super_to_pop, pop_to_super, color_palette_dict), label=k)
        df.loc[cur_pop]=np.concatenate((np.array([pop_to_super[cur_pop]]), cur_bar))
        positional_bar=positional_bar+cur_bar
        print(k)
    # ax.set_yscale('log')

    df.to_csv(os.path.join(constants.OUTPUT_PATH, "pheno_dist_by_pop.tsv"), sep='\t')
    xaxis_labels=[df_pheno_name.loc[a,'name'] for a in pheno_counts_list_top_ids]
    ax.set_xticks(np.arange(len(xaxis_labels)))
    ax.set_xticklabels(tuple(xaxis_labels),rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(constants.FIGURES_PATH, "pheno_dist_by_pop.png"))


    # pickle.dump(pop_to_count_dict, open('pheno_counts_dict.pkl', 'wb+'))


