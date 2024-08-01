#!/bin/bash
set -e
source constants_.sh
source parse_args.sh "$@"
source init_args.sh

# Parse input
discovery_path=${GWASs_path}${discovery}'/'
target_path=${datasets_path}${target}"/${imp}/"
prs_path=${PRSs_path}${discovery}_${target}"/${imp}/"
if [[ -z ${imp} ]]; then imp="original"; fi
if [[ -z ${memory} ]]; then memory=500000; fi
if [[ -z ${threads} ]]; then threads=80; fi
if [[ -z ${hp}  ]]; then hp="0.1"; fi
if [[ -z ${stage}  ]]; then stage=1; fi
if [[ -z ${rsid_col}  ]]; then rsid_col=1; fi
if [[ -z ${ea_col}  ]]; then ea_col=4; fi
if [[ -z ${beta_col}  ]]; then beta_col=6; fi
if [[ -z ${is_qc}  ]]; then is_qc="true"; fi

if [[ $is_qc == "true" ]]; then
    target_suffix=".QC"
else
    target_suffix=""
fi

if [[ ! -z $pheno ]]; then
    pheno_suffix="_${pheno}"
fi

# Start pipeline



if [[ $stage -le 1 ]]; then
  mkdir -p ${prs_path} || true

  echo calculate PRS
  plink \
    --bfile ${target_path}ds${target_suffix} \
    --score ${discovery_path}"prs.tsv" ${rsid_col} ${ea_col} ${beta_col}  \
    --keep ${datasets_path}${target}/pop.panel \
    --memory ${memory} \
    --threads ${threads} \
    --out ${prs_path}prs.mono.pt${sub}

  ## --extract ${discovery_path}"313.valid.snp"
  ## --score ${discovery_path}"313_rsids.tsv" 3 5 7 header

fi

if [[ $stage -le 2 ]]; then
  if [[ -f "${datasets_path}${target}/pheno${sub}" ]]; then
    echo Finding the best-fit PRS
    Rscript calc_metrics_pt.R --discovery=${discovery} --target=${target} --imp=${imp} \
                                         --sub=${sub} --analysis_type="mono" --grid_ids=-1;
  fi
fi

