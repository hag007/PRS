#!/bin/bash
set -e
source constants_.sh
source parse_args.sh "$@"

# Parse input
if [[ -z $imp  ]]; then imp="original"; fi
if [[ -z $memory  ]]; then memory="600000"; fi
if [[ -z $threads  ]]; then threads="80"; fi
if [[ -z $pval_th  ]]; then pval_th="0.1"; fi
if [ ${pop} != "" ]; then
        pop=_${pop}
fi

discovery_path=${GWASs_path}${discovery}'/'
target_path=${datasets_path}${target}"/${imp}/"
prs_path=${PRSs_path}${discovery}_${target}"/${imp}/"

echo "Calculate best fit (if ${datasets_path}${target}/pheno${pop} exists)"
if [[ -f "${datasets_path}${target}/pheno${pop}" ]]; then
	echo Finding the best-fit PRS
	Rscript best_fit_prs.R ${discovery} ${target} ${imp} ${pval_th} ${pop}
	  # R CMD BATCH "--args ${discovery} ${target} ${imp}" best_fit_prs.R /dev/tty;
fi

