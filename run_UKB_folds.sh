
# discoveries="D2_sysp_evangelou_2018,D2_dias_evangelou_2018,D2_asth_zhu_2019,D2_chol_willer_2013,D2_ldlp_willer_2013,D2_t2di_mahajan_2018,D2_gerx_an_2019,D2_madd_howard_2019" # "D2_sysp_evangelou_2018" D2_hdlp_willer_2013
# discoveries="UKB_ht_eur,UKB_chol_eur,UKB_hfvr_eur,UKB_hyty_eur,UKB_madd_eur,UKB_osar_eur,UKB_t2d_eur,UKB_utfi_eur,UKB_gerx_eur,UKB_angna_eur,UKB_ast_eur,UKB_ctrt_eur"
discoveries=${discoveries//,/ }
# targets="ukbb_afr"
targets=${targets//,/ }
# imps="original" # "impute2_1kg_gbr" # ,impute2_1kg_afr,impute2_1kg_gbr" # "impute2_1kg_eur,impute2_1kg_afr,impute2_1kg_gbr,impute2_1kg_sas" # "impute2_1kg_ceu2"
imps=${imps//,/ }
method="ls"
base_rep=105
folds=5
complete_missing=true


declare -A gwas_to_pheno=(['D2_hght_yengo_2018']='height' ['D2_ldlp_willer_2013']='chol' ['D2_hdlp_willer_2013']='chol' ['D2_chol_willer_2013']='chol'  ['D2_sysp_evangelou_2018']='ht' ['D2_dias_evangelou_2018']='ht' ['D2_asth_zhu_2019']='ast' ['D2_t2di_mahajan_2018']='t2d' ['D2_madd_howard_2019']='madd' ['D2_gerx_an_2019']='gerx') ['D2_hdlp_willer_2013']='chol' ['D_t2d_mahajan_2018']='t2d' \
['UKB_ht_eur']='ht' ['UKB_chol_eur']='chol' ['UKB_hfvr_eur']='hfvr' ['UKB_hyty_eur']='hyty'  ['UKB_madd_eur']='madd' ['UKB_osar_eur']='osar' ['UKB_t2d_eur']='t2d' ['UKB_utfi_eur']='utfi' ['UKB_gerx_eur']='gerx' ['UKB_angna_eur']='angna' ['UKB_ast_eur']='ast' ['UKB_ctrt_eur']='ctrt')

counter=0
min_n_profiles=60
min_n_profiles_res3=10

for discovery in ${discoveries[@]}; do
    pheno=${gwas_to_pheno[${discovery}]}
    for target in ${targets[@]}; do
        for imp in ${imps[@]}; do
            for cur_rep in {1..6}; do
                for fold in {1..5}; do
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
                        if [[ ${complete_missing} = true ]]; then
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
