#!/bin/bash
set -e
source parse_args.sh "$@"

manager_base_folder='/specific/elkon/hagailevi/PRS'
locks_folder=${manager_base_folder}"/locks"
logs_folder=${manager_base_folder}"/logs"
completed_jobs_folder=${manager_base_folder}"/completed_jobs"
input_files_folder=${manager_base_folder}"/input_files"
cmds_folder=${manager_base_folder}"/cmds"

if [[ -z $p_per_server ]]; then p_per_server=2; fi
if [[ -z $sleeping_time ]]; then  sleeping_time=30; fi

function mywait {
       while [ -e /proc/$1 ]; do
           echo "waiting for $1" 
           sleep 1               
       done
}

cmd='('$(cat ${cmds_folder}/${cmd_fn}.txt)' & echo $!>&3 | tr "\n" " ") 3>pid  && echo "start running pid $(<pid)"'
input_file=${input_files_folder}"/${input_fn}.txt"

n_completed=0
n_jobs=1
while [[ n_completed -lt n_jobs ]]; do
    readarray -t lines < "$input_file"
    declare -A file_params
    n_completed=0
    n_jobs=0
    for line in "${lines[@]}"; do
       if [[ ! -z  ${line// }  ]]; then
           # echo 1 ${line}  
           key=${line%%=*}
           value=${line#*=}
           # echo $key 
           # echo $value
           file_params["$key"]=$value  ## Or simply ary[${line%%=*}]=${line#*=}
    
       else
           n_jobs=$((n_jobs+1))
           # echo 2 ${line}
           cmd_formatted=$cmd
           params_string=""
           for key in "${!file_params[@]}"; do
               params_string=${params_string}${key}"="${file_params["$key"]}"_"
               cmd_formatted=${cmd_formatted//"\${"$key"}"/${file_params["$key"]}}
           done
           params_string=${params_string%?}
           # echo ${params_string}
           lock_name=${cmd_fn}"#"${params_string} # $(echo ${cmd_formatted}  | /usr/bin/md5sum | cut -f1 -d" ")
           current_p=$(ls ${locks_folder} -1 | xargs -I '{}' cat ${locks_folder}/'{}' | grep $HOSTNAME | wc -l)
           # echo currently $current_p jobs are running out of capacity of $p_per_server 
           # echo "about to start running the job:   \"${cmd_formatted}\""
           if [[ -f ${completed_jobs_folder}/${lock_name}".completed" ]]; then 
               echo "The job was completed"
               n_completed=$((n_completed+1))
           elif [[ -f ${locks_folder}/${lock_name}".lock" ]]; then 
               echo "The job is currently running"
           elif [[ $current_p -ge $p_per_server  ]]; then
               echo "too many jobs are running on this server ($HOSTNAME). rejecting the job"
           else
               echo "start new eval"
               ( ( (eval ${cmd_formatted}) && pid=$(<pid) && echo "$HOSTNAME $pid"> ${locks_folder}/${lock_name}".lock" && echo ${locks_folder}/${lock_name}".lock"  && echo "pid $pid has been started" && status_code=$(mywait $pid) && echo "done $pid with status code $status_code" && rm ${locks_folder}/${lock_name}".lock" && echo $HOSTNAME $cmd_formatted $status_code >> ${completed_jobs_folder}/${lock_name}".completed")  | tee "${logs_folder}/${HOSTNAME}_${lock_name}.log" ) &
               while [[ ! -f  ${locks_folder}/${lock_name}".lock" ]] &&  [[ ! -f  ${completed_jobs_folder}/${lock_name}".completed" ]]; do
                   echo "waiting for process to start..."
                   sleep 5
               done
               echo "pid $(<pid) started." 
           fi
       fi
    
    done
    echo "Currently $current_p jobs are running out of capacity of $p_per_server"
    echo "$n_completed jobs completed out of $n_jobs"
    # echo "completed jobs status:"
    # ls ${completed_jobs_folder} -1 | xargs -I {} cat ${completed_jobs_folder}/{} | sort | uniq -c
    echo "Running jobs status:"
    ls ${locks_folder} -1 | xargs -I {} cat ${locks_folder}/{} | sort | uniq -c
    sleep $sleeping_time
    
done

# cmd_format='plink2 --bgen ukb22828_c${a}_b0_v3.bgen ref-first --sample ukb22828_c${a}_b0_v3_s487281.sample --extract /specific/elkon/hagailevi/PRS/GWASs/bca_313/313.snplist --make-bed --out ds313.${a} --memory 600000 --threads 8'

