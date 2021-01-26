set -e

source constants.sh
source parse_args.sh $@

function qc_gwas {

    prefix=$1'/'
    GWAS_path=${GWASs_path}${gwas}'/'
    
    echo filter low-quality SNPs
    cat ${GWAS_path}gwas.tsv |\
    awk 'NR==1 || ($6 > 0.01) && ($10 > 0.8) {print}' |\
    gzip  > ${GWAS_path}gwas.quality.gz
    
    echo filter ambiguous SNPS
    gunzip -c ${GWAS_path}gwas.quality.gz |\
    awk '!( ($4=="A" && $5=="T") || \
            ($4=="T" && $5=="A") || \
            ($4=="G" && $5=="C") || \
            ($4=="C" && $5=="G")) {print}' |\
        gzip > ${GWAS_path}gwas.noambig.gz
    
    echo get duplicated SNPs
    gunzip -c ${GWAS_path}gwas.noambig.gz |\
    awk '{ print $1}' |\
    sort |\
    uniq -d > duplicated.snp
    
    echo remove duplicated SNPs
    gunzip -c ${GWAS_path}gwas.noambig.gz  |\
    grep -vf duplicated.snp |\
    gzip - > ${GWAS_path}gwas.QC.gz

    gunzip -c ${GWAS_path}gwas.QC.gz > ${GWAS_path}gwas.QC.Transformed
#    echo log-transform effect size
#    Rscript ${codebase_path}update_effect_size.R ${1}

}


gwass=(${gwas//,/ })
echo $gwas

for g in "${gwas[@]}"; do
    echo $g
    qc_gwas $g & pids+=($!)
done

wait "${pids[@]}"

