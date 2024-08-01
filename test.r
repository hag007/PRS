.libPaths(c('../R-env/prs-R',.libPaths()))

setwd('/specific/elkon/maibendayan/PRS/codebase')

pheno <- "pheno"
gwas_file <- "gwas.tsv"

discovery <- "bcac_onco_eur-5pcs"
target <- "humc19"
imp <- "impute2_1kg_eur-multi"

source("/specific/elkon/maibendayan/PRS/codebase/const.r")
PRS_DATASETS_ELKON<-"/specific/elkon/hagailevi/PRS/datasets/dec/"
discovery_path <- paste(PRS_GWASS, discovery, sep="/")
target_path <- paste(PRS_DATASETS_ELKON,target,imp, sep="/")
prs_path <- paste(PRS_PRSS,paste(discovery,target,sep="_"), sep="/")
pheno_path <- paste(PRS_DATASETS_ELKON, target, sep="/")


library(bigsnpr)
library(data.table)
library(magrittr)
library(runonce)

print("0. Prepare workspace")
options(bigstatsr.check.parallel.blas = FALSE)
options(default.nproc.blas = NULL)



print("1. Read in the phenotype and covariate files")

print('Read in the phenotype file')
phenotype <- fread(paste(pheno_path, "pheno", sep="/"))
# covariate <- fread("EUR.cov")

print('Filter samples w/o phenotype')
phenotype <- phenotype[phenotype$label!=-1,]

print('Calibrate label values')
phenotype[,'label']=phenotype[,'label']-1

print('Read in the PCs')
pcs <- fread(paste(target_path, "ds.eigenvec", sep="/"))
pcs <- pcs[,1:8]

print('Rename columns')
colnames(pcs) <- c("FID","IID", paste0("PC",1:6))

print('Generate required table')
pheno <- merge(phenotype, pcs)

print("2. Obtain HapMap3 SNPs")
info_file_path <- paste(prs_path, "map_hm3_ldpred2_local.rds", sep = "/")

if (!file.exists(info_file_path)) {
    print("download info file")
    info <- readRDS(runonce::download_file(
      "https://ndownloader.figshare.com/files/25503788",
      fname = "map_hm3_ldpred2.rds"))
    print("Save the 'info' object to a local RDS file")
    saveRDS(info, file = info_file_path)
}else {
    print("Load pre-existing 'info' object")
    info <- readRDS(info_file_path)
}



print("3. Load and transform the summary statistic file")
sumstats_file_path <- paste(discovery_path, "sumstats.ld.rds", sep = "/")

if (!file.exists(sumstats_file_path)) {
    print("Read in the summary statistic file")
    sumstats <- read.table(paste(discovery_path, paste0("gwas.QC.gz"), sep="/"), header=T) # bigreadr::fread2(paste(discovery_path, "bca_snps.QC.tsv", sep="/")) 

    # LDpred 2 require the header to follow the exact naming!!!!!! (change if needed)
    print('Rename header to follow LDpred 2 naming convension')
    names(sumstats) <-
        c("rsid",
        "chr",
        "pos",
        "a1",
        "a0",
        "MAF",
        "beta_se",
        "p",
        "n_eff",
        "INFO",
        "beta")
    # Transform the OR into log(OR) (#####actually not since in our datas beta is OR)
#     sumstats$beta <- sumstats$OR
    print("Filter out hapmap SNPs")
    sumstats <- sumstats[sumstats$rsid%in% info$rsid,]

    print("Save the 'sumstats' object to a local RDS file")
    saveRDS(sumstats, file = sumstats_file_path)
}else {
    print("Load pre-existing 'stat' object")
    sumstats <- readRDS(sumstats_file_path)
}

# print(head(readRDS(paste(target_path, "ds.QC.rds", sep = "/"))))

# print(names(readRDS(paste(target_path, "ds.QC.rds", sep = "/"))))

# print(head(readRDS("/specific/elkon/maibendayan/train0808_data/EUR.QC.rds")))

setwd(target_path)

# Get maximum amount of cores
# NCORES <- nb_cores() #=87 originally
print("3 (2). Calculate the LD matrix")

NCORES <- 40
print("# Open a temporary file")
cache.folder <- paste(paste(target_path, sep='/') ,"tmp-data", sep="/")
unlink(cache.folder, recursive=TRUE)
tmp <- tempfile(tmpdir = cache.folder)
on.exit(file.remove(paste0(tmp, ".sbk")), add = TRUE)

print("Initialize variables for storing the LD score and LD matrix")
corr <- NULL
ld <- NULL
print("We want to know the ordering of samples in the bed file") 
fam.order <- NULL
# preprocess the bed file (only need to do once for each data set)
print("Read in the train bed file")
rds_file_path <- paste(target_path, "ds.QC.rds", sep = "/")
if (!file.exists(rds_file_path)) {
    print("preprocess the bed file (only need to do once for each data set)")
    snp_readBed(paste(target_path, "ds.QC.bed", sep="/"))
}

# snp_readBed func reads the bed file, but also requests the presesnce of bim and fam file.#
# as it reads the file, it creates a backup (.bk) and .rds files in the same folder.#

