source parse_args.sh "$@"

# this script splits each train/test pheno file into 2, then prepares datasets for the multi script.
# output: two files with the suffix of 0 and 1 respectfully (pheno / ds .... train/test)
#recievs the input of discovery, target, imp, n_repetitions, n_folds, ratio
#for example for the ratio 20:80 the input will be 80 ; train0 contains 80%, train1 contains 20%

#PRE: create_cv_repetitions

#n_repetitions=6
#n_folds=5
if [[ -z $base_rep ]]; then base_rep=$((n_repetitions+99)); fi
ratio=80
if [[ -z $target ]]; then target="mai_cimba_eur_brca1_icogs"; fi

if [[ -z $hapmap_snps_only || $hapmap_snps_only == false ]]; then hapmap_param=""; else hapmap_param="--hapmap_snps_only=true"; fi

# split train data
inner_data="train"
outer_data="both"

# split test data , recommended ratio=50
#inner_data="validation"
#outer_data="test"

for cur_rep in $(seq 1 ${n_repetitions}); do
	rep="${base_rep}_${cur_rep}"
	for cur_fold in $(seq 1 ${n_folds}); do 
	    pheno_file_path="${PRS_DATASETS_ELKON}/${target}/rep_${rep}/pheno___${cur_fold}_${n_folds}_${inner_data}"
	
	    if [[ ! -f ${pheno_file_path}0 || ! -f ${pheno_file_path}1 ]]; then
		total_lines=$(wc -l < "${pheno_file_path}")	
		bigger_lines=$(( total_lines * $ratio /100 ))   #number of lines in the bigger train data
		smaller_lines=$(( total_lines - bigger_lines ))   #number of lines in the smaller train data
		head -n $bigger_lines "$pheno_file_path" > ${pheno_file_path}0
		head -n 1 "$pheno_file_path" > ${pheno_file_path}1
		tail -n $smaller_lines "$pheno_file_path" >> ${pheno_file_path}1
	    fi
		bash prepare_cv_datasets_split_data.sh --data=${inner_data} --discovery=${discovery} --target=${target} \
	        --cv="${cur_fold}_${n_folds}" --rep=${rep} --imp=${imp} ${hapmap_param} &		
    done 
    	pheno_file_path="${PRS_DATASETS_ELKON}/${target}/rep_${rep}/pheno___${n_folds}_${outer_data}"
	echo ${pheno_file_path}0
	if [[ ! -f ${pheno_file_path}0 || ! -f ${pheno_file_path}1 ]]; then
		total_lines=$(wc -l < "${pheno_file_path}")
		bigger_lines=$(( total_lines * $ratio /100 ))   #number of lines in the bigger train data
		smaller_lines=$(( total_lines - bigger_lines ))   #number of lines in the smaller train data
		head -n $bigger_lines "$pheno_file_path" > ${pheno_file_path}0
		head -n 1 "$pheno_file_path" > ${pheno_file_path}1		#print the header
		tail -n $smaller_lines "$pheno_file_path" >> ${pheno_file_path}1
	fi
	bash prepare_cv_datasets_split_data.sh --data=${outer_data} --discovery=${discovery} --target=${target} \
		                --cv="${n_folds}" --rep=${rep} --imp=${imp} ${hapmap_param} &
done


#example:
# bash split_train_data.sh --discovery=mai_bcac_onco_eur-5pcs --target=mai_cimba_eur_brca1_icogs --imp=impX_gen --gwas_pop=EUR+EUR --pheno="" --n_repetitions=1 --n_folds=0 
