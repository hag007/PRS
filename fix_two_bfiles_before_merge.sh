set -e 
source constants.sh
source parse_args.sh $@

datasets_path=${private_base_path}

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


echo "start merging ${src}/${imp_src} and ${dest}/${imp_dest} into ${src}_${dest}/${imp_merged}"

target_source_dataset="${datasets_path}${src}/${imp_src}/"
target_dest_dataset="${datasets_path}${dest}/${imp_dest}/"
merged_dataset="${datasets_path}${src}_${dest}/${imp_merged}/"


plink --bfile ${target_source_dataset}ds --exclude ${merged_dataset}ds.missnp --make-bed --out ${merged_dataset}ds_${src}_fixed --memory 600000 --threads 80
plink --bfile ${target_dest_dataset}ds --exclude ${merged_dataset}ds.missnp --make-bed --out ${merged_dataset}ds_${dest}_fixed --memory 600000 --threads 80
plink --bfile ${merged_dataset}ds_${src}_fixed --bmerge ${merged_dataset}ds_${dest}_fixed --out ${merged_dataset}ds --memory 600000 --threads 80
