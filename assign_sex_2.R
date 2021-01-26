source('constants.R')
args <- commandArgs(trailing = TRUE)  
path=paste0(DATASETS_PATH, args[1],'/')

# Read in file
valid <- read.table(paste0(path, "ds.valid.sample"), header=T)
dat <- read.table(paste0(path, "ds.QC.sexcheck"), header=T)
valid <- subset(dat, STATUS=="OK" & FID %in% valid$FID)
write.table(valid[,c("FID", "IID")], paste0(path, "ds.QC.valid"), row.names=F, col.names=F, sep="\t", quote=F) 
q() # exit R
