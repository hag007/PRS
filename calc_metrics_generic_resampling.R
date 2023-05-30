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
library(peperr)
source('constants.R')


percentile.or.power <- function(pheno.prs, df.or, or.fit){

    # for (a in seq(nrow(df.or))){
    #     p.per <- df.or[a,'n_control']/(df.or[1,'n_control']+df.or[a,'n_control'])
    #     n.per <- df.or[1,'n_case'] + df.or[1,'n_control'] + df.or[a,'n_case'] + df.or[a,'n_control']
    #     r.per <- (df.or[1,'n_control'] + df.or[a,'n_control'])/(df.or[1,'n_case'] + df.or[a,'n_case'])
    #     res.per <- epi.sscc(OR=or.fit$measure[a], p0=p.per, n=n.per, power=NA, r=r.per, rho.cc = 0, design = 1, sided.test = 2, nfractional = FALSE, conf.level = 0.95, method = "unmatched", fleiss = FALSE)
    #     print(paste("cur OR", quantiles[a], quantiles[a+1] ,res.per))
    # }

    p0.95 <- df.or[nrow(df.or)-1,'n_control']/(df.or[1,'n_control']+df.or[nrow(df.or)-1,'n_control'])
    n.95 <- df.or[1,'n_case'] + df.or[1,'n_control'] + df.or[nrow(df.or)-1,'n_case'] + df.or[nrow(df.or)-1,'n_control']
    r.95 <- (df.or[1,'n_control'] + df.or[nrow(df.or)-1,'n_control'])/(df.or[1,'n_case'] + df.or[nrow(df.or)-1,'n_case'])
    res.95 <- epi.sscc(OR=or.fit$measure[nrow(or.fit$measure)-1], p0=p0.95, n=n.95, power=NA, r=r.95, rho.cc = 0, design = 1, sided.test = 2, nfractional = FALSE, conf.level = 0.95, method = "unmatched", fleiss = FALSE)
    res.95 <- epi.sscc(OR=or.fit$measure[nrow(or.fit$measure)-1], p0=p0.95, n=n.95, power=NA, r=r.95, rho.cc = 0, design = 1, sided.test = 2, nfractional = FALSE, conf.level = 0.95, method = "unmatched", fleiss = FALSE)

    p0.99 <- df.or[nrow(df.or),'n_control']/(df.or[1,'n_control']+df.or[nrow(df.or),'n_control'])
    n.99 <- df.or[1,'n_case'] + df.or[1,'n_control'] + df.or[nrow(df.or),'n_case'] + df.or[nrow(df.or),'n_control']
    r.99 <- (df.or[1,'n_control'] + df.or[nrow(df.or),'n_control'])/(df.or[1,'n_case'] + df.or[nrow(df.or),'n_case'])
    res.99 <- epi.sscc(OR=or.fit$measure[nrow(or.fit$measure)], p0=p0.99, n=n.99, power=NA, r=r.99, rho.cc = 0, design = 1, sided.test = 2, nfractional = FALSE, conf.level = 0.95, method = "unmatched", fleiss = FALSE)
    res.99 <- epi.sscc(OR=or.fit$measure[nrow(or.fit$measure)], p0=p0.99, n=n.99, power=NA, r=r.99, rho.cc = 0, design = 1, sided.test = 2, nfractional = FALSE, conf.level = 0.95, method = "unmatched", fleiss = FALSE)
    
    return(list("res.95"=res.95, "res.99"=res.99))
}