print("now attach the genotype object")
obj.bigSNP <- snp_attach(rds_file_path)
print("extract the SNP information from the genotype")
map <- obj.bigSNP$map[-3]
names(map) <- c("chr", "rsid", "pos", "a1", "a0")   ###here it stays in the same order - .rds format.

print("perform SNP matching")
info_snp <- snp_match(sumstats, map)   
print("Assign the genotype to a variable for easier downstream analysis")
genotype <- obj.bigSNP$genotypes
print("here0")
# Rename the data structures
CHR <- map$chr
POS <- map$pos
# get the CM information from 1000 Genome
# will download the 1000G file to the current directory (".")
POS2 <- snp_asGeneticPos(CHR, POS, dir = prs_path)
print("here0.5")


# calculate LD
print("Rename the data structures??? TBD: \"rename\" vs \"naming\"")
ld_matrix_path <- paste(prs_path, "ld_matrix", sep="/")
ld_corr_path <- paste(prs_path, "ld_corr", sep="/")

print("TBD: Check why forcing the else statement ('&& F')")
if (file.exists(ld_matrix_path) && file.exists(ld_corr_path) && F){ 
    ld <- load(ld_matrix_path)
    corr <- load(ld_corr_path)
} else{
    for (chr in 22:22) {
    #     print("here1")
        print("Extract SNPs that are included in the chromosome")
        ind.chr <- which(info_snp$chr == chr)
        ind.chr2 <- info_snp$`_NUM_ID_`[ind.chr]
    #     print("here2")
        # Calculate the LD
        print(paste0("Calculate the LD for chromosome ",chr))
        corr0 <- snp_cor(
                genotype,
                ind.col = ind.chr2,
                ncores = NCORES,
                infos.pos = POS2[ind.chr2],
                size = 3 / 1000
            )
    #     print("here4")
        if (sum(is.na(corr0))!=0){
            print(paste0("found NA in chr",chr, "(n=", sum(is.na(corr0)),")"))
            corr0[is.na(corr0)]<-1
        } else{
            print(paste("no NA in chr",chr))
        }
        if (chr == 22) {
            ld <- Matrix::colSums(corr0^2)
#             print(dim(corr0))
#             q()
            corr <- as_SFBM(corr0, tmp)
        } else {
            ld <- c(ld, Matrix::colSums(corr0^2))
            corr$add_columns(corr0, nrow(corr))
    #         print("here5")
        }
    }
#     save(ld, file=ld_matrix_path)
#     save(corr, file=ld_corr_path)
}
print("here2.5")
# # We assume the fam order is the same across different chromosomes
# fam.order <- as.data.table(obj.bigSNP$fam)
# # Rename fam order
# setnames(fam.order,
#         c("family.ID", "sample.ID"),
#         c("FID", "IID"))
# print("here3")

df_beta <- info_snp[,c("beta", "beta_se", "n_eff", "_NUM_ID_")]
ldsc <- snp_ldsc(   ld, 
                    length(ld), 
                    chi2 = (df_beta$beta / df_beta$beta_se)^2,
                    sample_size = df_beta$n_eff, 
                    blocks = NULL)
h2_est <- ldsc[["h2"]]

# Prepare data for grid model
p_seq <- signif(seq_log(1e-4, 1, length.out = 17), 2)
h2_seq <- round(h2_est * c(0.7, 1, 1.4), 4)
grid.param <-
    expand.grid(p = p_seq,
            h2 = h2_seq,
            sparse = c(FALSE, TRUE))
# Get adjusted beta from grid model
beta_grid <-
    snp_ldpred2_grid(corr, df_beta, grid.param, ncores = NCORES)

# print("beta_grid:\n")
# print(head(beta_grid))

# if(is.null(obj.bigSNP)){
#     obj.bigSNP <- snp_attach(paste(target_path, "ds.QC.rds", sep="/"))
# }
# genotype <- obj.bigSNP$genotypes
# # calculate PRS for all samples
# ind.test <- 1:nrow(genotype)
# pred_grid <- big_prodMat(   genotype, 
#                             beta_grid, 
#                             ind.col = info_snp$`_NUM_ID_`)
# print("pred_grid:\n")
# print(head(pred_grid))
# write.table(pred_grid, file=paste(prs_path, "ds.ld.pred_grid",sep="/"))

fnames<-c()
for(a in 1:ncol(beta_grid)){
    if(!is.na(beta_grid[,a])){
        output<-cbind(info_snp[,c("chr","rsid","pos","a0","a1")],beta_grid[,a])
        fname<-paste0(prs_path,"/ld.",a,".weights")
        print(paste0('out file: ',paste(prs_path,'ldpred',fname, sep='/')))
        write.table(output, paste(prs_path,'ldpred',fname, sep='/'), row.names = FALSE, col.names = FALSE, sep='\t', quote=FALSE)
        fnames<-c(fnames, fname)
    }
}
write(fnames, file = paste(prs_path,'ldpred','all', sep='/'), sep='\n')


print(paste0("/ls.",paste(1,5,sep="-"),".weights"))


