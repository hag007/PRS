.libPaths(c('../prs-R',.libPaths()))
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

# Read p-values TH (Alternatively, for a predefined list, taking all SNPs )
if (file.exists(paste0(prs_path, "/", "prs.profile"))) {
    p.threshold<-c(-1)
} else {
     p.threshold<-as.numeric(unlist(strsplit(args[4], ",")))
}

print('Read in the phenotype file')
phenotype <- read.table(paste(paste(DATASETS_PATH, args[2], sep='/') , "pheno", sep="/"), header=T)
print('Filter samples w/o phenotype')
phenotype=phenotype[phenotype$label!=-1,]
print('Read in the PCs')
pcs <- read.table(paste(ds_path, "ds.eigenvec", sep="/"), header=F)
pcs <- pcs[,1:8]

# The default output from plink does not include a header. To make things simple, we will add the appropriate headers (1:6 because there are 6 PCs)
colnames(pcs) <- c("FID", "IID", paste0("PC",1:6)) 
print('Read in the covariates, if there is any (here, it is sex)')

print('Read covariates, if the file exists')
if (file.exists(paste(ds_path, "ds.covariate", sep="/"))){
    covariate <- read.table(paste(ds_path, "ds.covariate", sep="/"), header=T)
}

print('Merge PCs, covariates and phenotype #TODO include convariates')
pheno <- merge(phenotype, pcs, by=c("FID","IID"))
# Calculate the null model (model with PRS) using a logistic regression against phenotype
null.model2 <- glm(label~., data=pheno[,!colnames(pheno)%in%c("FID","IID")], family=binomial(link="logit")) # binomial(link="logit")

print('Calculate R2 of the null model')
null.ngk.r2 <- PseudoR2(null.model2, which = 'Nagelkerke') # NagelkerkeR2(model2)

print('Calculate AUROC of the null model')
null.prediction <- predict(null.model2,pheno[,!colnames(pheno)%in%c("FID","IID")])
null.roc.obj <- roc(pheno[,'label'], null.prediction)
null.roc.auc <- auc(null.roc.obj)
print(null.roc.auc)


