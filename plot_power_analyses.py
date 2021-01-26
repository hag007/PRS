import os

import matplotlib
import pandas as pd
import argparse
import constants

matplotlib.use("Agg")
import matplotlib.pyplot as plt

def plot_or_all(ax, x_axis_ar, curve_dict, curve_name, curve_value, y_field, xlabel, ylabel):
    p=ax.plot(x_axis_ar, [cur[0].loc[y_field] for cur in curve_dict[curve_value]], linestyle='-', marker='o', label=f'{curve_name}={curve_value}')
    ax.errorbar(x_axis_ar, [cur[0].loc[y_field] for cur in curve_dict[curve_value]], yerr=[cur[1].loc['or_all'] for cur in curve_dict[curve_value]], color=p[0].get_color(), capsize=5, ls='None', elinewidth=0.5, label='_nolegend_', marker="_")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title("logistic OR per 1 SD")

def plot_or_by_percentile(ax, x_axis_ar, curve_dict, curve_name, curve_value, y_field, xlabel, ylabel, title):
    p=ax.plot(x_axis_ar, [cur[0].loc[y_field] for cur in curve_dict[curve_value]], label=f'{curve_name}={curve_value}',
                       linestyle='-', marker='o')
    ax.errorbar(x_axis_ar, [cur[0].loc[y_field] for cur in curve_dict[curve_value]],
                       yerr=[cur[1].loc[y_field] for cur in curve_dict[curve_value]], color=p[0].get_color(), capsize=5,
                       ls='None', elinewidth=0.5, label='_nolegend_', marker="_")
    ax.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())
    ax.yaxis.grid(True, which='both')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='args')
    parser.add_argument('-s', '--pheno_src_path', dest='pheno_src_path', help='', default=os.path.join(constants.DATASETS_PATH, "ukbb","pheno_bc_only_scn_w.tsv"))
    parser.add_argument('-d', '--pheno_dest_path', dest='pheno_dest_path', help="", default=os.path.join(constants.DATASETS_PATH, "ukbb","pheno"))
    parser.add_argument('-i', '--n_iterations', dest='n_iterations', default="100", help='')
    parser.add_argument('-n', '--n_samples', dest='n_samples', default="200, 300, 400, 500, 750, 1000, 1500, 2000, 2500, 3000, 4000, 5000", help='')
    parser.add_argument('-p', '--prevalences', dest='prevalences', default="0.05, 0.1, 0.25, 0.5", help='')
    parser.add_argument('-g', '--discovery', dest='discovery', default="D_bca_michailidou_2017", help='')   # UR,BEB,PJL,MSL,ASW,ACB,CEU
    parser.add_argument('-t', '--target', dest='target', default="ukbb", help='')   # UR,BEB,PJL,MSL,ASW,ACB,CEU
    parser.add_argument('-imp', '--imp', dest='imp', default="imputeX", help='')   # UR,BEB,PJL,MSL,ASW,ACB,CEU
    parser.add_argument('-p', '--scripts_path', dest='scripts_path', default=os.path.join(constants.PUBLIC_BASE_PATH,"codebase"), help='')   # UR,BEB,PJL,MSL,ASW,ACB,CEU

    args = parser.parse_args()
    pheno_src_path=args.pheno_src_path
    pheno_dest_path = args.pheno_dest_path
    n_iterations=int(args.n_iterations)
    ar_n_samples = [int(a) for a in args.n_samples.split(',')]
    ar_prevalences = [float(a) for a in args.prevalences.split(',')]
    discovery=args.discovery
    target = args.target
    imp = args.imp
    scripts_path = args.scripts_path


    gwass=args.gwass.split(',')
    imp=args.imp
    targets=args.targets.split(',')
    thresholds=args.thresholds.split(',')

    res_by_prevalences={}
    res_by_n_samples={}
    for prevalence in ar_prevalences:
         res_by_prevalences[prevalence]=[]

    for n_samples in ar_n_samples:
         res_by_n_samples[n_samples]=[]

    df=pd.read_csv(pheno_src_path, sep='\t', index_col=0)
    for n_samples in ar_n_samples:
        for prevalence in ar_prevalences:
            df_all_statistics=pd.read_csv(os.path.join(constants.OUTPUT_PATH, f'agg_statistics_{discovery}_{target}_{imp}_{n_iterations}_{n_samples}_{prevalence}.tsv'), sep='\t')
            stat_mn=df_all_statistics.mean().round(2)
            stat_std=df_all_statistics.std().round(2)
            res_by_n_samples[n_samples].append((stat_mn,stat_std))
            res_by_prevalences[prevalence].append((stat_mn,stat_std))

    # OR by prevalence
    fig,axs = plt.subplots(2,3,figsize=(30,20))
    for k in res_by_n_samples:

        # OR value
        plot_or_all(axs[0][0], ar_prevalences, res_by_n_samples, "cohort size", k, "or_all", "prevalence", "mean OR")
        plot_or_by_percentile(axs[0][1], ar_prevalences, res_by_n_samples, "cohort size", k, "or_95", "prevalence", "mean OR" ,"OR (95-99%)/(40-60%)")
        plot_or_by_percentile(axs[0][2], ar_prevalences, res_by_n_samples, "cohort size", k, "or_99", "prevalence", "mean OR", "OR (99-100%)/(40-60%)")

        # # OR power
        plot_or_all(axs[1][0], ar_prevalences, res_by_n_samples, "cohort size", k, "power", "prevalence", "mean power")
        plot_or_by_percentile(axs[1][1], ar_prevalences, res_by_n_samples, "cohort size",k ,"or_95_power", "prevalence", "mean power" ,"OR (95-99%)/(40-60%)")
        plot_or_by_percentile(axs[1][2], ar_prevalences, res_by_n_samples, "cohort size", k, "or_99_power", "prevalence", "mean power", "OR (99-100%)/(40-60%)")

    plt.legend(loc=(1.1,0.9))
    plt.savefig(os.path.join(constants.FIGURES_PATH, "res_by_prevalences.png"))

    # OR by cohort size
    fig, axs = plt.subplots(2, 3, figsize=(30, 20))
    for k in res_by_prevalences:

        # OR value
        plot_or_all(axs[0][0], ar_n_samples, res_by_prevalences, "prevalence", k, "or_all", "cohort size", "mean OR")
        plot_or_by_percentile(axs[0][1], ar_n_samples, res_by_prevalences, "prevalence", k, "or_95", "cohort size",
                              "mean power", "OR (95-99%)/(40-60%)")
        plot_or_by_percentile(axs[0][2], ar_n_samples, res_by_prevalences, "prevalence", k, "or_99", "cohort size",
                              "mean power", "OR (99-100%)/(40-60%)")

        # OR power
        plot_or_all(axs[1][0], ar_n_samples, res_by_prevalences, "prevalence", k, "power", "cohort size", "mean OR")
        plot_or_by_percentile(axs[1][1], ar_n_samples, res_by_prevalences, "prevalence", k, "or_95_power", "cohort size",
                              "mean power", "Power of OR (95-99%)/(40-60%)")
        plot_or_by_percentile(axs[1][2], ar_n_samples, res_by_prevalences, "prevalence", k, "or_99_power", "cohort size",
                              "mean power", "Power of OR (99-100%)/(40-60%)")

    plt.legend(loc=(1.1, 0.9))
    plt.savefig(os.path.join(constants.FIGURES_PATH, "res_by_n_samples.png"))






