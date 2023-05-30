#!/bin/bash
set -e

source constants_.sh
source parse_args.sh "$@"
source parse_chrs.sh
eval $(parse_chrs $chrs)

if [[ -z ${imp} ]]; then echo "imp argument is missing!"; exit 1; fi
if [[ -z ${target} ]]; then echo "target argument is missing!"; exit 1; fi

if [[ -z ${threads} ]]; then threads=22; fi

if [[ -z ${chrs_range} ]]; then chrs_range=($(seq 1 22)); fi


target_path=${datasets_path}${target}"/${imp}/"
target_path_elkon="/specific/elkon/hagailevi/PRS/datasets/dec/"${target}"/${imp}/"

echo 'Merge impute2 chrs'
pids=()
mkdir -p ${target_path_elkon}/raw/impute2/chrs || echo ""

for a in "${chrs_range[@]}"; do 
    echo "start chr${a}" 
    ( ( ls -1v ${target_path}raw/impute2/parts/chr${a}.*.legend | xargs cat > ${target_path_elkon}/raw/impute2/chrs/chr${a}.impute2 ) && echo "done merging chr${a}" ); 
    echo "finished chr${a}"
done;


echo 'Convert to bed files'
mkdir -p ${target_path_elkon}/raw/impute2/bed || echo ""
for a in "${chrs_range[@]}"; do plink --gen ${target_path_elkon}/raw/impute2/chrs/chr${a}.impute2 --sample ${datasets_path}${target}/original/raw/phased/chr${a}.phased.sample --oxford-single-chr ${a} --make-bed --threads 50 --out ${target_path_elkon}/raw/impute2/bed/ds${a}; done

# echo 'merge bed files'
# rm ${target_path}/raw/impute2/bed/mergelist.txt || echo ""
# for i in "${chrs_range[@]}"; do
#     echo ${target_path}/raw/impute2/bed/ds$i >> ${target_path}/raw/impute2/bed/mergelist.txt
# done
# 
# if [[ -f ${target_path}raw/impute2/bed/ds.all-merge.missnp ]]; then
#     echo 'fix bed files'
#     for i in "${chrs_range[@]}"; do
#         plink --bfile ${target_path}/raw/impute2/bed/ds$i --exclude ${target_path}raw/impute2/bed/ds.all-merge.missnp --make-bed --out ${target_path}/raw/impute2/bed/ds${i}.fixed
#         mv ${target_path}/raw/impute2/bed/ds${i}.fixed.fam ${target_path}/raw/impute2/bed/ds${i}.fam
#         mv ${target_path}/raw/impute2/bed/ds${i}.fixed.bim ${target_path}/raw/impute2/bed/ds${i}.bim
#         mv ${target_path}/raw/impute2/bed/ds${i}.fixed.bed ${target_path}/raw/impute2/bed/ds${i}.bed
#     done
# fi    
# 
# echo "retry to merge (fixed) chrs files"
# plink --exclude /specific/netapp5/gaga/gaga-pd/prs_data/datasets/dec/dbg-scz19/impute2_ajkg14_t101//raw/impute2/bed/ds.all-merge.missnp --merge-list ${target_path}/raw/impute2/bed/mergelist.txt --make-bed --out ${target_path}/raw/impute2/bed/ds.all
