#!/bin/bash
set -e

source constants_.sh
source parse_args.sh $@


if [[ -z $imp ]]; then
    imp="original"
fi

if [[ -z $imp_src ]]; then
    imp_src=$imp
fi

if [[ -z $imp_dest ]]; then
    imp_dest=$imp
fi

if [[ -z $imp_merged ]]; then
    imp_merged=$imp
fi

echo "start merging ${src}/${imp_src} and ${dest}/${imp_dest} into ${src}_${dest}/${imp_merged}..."

target_source_dataset="${datasets_path}${src}/${imp_src}/"
target_dest_dataset="${datasets_path}${dest}/${imp_dest}/"
merged_dataset="${datasets_path}${src}_${dest}/${imp_merged}/"


echo '# Prepare a directory for files to be merged'
{  mkdir -p ${merged_dataset}; } || { echo 'Skipping directory creation'; }

echo '# Merge integrated bfile with other integrated bfiles (e.g. 1000G)'
{
    plink -bfile ${target_source_dataset}ds --bmerge ${target_dest_dataset}ds --out ${merged_dataset}ds --memory 600000 --threads 80
} || {
    echo "Merging failed, possibly due to inconsistent SNPs between files.\nAttemping to filter these SNPs and merge again..."
    bash fix_two_bfiles_before_merge.sh --src ${src} --dest ${dest} --imp ${imp} --imp_src ${imp_src} --imp_dest ${imp_dest} --imp_merged ${imp_merged}
}
# For multiple files, run the line below
# plink -bfile ${target_source_dataset}ds --merge-list ${target_source_dataset}merge_list --out ${merged_dataset}ds; done'


