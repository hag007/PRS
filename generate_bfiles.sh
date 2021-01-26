for i in {21..22}
do
/specific/elkon/hagailevi/vcf/plink --vcf /specific/netapp5/gaga/data-scratch/hagailevi/ALL.chr${i}.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf --make-bed --out chr${i}
done
