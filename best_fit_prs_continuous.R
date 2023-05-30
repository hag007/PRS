.libPaths(c('../R-env/prs-R',.libPaths()))
library(dplyr)
library(fmsb)
library(epitools)
library(performance)
library(pROC)
library(DescTools)
library(genpwr)
library(WebPower)
library(epiR)
source('constants.R')
args <- commandArgs(trailing = TRUE)
gwas_path<-paste0(GWASS_PATH, args[1],'/')
ds_path<-paste(DATASETS_PATH, args[2], args[3], sep='/')
prs_path<-paste(PRSS_PATH, paste(args[1],args[2],sep='_'), args[3], sep='/')
sub<-args[5]

if (is.na(sub)){
    sub=""

} else {
    s=unlist(strsplit(sub, "_"))
    pheno_name=paste0("_",s[2])
    if (is.na(s[3])){
        print("here")
        pop=""
    } else {
        pop=paste0("_",s[3])
    }
}


# Read p-values TH (Alternatively, for a predefined list, taking all SNPs )
if (file.exists(paste0(prs_path, "/", "prs.profile"))) {
     p.threshold<-c(-1)
} else {
     p.threshold<-unlist(strsplit(args[4], ","))
}

print('Read in the phenotype file')
phenotype <- read.table(paste(paste(DATASETS_PATH, args[2], sep='/') , paste0("pheno",sub), sep="/"), header=T)
print('Filter samples w/o phenotype')
phenotype=phenotype[phenotype$label!=-1,]
print('Read in the PCs')
pcs <- read.table(paste(ds_path, paste(paste0("ds",pop,".eigenvec")), sep="/"), header=F)
pcs <- pcs[,1:8]

# The default output from plink does not include a header. To make things simple, we will add the appropriate headers (1:6 because there are 6 PCs)
colnames(pcs) <- c("FID", "IID", paste0("PC",1:6)) 

print('Read in the covariates, if there is any (here, it is sex)')

print('Read covariates, if the file exists')
if (file.exists(paste(ds_path, "ds.covariate", sep="/"))){
    covariate <- read.table(paste(ds_path, "ds.covariate", sep="/"), header=T)
}

print('Merge PCs, covariates and phenotype #TODO include convariates')
pheno <-  merge(phenotype, pcs, by=c("FID"))
print(paste('Total number of phenotype rows after the merge:',nrow(pheno)))

# Calculate the null model (model with PRS) using linear regression against phenotype
print(unique(pheno[,'label']))
null.model2 <- glm(label~., data=pheno[,!colnames(pheno)%in%c("FID","IID", "IID.x", "IID.y")]-1, family=gaussian(link = "identity")) 

print('Calculate R2 of the null model')
null.r2 <- with(summary(null.model2), 1 - deviance/null.deviance) 

print('Calculate AUROC of the null model')
null.prediction <-  predict(null.model2,pheno[,!colnames(pheno)%in%c("FID","IID", "IID.x", "IID.y")])
null.roc.obj <-  roc(pheno[,'label'], null.prediction)
# null.roc.auc <-  auc(null.roc.obj)
# print(null.roc.auc)


print('Start looping thresholds')
prs.result <- NULL
# Go through each p-value threshold
for(i in p.threshold){
    print('Read PRS')
    if (i<0) {
        prs.file.name<-paste0(prs_path, "/", "prs",pop,".profile")
    } else {
        prs.file.name<-paste0(prs_path, "/", "prs",pop,".",i,".profile")
    }
    prs<-read.table(prs.file.name, header=T)
    print(paste('Total number of prs rows:',nrow(prs)))
    print('Merge the prs with the phenotype matrix')
    pheno.prs <-  merge(pheno, prs[,c("FID", "SCORE")], by=c("FID"))
    print(paste('Total number of phenotype rows after the merge:',nrow(pheno.prs)))
    print('Fits linear  regression on continuous phenotype with PRS and the covariates, including PCs (ignoring the FID and IID from our model)')
    prs.model2 <- glm(label~., data=pheno.prs[,!colnames(pheno.prs)%in%c("FID","IID", "IID.x", "IID.y")] , family=gaussian(link = "identity")) 

#     print('Calculates AUROC of full model')
#     prs.prediction <- predict(prs.model2,pheno.prs[,!colnames(pheno.prs)%in%c("FID","IID")]) 
#     prs.roc.obj <- roc(pheno.prs[,'label'], prs.prediction)
#     prs.roc.auc <- auc(prs.roc.obj)

    print('Calculates R2 of full model')
    prs.r2 <- with(summary(prs.model2), 1 - deviance/null.deviance) 
    all.r2 <- prs.r2-null.r2
#     all.roc.auc <- prs.roc.auc-null.roc.auc

    print('Get coeffcient, p-value, beta, SE')    
    print(summary(prs.model2)$coeff)
    prs.coef <- summary(prs.model2)$coeff["SCORE",]
    prs.beta <- as.numeric(prs.coef[1])
    prs.se <- as.numeric(prs.coef[2])
    prs.p <- as.numeric(prs.coef[4])

    print('Save statistics, and metrics (excluding ORs)')
    prs.result <- rbind(prs.result, data.frame(threshold=i, all_R2=all.r2, prs_R2=prs.r2, null_R2=null.r2, P=prs.p, BETA=prs.beta,SE=prs.se))
#     prs.result <- rbind(prs.result, data.frame(threshold=i, all_ngkR2=all.r2, prs_R2=prs.r2, null_R2=null.r2, roc_auc=prs.roc.auc, P=prs.p, BETA=prs.beta,SE=prs.se))

    print('print statistics and metrics (w/o OR)')
    write.table(prs.result, paste(prs_path,paste0("prs.statistics.",i,".tsv"), sep='/'), row.names = FALSE, sep='\t', quote = FALSE)
    print(prs.result)
    print(paste(prs_path,paste0("prs.statistics.",i,".tsv"), sep='/')) 

}
