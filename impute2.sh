set -e 

source /specific/elkon/hagailevi/PRS/codebase/parse_args.sh $@
source /specific/elkon/hagailevi/PRS/codebase/parse_chrs.sh
eval $(parse_chrs $chrs)

for chr in ${chrs_range[@]}; do
namefile="${chr}.phased";
maxPos=$(tail -n 1 /specific/elkon/hagailevi/data-scratch/imputation/maps/1000G_ALL_impute2/1000GP_Phase3/genetic_map_chr${chr}_combined_b37.txt | awk '{print $1}')
nrChunk=$(expr ${maxPos} "/" 5000000)
nrChunk2=$(expr ${nrChunk} "+" 1)
start="0"
for chunk in $(seq 1 $nrChunk2); do

    endchr=$(expr $start "+" 5000000)
    startchr=$(expr $start "+" 1)
   
    impute2 \
        -m "/specific/elkon/hagailevi/data-scratch/imputation/maps/1000G_ALL_impute2/1000GP_Phase3/genetic_map_chr${chr}_combined_b37.txt" \
        -h "/specific/netapp5/gaga/gaga-pd/prs_data/raw/dec/gd_aj/Phase 2/Ref panel/${chr}.merged.snp_indel.hap.gz" \
        -l "/specific/netapp5/gaga/gaga-pd/prs_data/raw/dec/gd_aj/Phase 2/Ref panel/${chr}.merged.snp_indel.legend" \
        -g "/specific/netapp5/gaga/gaga-pd/prs_data/datasets/dec/dbg-scz/original/raw/chr.${chr}.gen" \
        -int ${startchr} ${endchr} \
        -Ne 20000 \
        -allow_large_regions \
        -o "/specific/netapp5/gaga/gaga-pd/prs_data/datasets/dec/dbg-scz/imputed2/chr${chr}.${chunk}.legend"

start=${endchr}
done
done
