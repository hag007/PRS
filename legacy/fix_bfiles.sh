base_folder=/specific/elkon/hagailevi/PRS/datasets/1000genomes/
for i in {21..22}
do
/specific/elkon/hagailevi/vcf/plink --bfile ${base_folder}chr${i} --merge-list ${base_folder}empty.txt --make-bed --out ${base_folder}chr${i}_fixed
/specific/elkon/hagailevi/vcf/plink --bfile ${base_folder}chr${i} --exclude ${base_folder}chr${i}_fixed-merge.missnp --make-bed --out ${base_folder}chr${i}_fixed
done 
