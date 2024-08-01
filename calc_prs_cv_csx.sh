#!/bin/bash

source constants_.sh
source utils.sh
source parallel.sh

source parse_args.sh "$@"
source init_args_cv.sh

prs_prefix="prs.cv.csx_${pop}_${pheno}"
ds_prefix="ds_${pop}_${pheno}"


path_to_reference="$ELKON_SCRATCH/prs_csx_1kg_ref"
if [[ -z $discovery_pops ]]; then echo "discovery_pops param is missing (e.g., EUR+EAS)"; exit 0; fi

# Default prs csx values:
if [[ -z $param_phi ]]; then phi_param=""; else phi_param="--param_phi=$param_phi"; fi                                  # If phi is not specified, it will be learnt from the data using a fully Bayesian approach
if [[ -z $mcmc_iterations ]]; then mcmc_iterations_param=""; else mcmc_iterations_param="--n_iter=$mcmc_iterations"; fi # default value will be assigned
if [[ -z $mcmc_burnin ]]; then mcmc_burnin_param=""; else mcmc_burnin_param="--n_burnin=$mcmc_burnin"; fi               # defult value will be assigned
if [[ -z $mcmc_thinning_factor ]]; then mcmc_thinning_factor=5; fi
if [[ -z $meta_flag ]]; then meta_flag="F"; fi # default only one population in tatget data
if [[ -z $seed ]]; then seed=1; fi
a_vals=(${a_arr//,/ })
b_vals=(${b_arr//,/ })
if [[ -z "${a_arr[@]}" && -z "${b_arr[@]}" ]]; then
    a_vals=(1 0.5) #  0.5 1.5 1
    b_vals=(0.5 0.5) #  0.5 0.5 1
    echo "default hps"
fi

for d in ${discoveries[@]}; do
    awk '{ if (NR==1){coef=$11} else {coef=exp($11)} print $1" "$4" "$5" "coef" "$7}' $PRS_GWASS/${gwas}/"gwas.QC.Transformed" > $PRS_GWASS/${gwas}/"gwas.QC.csx_format.tsv"
    gwas_files_path+="$PRS_GWASS/$d/gwas.QC.csx_format.tsv,"

    # TBD optional: count how many individuals in each gwas
    # for now: use default 100k
    n="100000"
    gwas_sample_size+="$n,"
    num_of_gwass=$((num_of_gwass+1))

done
gwas_files_path=${gwas_files_path%,}
gwas_sample_size="${gwas_sample_size%,}"

# Check if each option in PARAM_A has a corresponding option in PARAM_B
if [[ "${#a_vals[@]}" -ne "${#b_vals[@]}" ]]; then
    echo "Error: the number of hps a and b is not equal"
    exit 1
fi

for i in ${!a_vals[@]}; do
    param_a="${a_vals[i]}"
    param_b="${b_vals[i]}"
    cur_hp="${param_a}-${param_b}"
    echo "**** current hps are a=${param_a} , b=${param_b} ****"

    if [[ ${stage} -le 1 ]]; then
        cd $PRS_TOOLS/PRScsx/
        for chr in {1..22}; do
            if [[ ! -f $output_dir/out_EUR_pst_eff_a${param_a}_b${param_b}_phiauto_chr$chr.txt ]]; then
                output_dir=${prs_path}prs_csx/${prs_prefix}${test_suffix}.${cur_hp}.weights
                mkdir -p $output_dir

                cmd='python PRScsx.py \
                    --ref_dir='$path_to_reference' \
                    --bim_prefix='${imp_train_path}${ds_prefix}${train_suffix}' \
                    --sst_file='$gwas_files_path' \
                    --a='$param_a' \
                    --b='$param_b' \
                    --n_gwas='$gwas_sample_size' \
                    --pop='$(merge_array "," ${discovery_pops[@]})' \
                    --chrom='$chr' \
                    --meta='$meta_flag' \
                    --seed='$seed' \
                    '$phi_param' '$n_iter_param'  '$n_burnin_param' \
                    --thin='$mcmc_thinning_factor' \
                    --out_dir='$output_dir' \
                    --out_name=out'

                processes+=("$cmd")
            else
                echo "There's a weight file for chromosome $chr. Skipping.."
            fi
        done
        wait_for_threads

        # concatenate all chromosomes' weights into one file
        for pop in ${discovery_pops_arr[@]}; do
            rm ${output_dir}/out_all_${pop} || true
            for chr in {1.22}; do
                cat $output_dir/out_${pop}_pst_eff_a${param_a}_b${param_b}_phiauto_chr${chr}.txt \
                > $output_dir/out_all_${pop}
            done
        done

        cd $PRS_CODEBASE
    fi

    # Calculate risk scores for each population separately, and then regress the scores into a single PRS
    if [[ ${stage} -le 2 ]]; then
        profile_output=${prs_path}${prs_prefix}${test_suffix}
        mkdir -p ${profile_output}.${cur_hp}/

        # Parse the population identifiers (EUR, EAS etc.)
        unique_pops=($(echo "${discovery_pops_arr[@]}" | tr ' ' '\n' | sort -u))
        hps_str=""
        prs_paths=""
        for origin in ${unique_pops[@]}; do
            ls -tr ${output_dir}/out_${origin}* | xargs -n 100 cat >${output_dir}/out_all_${origin}

            plink --bfile ${imp_test_path}${ds_prefix}${test_suffix} \
                --score ${output_dir}/out_all_${origin} 2 4 6 \
                --exclude ${imp_test_path}ds.dupvar \
                --memory 20000 \
                --threads 40 \
                --out ${profile_output}.${cur_hp}.${origin}

            hps_str+="${cur_hps}.${origin}+"
            prs_paths+="${profile_output},"
        done

        hps_str=${hps_str%,}
        prs_paths=${prs_paths%,}
        pheno_file_path=${target_path}pheno__${test_suffix}

#        # Regress the per-population risk scores to create a single one (that is, a single profile file).
#        if [[ ${#unique_pop[@]} -gt 1 ]]; then
#            python regress_multi_scores.py --prs_paths_lst=${prs_paths} --best_hps=${hps_str} --pheno_file_path=${pheno_file_path} --method="csx" --output_path=${profile_output} --prefix="" --reg_type="linear"
#
#            # Move the profile file to the place where calc_metrics will look for
#            mv ${output_path}.${hps_str}.multi_profile ${output_path}.${cur_hp}.profile
#        else
#            mv ${profile_output}.${cur_hp}.${origin}.profile ${output_path}.${cur_hp}.profile
#            rm ${profile_output}.${cur_hp}.${origin}.profile
#        fi
    fi

    # Evaluate model performances
#    if [[ ${stage} -le 3 ]]; then
#        Rscript calc_metrics_cv_csx.R --discovery=${discovery} --target=${target} --imp=${imp} \
#            --suffix=${test_suffix} --rep=${rep} --analysis_type="cv"
#    fi

done
