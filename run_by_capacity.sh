#!/bin/bash
set -e
source parse_args.sh "$@"

manager_base_folder='/specific/elkon/hagailevi/PRS'
locks_folder=${manager_base_folder}"/locks"
logs_folder=${manager_base_folder}"/logs"
completed_jobs_folder=${manager_base_folder}"/completed_jobs"
input_files_folder=${manager_base_folder}"/input_files"
cmds_folder=${manager_base_folder}"/cmds"

if [[ -z $cmd ]]; then echo "Please choose a command file (arg name: --cmd)"; exit 1; fi
if [[ -z $input ]]; then echo "Please choose an input file (arg_name: --input)"; exit 1; fi
if [[ -z $p_per_server ]]; then p_per_server=2; fi
if [[ -z $sleeping_time ]]; then  sleeping_time=30; fi

function mywait {
       while [ -e /proc/$1 ]; do
           d=$(date '+%T')
           echo -e "\e[1A\e[KWaiting for $1 (Recent check: $d)" 
           sleep 1               
       done
}

cmd_file='('$(cat ${cmds_folder}/${cmd}.txt)' & echo $!>&3 | tr "\n" " ") 3>pid  && echo "start running pid $(<pid)"'
input_file=${input_files_folder}"/${input}.txt"

n_completed=0
n_jobs=1
iterations_to_message=0
while [[ n_completed -lt n_jobs ]]; do
    readarray -t lines < <(cat $input_file | awk 'FS=";" {gsub(/^[ \t]+|[ \t]+$/, ""); gsub(/[ \t]+;|;[ \t]+/, ";"); print}')
    declare -A file_params=()
    declare -a running_params=()
    declare -a completed_params=()
    declare -a pending_params=()
    n_completed=0
    n_jobs=0
    for line in "${lines[@]}"; do

        for arg in $(IFS=';'; echo $line); do 

            # echo 1 ${arg}  
            key=${arg%%=*}
            value=${arg#*=}
            # echo $key 
            # echo $value
            file_params["$key"]=$value  ## Or simply ary[${line%%=*}]=${line#*=}
        done
    
        n_jobs=$((n_jobs+1))
        # echo 2 ${line}
        cmd_formatted=${cmd_file}
        params_string=""
        for key in "${!file_params[@]}"; do
            params_string=${params_string}${key}"="${file_params["$key"]}"_"
            cmd_formatted=${cmd_formatted//"\${"$key"}"/${file_params["$key"]}}
        done
        params_string=${params_string%?}
        # echo ${params_string}
        lock_name=${cmd}"#"${params_string} # $(echo ${cmd_formatted}  | /usr/bin/md5sum | cut -f1 -d" ")
        current_p=$(ls ${locks_folder} -1 | xargs -I '{}' cat ${locks_folder}/'{}' | grep $HOSTNAME | wc -l)
        # echo currently $current_p jobs are running out of capacity of $p_per_server 
        # echo "about to start running the job:   \"${cmd_formatted}\""
        if [[ -f ${completed_jobs_folder}/${lock_name}".completed" ]]; then 
            completed_params+=($line)
            n_completed=$((n_completed+1))
        elif [[ -f ${locks_folder}/${lock_name}".lock" ]]; then 
            running_params+=($line)
        elif [[ $current_p -ge $p_per_server  ]]; then
            pending_params+=($line) 
        else
            echo "Start new eval ${cmd_formatted}"
             ( ( (eval ${cmd_formatted}) && pid=$(<pid) && echo "$HOSTNAME $pid"> ${locks_folder}/${lock_name}".lock" && echo ${locks_folder}/${lock_name}".lock"  && echo "pid $pid has been started" && status_code=$(mywait $pid) && echo "done $pid with status code $status_code" && rm ${locks_folder}/${lock_name}".lock" && echo $HOSTNAME $cmd_formatted $status_code >> ${completed_jobs_folder}/${lock_name}".completed")  | tee "${logs_folder}/${HOSTNAME}_${lock_name}.log" ) &
            while [[ ! -f  ${locks_folder}/${lock_name}".lock" ]] &&  [[ ! -f  ${completed_jobs_folder}/${lock_name}".completed" ]]; do
                echo -e "\e[1A\e[KWaiting for process to start..."
                sleep 5
            done
            echo "pid $(<pid) started." 
        fi
    done
    echo "Currently $current_p jobs are running out of capacity of $p_per_server"
    echo "$n_completed jobs completed out of $n_jobs"
    # echo "completed jobs status:"
    # ls ${completed_jobs_folder} -1 | xargs -I {} cat ${completed_jobs_folder}/{} | sort | uniq -c
    echo "Running jobs status:"
    ls ${locks_folder} -1 | xargs -I {} cat ${locks_folder}/{} | sort | uniq -c
    sleep $sleeping_time
    iterations_to_message=$(($iterations_to_message+1))
    d=$(date '+%T')
    echo "Status of job executed with specific parameters for server $HOSTNAME: (checked in $d)"
    echo "Completed: ${completed_params[@]}"
    echo "Running: ${running_params[@]}"
    echo "Pending: ${pending_params[@]}"
done

# cmd_format='plink2 --bgen ukb22828_c${a}_b0_v3.bgen ref-first --sample ukb22828_c${a}_b0_v3_s487281.sample --extract /specific/elkon/hagailevi/PRS/GWASs/bca_313/313.snplist --make-bed --out ds313.${a} --memory 600000 --threads 8'

