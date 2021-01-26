
1000G_path='/specific/netapp5/gaga/data-scratch/hagailevi/1000G_ALL/'

for a in {1..22};do mv ${1000G_path}ALL.chr${a}.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf ${1000G_path}chr${a}.vcf;done

for a in {1..22};do mv ${1000G_path}ALL.chr${a}.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz.tbi ${1000G_path}chr${a}.vcf.gz.tbi; done

mv ${1000G_path}ALL.chrY.phase3_integrated_v2a.20130502.genotypes.vcf ${1000G_path}chrY.vcf
mv ${1000G_path}ALL.chrY.phase3_integrated_v2a.20130502.genotypes.vcf.gz.tbi ${1000G_path}chrY.vcf.gz.tbi 

mv ${1000G_path}ALL.chrX.phase3_shapeit2_mvncall_integrated_v1b.20130502.genotypes.vcf ${1000G_path}chrX.vcf 
mv ${1000G_path}ALL.chrX.phase3_shapeit2_mvncall_integrated_v1b.20130502.genotypes.vcf.gz.tbi ${1000G_path}chrX.vcf.gz.tbi

mv ${1000G_path}ALL.chrMT.phase3_callmom-v0_4.20130502.genotypes.vcf ${1000G_path}chrMT.vcf
mv ${1000G_path}ALL.chrMT.phase3_callmom-v0_4.20130502.genotypes.vcf.gz.tbi ${1000G_path}chrMT.vcf.gz.tbi  