percentile.or <- function(pheno.prs){
    df.or=data.frame()
    quantiles=c(0.1,0.2,0.3,0.4,0.6,0.7,0.8,0.9,1) # 0.95
    q_order= c(5,1:4,6:9) # c(6,1:5,7:11)
    # quantiles=c(0.2,0.3,0.4,0.6,0.7,0.8,1) # 0.95
    # q_order= c(4,1:3,5:7) # c(6,1:5,7:11)
    qtls<-quantile(pheno.prs[,'SCORE'],quantiles) 
        for(a_i in q_order){
        a=qtls[a_i]
        a_prev=if (a_i-1==0) min(qtls)-0.1 else qtls[a_i-1]
        n_control <- nrow(filter(pheno.prs, label==0 & SCORE>a_prev & SCORE <=a))
        n_case <- nrow(filter(pheno.prs, label==1 & SCORE>a_prev & SCORE <=a))
        df.or <-rbind(df.or, data.frame(n_control=n_control, n_case=n_case)) # qtl=a,
    }
    df.or <- as.matrix(df.or)
    df.or[(df.or[,1]==0) | (df.or[,2]==0),]=1
    # print(df.or)
    or.fit <- oddsratio(df.or) # [,c('n_case','n_control')]
    rownames(or.fit$measure)<- paste0(c(0,quantiles)[q_order]*100,"-",quantiles[q_order]*100)
    colnames(or.fit$measure)<- c("OR", "CI min", "CI max")
    ## print(or.fit)
    return(list("df.or"=df.or,"or.fit"=or.fit))  
}

basic.metrics <- function(prs.model, pheno.prs, null.ngk.r2, null.roc.auc, cur.grid.id){
    print('Calculates AUROC of full model')
    prs.prediction <- predict(prs.model,pheno.prs) 
    prs.roc.obj <- roc(pheno.prs[,'label'], prs.prediction)
    prs.roc.auc <- auc(prs.roc.obj)

    print('Calculates R2 of full model')
    prs.ngk.r2 <- PseudoR2(prs.model, which = 'Nagelkerke') # NagelkerkeR2(prs.model2) # r2_nagelkerke(model)
    all.ngk.r2 <- prs.ngk.r2-null.ngk.r2
    all.roc.auc <- prs.roc.auc-null.roc.auc

    print('Get coeffcient, p-value, beta, SE')
    
    print(summary(prs.model)$coeff)
    prs.coef <- summary(prs.model)$coeff["SCORE",]
    prs.beta <- as.numeric(prs.coef[1])
    prs.se <- as.numeric(prs.coef[2])
    prs.p <- as.numeric(prs.coef[4])

    return(data.frame(threshold=cur.grid.id, all_ngkR2=all.ngk.r2, prs_ngkR2=prs.ngk.r2, null_ngkR2=null.ngk.r2, roc_auc=prs.roc.auc, P=prs.p, BETA=prs.beta,SE=prs.se))

}

power.or <- function(pheno.prs, df.or.all){
    total.healthy.n <- nrow(filter(pheno.prs, label==0))
    total.case.n <- nrow(filter(pheno.prs, label==1))
    p0 <- total.case.n/(total.case.n+total.healthy.n)
    p0.or <- total.case.n/total.healthy.n
    p1.or <- df.or.all[nrow(df.or.all),1]
    p1 <- (p0.or*p1.or)/(1+p0.or*p1.or)
    return(wp.logistic(n = nrow(pheno.prs), p0 = p0 , p1 = p1 , family='normal', alpha = 0.05)['power'])
}

