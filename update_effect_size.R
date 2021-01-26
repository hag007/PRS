source('constants.R')
args <- commandArgs(trailing=TRUE)
prefix <- paste0(args[1],'/')
dat <- read.table(gzfile(paste0(GWASS_PATH, prefix, "gwas.QC.gz")), header=T)
dat$OR <- log(dat$OR)
write.table(dat, paste0(GWASS_PATH, prefix, "gwas.QC.Transformed"), quote=F, row.names=F)
q() # exit R

