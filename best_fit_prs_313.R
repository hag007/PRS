.libPaths(c('../prs-R',.libPaths()))
library(dplyr)
library(epitools)
# library(oddsratio)
source('constants.R')
args <- commandArgs(trailing = TRUE)
gwas_path=paste0(GWASS_PATH, args[1],'/')
ds_path=paste(DATASETS_PATH, args[2], args[3], sep='/') 
prs_path=paste(PRSS_PATH, paste(args[1],args[2],sep='_'), args[3], sep='/')

# p.threshold <- c(0.001 ,0.05,0.1,0.2,0.3,0.4,0.5)
# Read in the phenotype file 
phenotype <- read.table(paste(paste(DATASETS_PATH, args[2], sep='/') , "pheno", sep="/"), header=T)
# Read in the PCs
pcs <- read.table(paste(ds_path, "ds.eigenvec", sep="/"), header=F)
pcs <- pcs[,1:8]

# The default output from plink does not include a header
# To make things simple, we will add the appropriate headers
# (1:6 because there are 6 PCs)
colnames(pcs) <- c("FID", "IID", paste0("PC",1:6)) 
# Read in the covariates (here, it is sex)
# covariate <- read.table("ds.covariate", header=T)
# Now merge the files
pheno <- merge(phenotype, pcs, by=c("FID","IID"))
# We can then calculate the null model (model with PRS) using a linear regression (as height is quantitative)
null.model <- lm(label~., data=pheno[,!colnames(pheno)%in%c("FID","IID")])
# And the R2 of the null model is 
null.r2 <- summary(null.model)$r.squared
null.adj.r2 <- summary(null.model)$adj.r.squared
prs.result <- NULL

# Go through each p-value threshold
prs <- read.table(paste0(prs_path, "/", "prs.profile"), header=T)
# Merge the prs with the phenotype matrix
# We only want the FID, IID and PRS from the PRS file, therefore we only select the 
# relevant columns
pheno.prs <- merge(phenotype, prs[,c("FID","IID", "SCORE")], by=c("FID", "IID")) ##### TODO: reverse phenotype --> pheno
# Now perform a linear regression on Height with PRS and the covariates
# ignoring the FID and IID from our model
print(paste("before filtering", nrow(pheno.prs)))
pheno.prs=pheno.prs[pheno.prs$label!=-1,]
print(paste("after filtering", nrow(pheno.prs)))
# print(pheno.prs[,!colnames(pheno.prs)%in%c("FID","IID")][1:10,])
print(paste("# of 0 label", nrow(pheno.prs[pheno.prs$label==0,])))
print(paste("# of 1 label", nrow(pheno.prs[pheno.prs$label==1,])))
model <- lm(label~., data=pheno.prs[,!colnames(pheno.prs)%in%c("FID","IID")])
# model R2 is obtained as 
model.r2 <- summary(model)$r.squared
model.adj.r2 <- summary(model)$adj.r.squared
        
# R2 of PRS is simply calculated as the model R2 minus the null R2
prs.r2 <- model.r2-null.r2
prs.adj.r2 <- model.adj.r2-null.adj.r2
# We can also obtain the coeffcient and p-value of association of PRS as follow
# print(summary(model)$coeff[1:10,])
prs.coef <- summary(model)$coeff["SCORE",]
prs.beta <- as.numeric(prs.coef[1])
prs.se <- as.numeric(prs.coef[2])
prs.p <- as.numeric(prs.coef[4])
# We can then store the results
prs.result <- rbind(prs.result, data.frame(p_threshold=1, score_R2=prs.r2, score_adjR2=prs.adj.r2, model_R2=model.r2, model_adjR2=model.adj.r2, P=prs.p, BETA=prs.beta,SE=prs.se))

write.table(prs.result, paste(prs_path,"prs.statistics.tsv", sep='/'), row.names = FALSE, sep='\t', quote = FALSE)

# }
print(prs.result)

total_healthy_n <- length(filter(pheno.prs, label==0))
total_case_n <- length(filter(pheno.prs, label==1))


df.or=data.frame()
qtls<-quantile(pheno.prs[,'SCORE'],c(0.1,0.2,0.4,0.6,0.8,0.9,0.95,0.99,1))
for(a_i in c(4,1:3,5:9)){
    a=qtls[a_i]
    a_prev=if (a_i-1==0) min(qtls)-0.1 else qtls[a_i-1]
    n_control <- nrow(filter(pheno.prs, label==0 & SCORE>a_prev & SCORE <=a))
    n_case <- nrow(filter(pheno.prs, label==1 & SCORE>a_prev & SCORE <=a)) 
    df.or <-rbind(df.or, data.frame(n_control=n_control, n_case=n_case)) # qtl=a, 
}   
df.or <- as.matrix(df.or) 
print(df.or)
or.fit <- oddsratio(df.or) # [,c('n_case','n_control')]
write.table(or.fit$measure, paste(prs_path,"prs.or.percentile.tsv", sep='/'), row.names = FALSE, sep='\t', quote = FALSE)
write.table(or.fit$p.value, paste(prs_path,"prs.or.p.value.tsv", sep='/'), row.names = FALSE, sep='\t', quote = FALSE)
print(or.fit)

pheno.prs[,'SCORE']=scale(pheno.prs[,'SCORE'])
OR.lgm <- glm(label ~ SCORE, data=pheno.prs, family=binomial(link="logit") )
df.or.all <- exp(cbind(coef(OR.lgm), confint(OR.lgm)))
df.or.all <- data.frame(df.or.all)
write.table(df.or.all, paste(prs_path,"prs.or.all.tsv", sep='/'), row.names = FALSE, sep='\t', quote = FALSE)
print(df.or.all)
#print(coef(model))
# print(or_glm(pheno.prs[,!colnames(pheno.prs)%in%c("FID","IID")], lm, list(SCORE=0.001), ci = 0.95))

q() # exit R
