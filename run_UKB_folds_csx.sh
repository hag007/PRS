source constants_.sh
source parse_args.sh "$@"

discoveries=${discoveries//,/ }
targets=${targets//,/ }
imps=${imps//,/ }
method="csx"
base_rep=105
folds=5
complete_missing=true
n_folds=5
n_repetitions=6


counter=0
min_n_profiles=4
min_n_profiles_res3=4

for discovery in ${discoveries[@]}; do
    pheno=${gwas_to_pheno[${discovery}]}
    for target in ${targets[@]}; do
        for imp in ${imps[@]}; do
            for cur_rep in $(seq 1 $n_repetitions); do
                for fold in $(seq 1 $n_folds); do
                    res1=$(ls -1 /specific/netapp5/gaga/gaga-pd/prs_data/PRSs//${discovery}_${target}/${imp}/rep_${base_rep}_${cur_rep}/lasso/prs.cv.${method}___${fold}_${folds}_train.*.weights 2>/dev/null| wc -l );
                    res2=$(ls -1 /specific/netapp5/gaga/gaga-pd/prs_data/PRSs//${discovery}_${target}/${imp}/rep_${base_rep}_${cur_rep}/prs.cv.${method}_${pheno}__${fold}_${folds}_validation.*.profile 2>/dev/null| wc -l ) ;
                    res3=$(ls -1 /specific/netapp5/gaga/gaga-pd/prs_data/PRSs//${discovery}_${target}/${imp}/rep_${base_rep}_${cur_rep}/prs.cv.${method}_${pheno}__${fold}_${folds}_validation.or.summary.1-*.tsv 2>/dev/null | wc -l );
                    stage=-1
                    if [[ ${res3} -lt ${min_n_profiles_res3} ]]; then
                        stage=3
                    fi
                    if [[ ${res2} -lt ${min_n_profiles} ]]; then
                        stage=2
                    fi
                    if [[ ${res1} -lt ${min_n_profiles} ]]; then
                        stage=1
                    fi
                    echo "Discovery: ${discovery}, Target: ${target}, imp: ${imp}, rep: ${cur_rep}, fold: ${fold}: res validation: stage 1 - ${res1}, stage 2 - ${res2}, stage 3 - ${res3}"
                    if [[ ${stage} -ne -1 ]]; then
                        if [[ ${complete_missing} == true ]]; then
                            bash calc_prs_cv_${method}.sh --discovery ${discovery} --target ${target} --imp ${imp} --cv ${fold}_${folds} --rep ${base_rep}_${cur_rep} --pheno ${pheno} --stage ${stage};
                        fi
                        counter=$((${counter}+1))
                    fi
                done;
                res1=$(ls -1 /specific/netapp5/gaga/gaga-pd/prs_data/PRSs//${discovery}_${target}/${imp}/rep_${base_rep}_${cur_rep}/lasso/prs.cv.${method}___${folds}_both.*.weights 2>/dev/null| wc -l );
                res2=$(ls -1 /specific/netapp5/gaga/gaga-pd/prs_data/PRSs//${discovery}_${target}/${imp}/rep_${base_rep}_${cur_rep}/prs.cv.${method}_${pheno}__${folds}_test.*.profile 2>/dev/null | wc -l);
                res3=$(ls -1 /specific/netapp5/gaga/gaga-pd/prs_data/PRSs//${discovery}_${target}/${imp}/rep_${base_rep}_${cur_rep}/prs.cv.${method}_${pheno}__${folds}_test.or.summary.1-*.tsv 2>/dev/null | wc -l );
                echo "Discovery: ${discovery}, Target: ${target}, imp: ${imp}, rep: ${cur_rep}, fold: ${fold}: res test: stage 1 - ${res1}, stage 2 - ${res2}, stage 3 - ${res3}"
                stage=-1
                if [[ ${res3} -lt ${min_n_profiles_res3} ]]; then
                    stage=3
                fi
                if [[ ${res2} -lt ${min_n_profiles} ]]; then
                        stage=2
                fi
                if [[ ${res1} -lt ${min_n_profiles} ]]; then
                    stage=1
                fi
                if [[ ${stage} -ne -1 ]]; then
                    if [[ ${complete_missing} = true ]]; then
                        bash calc_prs_cv_${method}.sh --discovery ${discovery} --target ${target} --imp ${imp} --cv 5 --rep ${base_rep}_${cur_rep} --pheno ${pheno} --stage ${stage} ;
                    fi
                    counter=$((${counter}+1))
                fi
            done
        done
    done
done

echo "counter: ${counter}"
