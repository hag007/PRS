.libPaths(c('../R-env/prs-R',.libPaths()))

source('constants.R')
source('utils.R')

library(bigsnpr)
library(data.table)
library(magrittr)
library(fmsb)
library(runonce)

grid.ids.default <- "0.5"
method<-'ld'
args <- commandArgs(trailing = TRUE)
parse.args(args, grid.ids.default,method)


print("Read in the train bed file")
ds.train.file.name <- paste(imp.train.path, paste0(ds.prefix,train.suffix), sep="/")
ds.train.processed.rds.file.name=paste0(ds.train.file.name, ".rds")
ds.train.processed.bk.file.name=paste0(ds.train.file.name, ".bk")
if (!file.exists(ds.train.processed.rds.file.name) || !file.exists(ds.train.processed.bk.file.name)){
    if (file.exists(ds.train.processed.rds.file.name)) {
        print("Removing old (orphan) rds file")
        file.remove(ds.train.processed.rds.file.name)
    }
    if (file.exists(ds.train.processed.bk.file.name)) {
        print("Removing old (orphan) bk file")
        file.remove(ds.train.processed.bk.file.name)
    }
    print("preprocess the bed file (only need to do once for each data set)")
    snp_readBed2(paste0(ds.train.file.name,".bed"))
}

print("Read in the test bed file")
ds.test.file.name <- paste(imp.test.path, paste0(ds.prefix,test.suffix), sep="/")
ds.test.processed.rds.file.name=paste0(ds.test.file.name, ".rds")
ds.test.processed.bk.file.name=paste0(ds.test.file.name, ".bk")
if (!file.exists(ds.test.processed.rds.file.name) || !file.exists(ds.test.processed.bk.file.name)){
    if (file.exists(ds.test.processed.rds.file.name)) {
        print("Removing old (orphan) rds file")
        file.remove(ds.test.processed.rds.file.name)
    }
    if (file.exists(ds.test.processed.bk.file.name)) {
        print("Removing old (orphan) bk file")
        file.remove(ds.test.processed.bk.file.name)
    }
    print("preprocess the bed file (only need to do once for each data set)")
    snp_readBed2(paste0(ds.test.file.name,".bed"), ncores=100)
}

print("now attach the test genotype object")
obj.bigSNP.test <- snp_attach(ds.test.processed.rds.file.name)