or.per.1.sd <- function(pheno.prs){
        tryCatch({
        for (a in colnames(pheno.prs)){
            if(a == 'SCORE'){
                pheno.prs[,a]=scale(pheno.prs[,a])
            }
        }
        # pheno.prs[,'SCORE_SCALE']=scale(pheno.prs[,'SCORE'])
        OR.glm <- glm(label ~ . , data=pheno.prs , family=binomial(link="logit")) # [,!colnames(pheno.prs)%in%c("SCORE")]
        df.or.all.log <- cbind(coef(OR.glm), confint(OR.glm))
        df.or.all <- exp(df.or.all.log)
        return(data.frame(df.or.all))
        },
        error=function(error_message) {return(NA)})
}

 
calc.metrics <- function(src.path, imp.name, res.path, sub, grid.ids, prs.prefix, suffix, rep){

    print('Read in the phenotype file')
    phenotype <- read.table(paste(target.path, paste0("pheno",sub,suffix), sep="/"), header=T)

    print('Filter samples w/o phenotype')
    phenotype=phenotype[phenotype$label!=-1,]
    print('Read in the PCs')
    pcs <- read.table(paste(src.path, imp.name, paste(paste0("ds",sub, suffix,".eigenvec")), sep="/"), header=F)
    pcs <- pcs[,1:8]
    
    # The default output from plink does not include a header. To make things simple, we will add the appropriate headers (1:6 because there are 6 PCs)
    colnames(pcs) <- c("FID", "IID", paste0("PC",1:6)) 
    
    print('Read in the covariates, if there is any (here, it is sex)')

    print('Merge PCs, covariates and phenotype')
    print(colnames(phenotype))
    print(colnames(pcs))
    pheno <-  merge(phenotype, pcs, by=c("FID"))
    print('Read covariates, if the file exists')
    print('Check if covariates file exists')
    print(paste(cov.path, "cov", sep="/"))
    if (file.exists(paste(cov.path, "cov", sep="/"))){
        print('Read covariates file')
        covariate <- read.table(paste(cov.path, "cov", sep="/"), header=T)
        print('Merge covariates and phenotype')
        pheno <-  merge(pheno, covariate, by=c("FID"))
    }
    print(paste(cov.path, "pop.panel", sep="/"))
    if (file.exists(paste(cov.path, "pop.panel", sep="/"))){
        print('Read pop.panel file')
        pop.panel <- read.table(paste(cov.path, "pop.panel", sep="/"), header=T)
        print('Merge covariates and phenotype')
        # pheno <-  merge(pheno, pop.panel, by=c("FID"))
        # pheno <- pheno[,!colnames(pheno)%in%c("super_pop", "pop")]
    }
    print('Clean redundant colums')
    pheno <- pheno[,!colnames(pheno)%in%c("FID.1", "IID", "IID.x", "IID.y", "IID.y.1", "IID.x.1")]
    print('Adjust label values for GLM')
    pheno[,'label'] <- pheno[,'label']-1
    print(paste('Total number of phenotype rows after the merge:',nrow(pheno)))
    print(head(pheno))
    print(tail(pheno))
    # Calculate the null model (model with PRS) using a logistic regression against phenotype
    null.model <- glm(label~., data=pheno[,!colnames(pheno)%in%c("FID")], family=binomial(link="logit")) # binomial(link="logit")

    print('Calculate R2 of the null model')
    null.ngk.r2 <-  PseudoR2(null.model, which = 'Nagelkerke') # NagelkerkeR2(model2)

    print('Calculate AUROC of the null model')
    null.prediction <-  predict(null.model,pheno[,!colnames(pheno)%in%c("FID")])
    null.roc.obj <-  roc(pheno[,'label'], null.prediction)
    null.roc.auc <-  auc(null.roc.obj)
    print(null.roc.auc)

    print('Start looping grid.ids')
    prs.result <- NULL
    # Go through each p-value threshold
    for(i in grid.ids){
        print('Read PRS')
        if (i<0) {
            prs.file.name<-paste(res.path, paste0(prs.prefix,suffix,".profile"), sep='/')
        } else {
            prs.file.name<-paste(res.path, paste0(prs.prefix,suffix,".",i,".profile"), sep='/')
        }
        if (!file.exists(prs.file.name)){
            print(paste0("The file ", prs.file.name, " does not exist. Skipping..."))
            next
        } else{
            print(paste0("Found ", prs.file.name, ". Start processing..."))

        }

        prs<-read.table(prs.file.name, header=T)
        print(paste('Total number of prs rows:',nrow(prs)))

        print('Merge the prs with the phenotype matrix')
        # print(colnames(pheno))
        # print(colnames(prs))
        pheno.prs.original <-  merge(pheno, prs[,c("FID", "SCORE")], by=c("FID"))
        sample.res<-resample.indices(dim(pheno.prs.original)[1], sample.n = 2000, method = "boot")
        or1sds=c()
        or99s=c()
        idx=1
        while (length(or1sds)<1000){
            print(paste0("idx: ",idx))
            print(paste0("length(or1sds): ",length(or1sds)))
            # print(cur.sample)
            pheno.prs<-pheno.prs.original[unlist(sample.res$sample.index[idx]),]
            # q()

            print("drop FID column")
            pheno.prs <- pheno.prs[,!colnames(pheno.prs)%in%c("FID")]
            print(paste('Total number of phenotype rows after the merge:',nrow(pheno.prs)))

            print('Perform a logistic regression on (binary) phenotype with PRS and the covariates, including PCs (ignoring the FID and IID from our model)')
            prs.model <- glm(label~., data=pheno.prs, family=binomial(link="logit")) # binomial(link="logit")

            if (! ("SCORE" %in% rownames(summary(prs.model)$coeff))){
                print("Warning: Could not infer estimates for PRS score. This might happen if all values are identical (probably 0). Assign zeros to estimates")
                next;
            }

            print('Save statistics, and metrics (excluding ORs)')
            cur.basic.metrics <- basic.metrics(prs.model, pheno.prs, null.ngk.r2, null.roc.auc, i)
            prs.result <- rbind(prs.result, cur.basic.metrics)


            print('Calculate OR of logistic regression')

            df.or.all <- or.per.1.sd(pheno.prs)
            if(all(is.na(df.or.all))){ next}
            write.table(df.or.all, paste(res.path,paste0(prs.prefix,suffix,".or.all.",i,".tsv"), sep='/'), row.names = FALSE, sep='\t', quote = FALSE)

            or1sds=c(or1sds,df.or.all[nrow(df.or.all),1])
            if(T){
                print('Calculate power for OR of logistic regression')
                res.wp <- power.or(pheno.prs, df.or.all)

                print ('Calculate stratified OR (by percentiles)')
                res <- percentile.or(pheno.prs)
                df.or <- res$df.or
                or.fit <- res$or.fit

                write.table(or.fit$measure, paste(res.path,paste0(prs.prefix,suffix,".or.percentile.",i,".tsv"), sep='/'), col.names= NA, row.names = TRUE, sep='\t', quote = FALSE)
                write.table(or.fit$p.value, paste(res.path,paste0(prs.prefix,suffix,".or.p.value.",i,".tsv"), sep='/'), row.names = FALSE, sep='\t', quote = FALSE)

                print('Calculate power for stratified OR (by percentiles)')
                powers <- percentile.or.power(pheno.prs, df.or, or.fit)
                or99s=c(or99s,or.fit$measure[nrow(or.fit$measure),1])
                res.or.analysis <- data.frame(threshold=i,
                    or_all=df.or.all[nrow(df.or.all),1], or_all_power=res.wp,
                    or_95=or.fit$measure[nrow(or.fit$measure)-1,1], or_95_ci_min=or.fit$measure[nrow(or.fit$measure)-1,2], or_95_ci_max=or.fit$measure[nrow(or.fit$measure)-1,3], or_95_power=powers$res.95$power,
                    or_99=or.fit$measure[nrow(or.fit$measure),1], or_99_ci_min=or.fit$measure[nrow(or.fit$measure),2], or_99_ci_max=or.fit$measure[nrow(or.fit$measure),3], or_99_power=powers$res.99$power )
                write.table(res.or.analysis, paste(res.path,paste0(prs.prefix,suffix,".or.summary.",i,".tsv"), sep='/'), row.names = FALSE, sep='\t', quote = FALSE)



                print('print statistics and metrics (w/o OR)')
                write.table(prs.result, paste(res.path,paste0(prs.prefix,suffix,".statistics.",i,".tsv"), sep='/'), row.names = FALSE, sep='\t', quote = FALSE)
                print(res.or.analysis)
                print(prs.result)
                print(paste(res.path,paste0(prs.prefix,suffix,".statistics.",i,".tsv"), sep='/'))
            }

            idx<-idx+1
        }
        print("or1sds")
        print(mean(or1sds))
        print(sd(or1sds))
        print("or99s")
        print(mean(or99s))
        print(sd(or99s))
    }
}
