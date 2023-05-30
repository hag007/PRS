

echo "start script..."
nrow=1000
impX_snps=$(head -n $nrow $PRS_DATASETS/bcac_onco_eur_random/impX/ds.vcf  | tail -n +30)
echo "fetch first VCF"
impX_new_snps=$(head -n $nrow $PRS_DATASETS/bcac_onco_eur_random/impX_new/ds.vcf  | tail -n +30)
echo "fetch second VCF"
c=0
nf=0
e=0
counter=0

snps=$(head -n $nrow $PRS_DATASETS/bcac_onco_eur_random/impX/ds.vcf  | cut -f 3 | cut -d ':' -f 1 | tail -n +30)

echo "snps: $snps"

while IFS= read -r cur_snp; do
  echo "cur snp: $cur_snp"
  cur_impX_new_snps=$(echo "$impX_new_snps" | grep $cur_snp | cut -f 4-20)
  cur_impX_snps=$(echo "$impX_snps" | grep $cur_snp | cut -f 4-20)
  if [[ $cur_impX_new_snps == "" ]]; then
    # echo "SNP $cur_snp was not found"
    nf=$(($nf+1))
  elif [[ $cur_impX_snps == $cur_impX_new_snps ]]; then
    c=$(($c+1))
  else
    e=$(($e+1))
  fi

  counter=$((counter+1))

done <<< "$snps"

echo "total number of SNPs: "
echo "nf: $nf"
echo "c: $c"
echo "e: $e"

