source('constants.R')    


args <- commandArgs(trailing = TRUE)  
gwas_name=paste0(args[1],'/')
discovery_name=paste0(args[2], '/dec/')

options(error=function()traceback(2))


# Read in bim file
prefix=paste0(DATASETS_PATH, discovery_name, 'ds')
bim <- read.table(paste0(prefix, ".bim"))
colnames(bim) <- c("CHR", "SNP", "CM", "BP", "B.A1", "B.A2")
# Read in QCed SNPs
qc <- read.table(paste0(prefix, ".QC.snplist"), header = F, stringsAsFactors = F)
# Read in GIANT data
height <-
    read.table(gzfile(paste0(GWASS_PATH, gwas_name, "gwas.QC.gz")),
               header = T,
               stringsAsFactors = F, 
               sep="\t")
# Change all alleles to upper case for easy comparison
height$A1 <- toupper(height$A1)
height$A2 <- toupper(height$A2)
bim$B.A1 <- toupper(bim$B.A1)
bim$B.A2 <- toupper(bim$B.A2)

# Merge GIANT with target
info <- merge(bim, height, by = c("SNP", "CHR", "BP"))
# Filter QCed SNPs
info <- info[info$SNP %in% qc$V1,]
# Function for finding the complementary allele
complement <- function(x) {
    switch (
        x,
        "A" = "T",
        "C" = "G",
        "T" = "A",
        "G" = "C",
        return(NA)
    )
}
# Get SNPs that have the same alleles across base and target
info.match <- subset(info, A1 == B.A1 & A2 == B.A2)
# Identify SNPs that are complementary between base and target
info$C.A1 <- sapply(info$B.A1, complement)
info$C.A2 <- sapply(info$B.A2, complement)
info.complement <- subset(info, A1 == C.A1 & A2 == C.A2)
# Update these allele coding in the bim file
bim[bim$SNP %in% info.complement$SNP,]$B.A1 <-
    sapply(bim[bim$SNP %in% info.complement$SNP,]$B.A1, complement)
bim[bim$SNP %in% info.complement$SNP,]$B.A2 <-
    sapply(bim[bim$SNP %in% info.complement$SNP,]$B.A2, complement)

# identify SNPs that need recoding
info.recode <- subset(info, A1 == B.A2 & A2 == B.A1)
# identify SNPs that need recoding & complement
info.crecode <- subset(info, A1 == C.A2 & A2 == C.A1)
# Update these allele coding in the bim file
com.snps <- bim$SNP %in% info.crecode$SNP
tmp <- bim[com.snps,]$B.A1
bim[com.snps,]$B.A1 <- as.character(sapply(bim[com.snps,]$B.A2, complement))
bim[com.snps,]$B.A2 <- as.character(sapply(tmp, complement))
# Output updated bim file
bim_t <- apply(bim,2,as.character)
dim(bim_t)
write.table(
    bim_t,
    paste0(prefix, ".QC.adj.bim"),
    quote = F,
    row.names = F,
    col.names = F
)

mismatch <-
    bim$SNP[!(bim$SNP %in% info.match$SNP |
                  bim$SNP %in% info.complement$SNP | 
                  bim$SNP %in% info.recode$SNP |
                  bim$SNP %in% info.crecode$SNP)]

# mismatch <- apply(mismatch,2,as.character)
write.table(
    mismatch,
    paste0(prefix, ".mismatch"),
    quote = F,
    row.names = F,
    col.names = F
)
q() # exit R
