#!/bin/bash
set -e
source constants_.sh
source parse_args.sh "$@"

# Parse input
discovery_path=${GWASs_path}${discovery}'/'
target_path=${datasets_path}${target}"/${imp}/"
prs_path=${PRSs_path}${discovery}_${target}"/${imp}/"
if [[ -z ${imp} ]]; then imp="original"; fi
if [[ -z ${memory} ]]; then memory=500000; fi
if [[ -z ${threads} ]]; then threads=80; fi
if [[ -z ${hp}  ]]; then hp="0.1"; fi
if [[ -z ${stage}  ]]; then stage=1; fi
if [[ -z ${weight_column}  ]]; then weight_column=7; fi


# Start pipeline



if [[ $stage -le 1 ]]; then
  mkdir -p ${prs_path} || true

  echo calculate PRS
  plink \
    --bfile ${target_path}ds \
    --score ${discovery_path}"313_rsids.tsv" 3 5 ${weight_column}  \
    --keep ${datasets_path}${target}/pop.panel \
    --extract ${discovery_path}"313.valid.snp" \
    --memory ${memory} \
    --threads ${threads} \
    --out ${prs_path}prs.mono.pt

  ## --extract ${discovery_path}"313.valid.snp"
  ## --score ${discovery_path}"313_rsids.tsv" 3 5 7 header

fi

if [[ $stage -le 2 ]]; then
  if [[ -f "${datasets_path}${target}/pheno" ]]; then
    echo Finding the best-fit PRS
    Rscript calc_metrics_pt.R --discovery=${discovery} --target=${target} --imp=${imp} \
                                         --suffix="${suffix}" --analysis_type="mono" --grid_ids=-1;
  fi
fi

