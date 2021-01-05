#!/bin/sh

source constants.sh
source chr_args.sh

dataset_source=$1
dataset_destination=$2

cat ${datasets_path}${dataset_source}/ds.vcf | awk '{(!a[$1, $2]++ && !b[$3]++)}' > ${dataset_path}${dataset_destination}/ds.vcf
