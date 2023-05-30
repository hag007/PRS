# Parse input

source init_args_prs.sh

if [[ -z ${cv} ]]; then echo "please provide sample index value" && exit 1; fi
if [[ -z ${smpl} ]]; then echo "please provide sample id value" && exit 1; fi

if [[ ! -z "${cv}" ]]; then
        if [[ ${cv} == *_* ]]; then
            echo "create sample"
            train_suffix="_${cv}_sample" # train_sample
            test_suffix="_${cv}"
        fi
fi
if [[ "${train_suffix}" == "" || -z "${train_suffix}" ]]; then
    train_suffix=${suffix}
    test_suffix=${suffix}
fi
suffix=${test_suffix}

target_train_path=${PRS_DATASETS}/${target_train}"/sample_${smpl}/"
target_test_path=${target_train_path}
target_path=${target_train_path}

imp_train_path=${PRS_DATASETS}/${target_train}"/sample_${smpl}/${imp}/"
imp_test_path=${imp_train_path}
imp_path=${imp_train_path}
base_imp_path=${PRS_DATASETS}/${target_train}/${imp}"/"


prs_path=${prs_path}"sample_${smpl}/"


mkdir -p ${imp_path} || echo ""
mkdir -p ${prs_path} || echo ""
