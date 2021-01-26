cat gwas_raw.txt | awk -v OFS="\t" '{if (index($0,"rs") || NR==1) {gsub(":[^ ]* "," "); $1=$1; {print;next}; print $0}}' > gwas.tsv
