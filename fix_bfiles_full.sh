base_folder=/specific/elkon/hagailevi/PRS/datasets/1000genomes/
target_folder=/specific/elkon/hagailevi/PRS/datasets/chrs_full/
for i in {1..22}
do
#/specific/elkon/hagailevi/vcf/plink --bfile ${base_folder}chr${i} --merge-list ${base_folder}empty.txt --make-bed --out ${base_folder}chr${i}_fixed
/specific/elkon/hagailevi/vcf/plink --bfile ${base_folder}chr${i}_fixed --exclude ${target_folder}ds-merge.missnp --make-bed --out ${base_folder}chr${i}_fixed_2
done 
