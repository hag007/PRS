set -e

source constants.sh
source parse_args.sh $@


if [[ -z imp  ]]; then
    imp="original"
fi

if [[ -z memory  ]]; then
    memory="600000"
fi

if [[ -z threads  ]]; then
    threads="80"
fi


function calc_prs {


    discovery_path=${GWASs_path}${discovery}'/'
    target_path=${datasets_path}${target}"/${imp}/"
    prs_path=${PRSs_path}${discovery}_${target}"/${imp}/"
    
    
    echo calculate PRS
    plink \
        --bfile ${target_path}ds.QC \
        --memory ${memory} \
        --threads ${threads} \
        --out ${prs_path}prs \
        --score ${discovery_path}"313_rsids.tsv" 3 5 7 header \
        --extract ${discovery_path}"313.valid.snp" 
#         --score ${discovery_path}gwas.QC.Transformed 1 4 11 header \
#         --extract ${prs_path}"prs.valid.snp" \
 
    if [[ -f "${datasets_path}${target}/pheno" ]]; then 
        echo Finding the best-fit PRS
        Rscript best_fit_prs_313.R ${discovery} ${target} ${imp} ;
    fi

}

gwass=(${1//,/ })
echo $gwass

for g in "${gwass[@]}"; do
    echo $g $2
    calc_prs $g $2 # & pids+=($!)
done

wait "${pids[@]}"