print('Start looping thresholds')
prs.result <- NULL
# Go through each p-value threshold
for(i in p.threshold){
    print('Read PRS')
    if (i<0) {
        prs.file.name<-paste0(prs_path, "/", "prs.profile")
    } else {
        prs.file.name<-paste0(prs_path, "/", "prs.",i,".profile")
    }
    prs<-read.table(prs.file.name, header=T)

    print('Merge the prs with the phenotype matrix')
    pheno.prs <- merge(pheno, prs[,c("FID","IID", "SCORE")], by=c("FID", "IID"))

    print('Perform a logistic regression on (binary) phenotype with PRS and the covariates, including PCs (ignoring the FID and IID from our model)')
    prs.model2 <- glm(label~., data=pheno.prs[,!colnames(pheno.prs)%in%c("FID","IID")] , family=binomial(link="logit")) # binomial(link="logit")

    print('Calculates AUROC of full model')
    prs.prediction <- predict(prs.model2,pheno.prs[,!colnames(pheno.prs)%in%c("FID","IID")]) 
    prs.roc.obj <- roc(pheno.prs[,'label'], prs.prediction)
    prs.roc.auc <- auc(prs.roc.obj)

    print('Calculates R2 of full model')
    prs.ngk.r2 <- PseudoR2(prs.model2, which = 'Nagelkerke') # NagelkerkeR2(prs.model2) # r2_nagelkerke(model)
    all.ngk.r2 <- prs.ngk.r2-null.ngk.r2
    all.roc.auc=prs.roc.auc-null.roc.auc

    print('Get coeffcient, p-value, beta, SE')
    
    print('print(summary(prs.model2)$coeff)')
    prs.coef <- summary(prs.model2)$coeff["SCORE",]
    prs.beta <- as.numeric(prs.coef[1])
    prs.se <- as.numeric(prs.coef[2])
    prs.p <- as.numeric(prs.coef[4])

    print('Save statistics, and metrics (excluding ORs)')
    prs.result <- rbind(prs.result, data.frame(threshold=i, all_ngkR2=all.ngk.r2, prs_ngkR2=prs.ngk.r2, null_ngkR2=null.ngk.r2, roc_auc=prs.roc.auc, P=prs.p, BETA=prs.beta,SE=prs.se))

    total_healthy_n <- nrow(filter(pheno.prs, label==0))
    total_case_n <- nrow(filter(pheno.prs, label==1))

    print('Calculate OR of logistic regression')
    pheno.prs[,'SCORE_SCALE']=scale(pheno.prs[,'SCORE'])
    OR.glm <- glm(label ~ . , data=pheno.prs[,!colnames(pheno.prs)%in%c("FID","IID", "SCORE")] , family=binomial(link="logit") )
    df.or.all.log <- cbind(coef(OR.glm), confint(OR.glm))
    df.or.all <- exp(df.or.all.log)
    print(df.or.all)
    print(df.or.all[nrow(df.or.all),1])
    print(total_case_n/(total_case_n+total_healthy_n))
    df.or.all <- data.frame(df.or.all)
    write.table(df.or.all, paste(prs_path,"prs.or.all.tsv", sep='/'), row.names = FALSE, sep='\t', quote = FALSE)

    print ('Calculate power for OR of logistic regression')
    p0 <- total_case_n/(total_case_n+total_healthy_n)
    p0.or <- total_case_n/total_healthy_n
    p1.or <- df.or.all[nrow(df.or.all),1]
    p1 <- (p0.or*p1.or)/(1+p0.or*p1.or)
    res.wp <- wp.logistic(n = nrow(phenotype), p0 = p0 , p1 = p1 , family='normal', alpha = 0.05)['power']

    print ('Calculate stratified OR (by percentiles)')

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

    print('Calculate power for stratified OR (by percentiles)')
    p0.95 <- df.or[nrow(df.or)-1,'n_control']/(df.or[1,'n_control']+df.or[nrow(df.or)-1,'n_control'])
    n.95 <- df.or[1,'n_case'] + df.or[1,'n_control'] + df.or[nrow(df.or)-1,'n_case'] + df.or[nrow(df.or)-1,'n_control']
    r.95 <- (df.or[1,'n_control'] + df.or[nrow(df.or)-1,'n_control'])/(df.or[1,'n_case'] + df.or[nrow(df.or)-1,'n_case'])
    res.95 <- epi.sscc(OR=or.fit$measure[nrow(or.fit$measure)-1], p0=p0.95, n=n.95, power=NA, r=r.95, rho.cc = 0, design = 1, sided.test = 2, nfractional = FALSE, conf.level = 0.95, method = "unmatched", fleiss = FALSE)
    p0.99 <- df.or[nrow(df.or),'n_control']/(df.or[1,'n_control']+df.or[nrow(df.or),'n_control'])
    n.99 <- df.or[1,'n_case'] + df.or[1,'n_control'] + df.or[nrow(df.or),'n_case'] + df.or[nrow(df.or),'n_control']
    r.99 <- (df.or[1,'n_control'] + df.or[nrow(df.or),'n_control'])/(df.or[1,'n_case'] + df.or[nrow(df.or),'n_case'])
    res.99 <- epi.sscc(OR=or.fit$measure[nrow(or.fit$measure)], p0=p0.99, n=n.99, power=NA, r=r.99, rho.cc = 0, design = 1, sided.test = 2, nfractional = FALSE, conf.level = 0.95, method = "unmatched", fleiss = FALSE)

    res.or.analysis <- data.frame(threshold=i , or_all=df.or.all[nrow(df.or.all),1], or_all_power=res.wp, or_95=or.fit$measure[nrow(or.fit$measure)-1,1], or_95_ci_min=or.fit$measure[nrow(or.fit$measure)-1,2], or_95_ci_max=or.fit$measure[nrow(or.fit$measure)-1,3], or_95_power=res.95$power ,or_99=or.fit$measure[nrow(or.fit$measure),1], or_99_ci_min=or.fit$measure[nrow(or.fit$measure),2], or_99_ci_max=or.fit$measure[nrow(or.fit$measure)-1,3], or_99_power=res.99$power )
    write.table(res.or.analysis, paste(prs_path,"prs.or.summary.tsv", sep='/'), row.names = FALSE, sep='\t', quote = FALSE)

}

print('print statistics and metrics (w/o OR)')
write.table(prs.result, paste(prs_path,"prs.statistics.tsv", sep='/'), row.names = FALSE, sep='\t', quote = FALSE)
