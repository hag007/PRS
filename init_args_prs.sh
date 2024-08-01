# Parse input

source constants_.sh
source utils.sh

if [[ -z ${discovery} ]]; then echo "discovery value is missing" && exit 1; fi

if [[ (-z ${target_train}  || -z ${target_test} ) && -z ${target} ]]; then echo "target values are missing" && exit 1; fi
if [[ -z ${target_train} ]]; then target_train=$target; fi
if [[ -z ${target_test} ]]; then target_test=$target; fi
target=$target_test


if [[ (-z ${imp_train}  || -z ${imp_test} ) && -z ${imp} ]]; then echo "imp values are missing" && exit 1; fi
if [[ -z ${imp_train} ]]; then imp_train=$imp; fi
if [[ -z ${imp_test} ]]; then imp_test=$imp; fi
imp=$imp_test

if [[ -z ${stage} ]]; then stage=1; fi
if [[ -z ${hp}  ]]; then hp=""; fi
if [[ -z ${pop}  ]]; then pop=""; fi
if [[ -z ${pheno}  ]]; then pheno=""; fi
if [[ -z ${continuous}  ]]; then continuous="false"; fi
if [[ ! -z ${pheno} ]]; then pheno_suffix=_${pheno}_; fi
if [[ -z ${ld} ]]; then ld="eur"; fi

sub=""

if [[ ! "${pheno}" == ""  ||  ! "${pop}" == "" ]]; then
	sub=_${pheno}_${pop}
fi

if [[ ! "${pheno}" == ""  ]]; then
        pheno=${pheno} # removed underscore prefix!
fi

if [[ ! "${pop}" == "" ]]; then
        pop=${pop} # removed underscore prefix!
fi

train_suffix=""
test_suffix=""
suffix=""

############ LEGACY ##################
## considering discovery=dis1;dis2;dis3:
#discoveries=($(split_to_array "${discovery}" '+'))
#gwas_files_path0=()
#num_of_gwass=0
#for gwas in "${discoveries[@]}"; do
#	gwas_files_path0+=("${PRS_GWASS}/${gwas}/gwas.QC.csx_format.tsv")
#	((num_of_gwass+=1))
#done
#
#gwas_files_path=($(merge_array ',' "${gwas_files_path0[@]}" ))
############ LEGACY ##################

# Sorting the discovery sets according to lexicographic order

# Map each discovery set to its pop value,
# assuming that the discovery set and the pop are located in the same position in their arrays
discoveries=($(split_to_array "${discovery}" '+'))
discovery_pops=($(split_to_array "${discovery_pop}" '+'))
declare -A map
for ((j=0; j<${#discoveries[@]}; j++)); do
     map[${discoveries[j]}]=${discovery_pops[j]}
done

# Extract and sort discovery names
sorted_keys=($(printf '%s\n' "${!map[@]}" | sort))


discoveries=()
discovery_pops=()

# Regenerate sorted `discoveries` and `discovery_pops`,
# sorted lexicographically according to the discovery names
for key in "${sorted_keys[@]}"; do
    discoveries+=(${key})
    discovery_pops+=("${map[$key]}")
done
unset map
discovery=($(merge_array '+' "${discoveries[@]}" ))
discovery_pop=($(merge_array '+' "${discovery_pops[@]}" ))

# discovery_path=${GWASs_path}${discovery}'/'
# target_train_path=${datasets_path}${target_train}'/'
# target_test_path=${datasets_path}${target_test}'/'
# target_path=${target_test_path}
discovery_path="$PRS_GWASS/${discovery}/"
target_train_path="$PRS_DATASETS_ELKON/${target_train}/"
target_test_path="$PRS_DATASETS_ELKON/${target_test}/"
target_path=$target_test_path
prs_path="$PRS_PRSS/${discovery}_${target}/${imp}/"

imp_train_path=${target_train_path}${imp_train}'/'
imp_test_path=${target_test_path}${imp_test}'/'
imp_path=${imp_test_path}

# prs_path=${PRSs_path}${discovery}_${target}"/${imp}/"
mkdir -p ${prs_path} || echo ""
