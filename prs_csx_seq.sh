# set env
discoveries=("bcac_onco_eur-5pcs" "bcac_onco_eas1-5pcs")
gwas_pops=("EAS" "EUR")

pheno="pheno"
target="bcac_onco_eas2_seq"
imp="impX"

# cross validation parameters
n_folds=3
n_repetitions=4
base_rep=102

# sorting the discoveries according to lex order

#map the two arrays so i can sort gwass and keep the matching to pop array.
declare -A map
for ((j=0; j<${#discoveries[@]}; j++)); do
     map[${discoveries[j]}]=${gwas_pops[j]}
done


#sort only according to discovery
sorted_keys=($(printf '%s\n' "${!map[@]}" | sort))

discoveries=()
gwas_pops=()
for key in "${sorted_keys[@]}"; do
    discoveries+=(${key})
    gwas_pops+=("${map[$key]}")
done
unset map


discoveries_str=$(IFS=+; echo "${discoveries[*]}") #"g1+g2+..."

target_path=$PRS_DATASETS_ELKON/${target}/
imp_path=$PRS_DATASETS_ELKON/${target}/${imp}/
prs_path=$PRS_PRSS/${discoveries_str}_${target}/${imp}/
mkdir -p $prs_path || true
pheno_path=$PRS_DATASETS_ELKON/${target}/


for d in ${discoveries[@]}; do 
echo $d
done

# Reformatting the gwass to fit the csx pipeline
gwas_files_path0=()
num_of_gwass=0

for gwas in ${discoveries[@]}; do
awk '{ if (NR==1){coef=$11} else {coef=exp($11)} print $1, $4, $5, coef, $7}' $PRS_GWASS/${gwas}/"gwas.QC.Transformed" > $PRS_GWASS/${gwas}/"gwas.QC.csx_format.tsv"

# set SUM_STATS_FILE
gwas_files_path0+=("${PRS_GWASS}/${gwas}/gwas.QC.csx_format.tsv")
((num_of_gwass+=1))

done

gwas_files_path=$(IFS=,; echo "${gwas_files_path0[*]}")

gwas_sample_size=""
for ((i = 0; i < num_of_gwass; i++)); do
        n=100000
        gwas_sample_size+=",$n"
done
gwas_sample_size="${gwas_sample_size#,}"

micromamba activate

# PRS CSx parameters
path_to_reference="$ELKON_SCRATCH/prs_csx_1kg_ref/"
# param_phi=null # If phi is not specified, it will be learnt from the data using a fully Bayesian approach
population=$(IFS=,; echo "${gwas_pops[*]}")
# mcmc_iterations=null   # defult value will be assigned
# mcmc_burnin=null    # defult value will be assigned


if [[ -z $param_phi ]]; then phi_param=""; else phi_param="--param_phi=$param_phi"; fi # If phi is not specified, it will be learnt from the data using a fully Bayesian approach
if [[ -z $mcmc_iterations ]]; then mcmc_iterations_param=""; else mcmc_iterations_param="--n_iter=$mcmc_iterations"; fi   # defult value will be assigned
if [[ -z $mcmc_burnin ]]; then mcmc_burnin_param=""; else mcmc_burnin_param="--n_burnin=$mcmc_burnin"; fi   # defult value will be assigned
if [[ -z $mcmc_thinning_factor ]]; then mcmc_thinning_factor=5; fi
if [[ -z $meta_flag ]]; then meta_flag="F"; fi   # default only one population in tatget data
if [[ -z $seed ]]; then seed=1; fi
if [[ -z $chrom ]]; then chrom_param=""; else chrom_param="--chrom=$chrom"; fi     # will run through all 22 chromosomes


# define hyper parameters

a_vals=(0.5 1 1.5 1)
b_vals=(0.5 0.5 0.5 1)

if [[ -z "${a_arr[@]}" && -z "${b_arr[@]}" ]]; then a_vals=("1"); b_vals=("0.5"); echo "default hps"; fi

if [ ${#a_vals[@]} -ne ${#b_vals[@]} ]; then
    echo " a, b Arrays must have the same length"
    exit 1
fi
mcmc_thinning_factor=5


# body of cross validation
MAI_HOME='/home/elkon2/maibendayan/'
pheno_prefix=""
if [[ $pheno != "pheno" ]]; then pheno_prefix="_$pheno"; fi

prs_prefix="prs.cv.csx_${pop}${pheno_prefix}"
ds_prefix="ds_${pop}_${pheno_prefix}"
    
for i in $(seq 1 $n_repetitions); do
    # define pathes
    rep="${base_rep}_$i"
    
    cv_target_path=${PRS_DATASETS_ELKON}/${target}"rep_${rep}/"

    imp_path=${PRS_DATASETS_ELKON}/${target}"/rep_${rep}/${imp}/"
    base_imp_path="${PRS_DATASETS_ELKON}/${target}/${imp}/"
    mkdir -p ${imp_path} || echo ""
    
    cv_prs_path="${prs_path}rep_${rep}/"
    mkdir -p ${cv_prs_path} || echo ""
    
    
    for j in $(seq 1 $n_folds); do
        cv="${j}_${n_folds}"
        test_suffix=_${cv}_validation
        train_suffix=_${cv}_train
        
        # perform cross-validation
        for hps in "${!a_vals[@]}"; do
            param_a=${a_vals[hps]}
            param_b=${b_vals[hps]}
            cur_hp="${param_a}-${param_b}"
            echo "**** current hps are a=${param_a} , b=${param_b} ****"
            
            ## call for csx!!
            
            cd $MAI_HOME/tools/PRScsx/
            output_dir=${cv_prs_path}prs_csx/${prs_prefix}${test_suffix}.${cur_hp}.weights
            mkdir -p ${output_dir} || true

            #running prs_csx to receive weights per chromosome
            { python PRScsx.py \
                 --ref_dir=$path_to_reference \
                 --bim_prefix=${imp_path}${ds_prefix}${train_suffix} \
                 --sst_file="${gwas_files_path}" \
                 --a=${param_a} --b=${param_b} \
                 --n_gwas="${gwas_sample_size}" --pop="${population}" \
                 --meta=$meta_flag --seed=$seed \
                 $phi_param $chrom_param $n_iter_param $n_burnin_param --thin=$mcmc_thinning_factor \
                 --out_dir=${output_dir} --out_name=out


           cd $PRS_CODEBASE
        
            # concatinate all chromosomes' weights into one file  #####TBD change it####
            pop=$(echo "$POPULATION"| cut -d',' -f1)
            cat ${output_dir}/out_${pop}_"pst_eff_a${param_a}_b${param_b}_phiauto_chr"*".txt" \
                > ${output_dir}/out_all
            
            # calculate scores
            plink --bfile ${imp_path}${ds_prefix}${test_suffix}  \
                        --score ${output_dir}/out_all 2 4 6 \
                        --exclude ${imp_test_path}ds.dupvar \
                        --memory 20000 \
                        --threads 40 \
                        --out ${cv_prs_path}${prs_prefix}${test_suffix}.${cur_hp}

            
            # find best fit and r2 to evalute the model - outputs statistics file
            Rscript calc_metrics_cv_csx.R --discovery=${discoveries_str} --target=${target} --imp=${imp} \
                                           --suffix=${test_suffix} --rep=${rep} --analysis_type="cv" \
                                           --grid_ids=${cur_hp};
          } 
        done
    done
    
 # test against a hold-out set
 train_suffix=_${n_folds}_both
 test_suffix=_${n_folds}_test
    
 for hps in "${!a_vals[@]}"; do
         param_a=${a_vals[hps]}
         param_b=${b_vals[hps]}
         cur_hp="${param_a}-${param_b}"
         echo "**** current hps are a=${param_a} , b=${param_b} ****"
            
         ## call for csx!!
         cd $MAI_HOME/tools/PRScsx/
         output_dir=${cv_prs_path}prs_scx/${prs_prefix}${test_suffix}.${cur_hp}.weights
         mkdir -p ${output_dir} || true
            
         #running prs_csx to receive weights per chromosome
         { python PRScsx.py \
              --ref_dir=$path_to_reference \
              --bim_prefix=${imp_path}${ds_prefix}${train_suffix} \
              --sst_file="${gwas_files_path}" \
              --a=${param_a} --b=${param_b} \
              --n_gwas="${gwas_sample_size}" --pop="${population}" \
              --meta=$meta_flag --seed=$seed \
              $phi_param $chrom_param $n_iter_param $n_burnin_param --thin=$mcmc_thinning_factor \
              --out_dir=${output_dir} --out_name=out
            
        cd $PRS_CODEBASE
        
         # concatinate all chromosomes' weights into one file  #####TBD change it####
         pop=$(echo "$POPULATION"| cut -d',' -f1)
         cat ${output_dir}/out_${pop}_"pst_eff_a${param_a}_b${param_b}_phiauto_chr"*".txt" \
             > ${output_dir}/out_all
            
         # calculate scores
         plink --bfile ${imp_path}${ds_prefix}${test_suffix}  \
                     --score ${output_dir}/out_all 2 4 6 \
                     --exclude ${imp_path}ds.dupvar \
                     --memory 20000 \
                     --threads 40 \
                     --out ${cv_prs_path}${prs_prefix}${train_suffix}.${cur_hp}

            
         # find best fit and r2 to evalute the model - outputs statistics file
         Rscript calc_metrics_cv_csx.R --discovery=${discoveries_str} --target=${target} --imp=${imp} \
                                        --suffix=${test_suffix} --rep=${rep} --analysis_type="cv" \
                                        --grid_ids=${cur_hp};
        } 
     done
    
done
    

