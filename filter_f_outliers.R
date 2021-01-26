source('constants.R')

args <- commandArgs(trailing = TRUE)  

dataset_name=paste(args[1],args[2],sep='/')
dat <- read.table(paste(DATASETS_PATH, dataset_name, 'ds.QC.het', sep='/'), header=T) # Read in the EUR.het file, specify it has header
m <- mean(dat$F) # Calculate the mean  
s <- sd(dat$F) # Calculate the SD
valid <- subset(dat, F <= m+3*s & F >= m-3*s) # Get any samples with F coefficient within 3 SD of the population mean
write.table(valid[,c(1,2)], paste(DATASETS_PATH, dataset_name, "ds.valid.sample", sep='/'), quote=F, row.names=F) # print FID and IID for valid samples
q() # exit R
