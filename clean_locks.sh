#!/bin/sh
set -e 

locks_folder="/specific/elkon/hagailevi/PRS/locks"
locks="$(ls -1 ${locks_folder} )"
# locks=$'echo+start+3+&&+sleep+10+&&+echo+end+3.lock\necho+start+4+&&+sleep+10+&&+echo+end+4.lock'
processes_not_exist_message="No such process"
echo "$locks"

SAVEIFS=$IFS   # Save current IFS
IFS=$'\n'      # Change IFS to new line
locks=($locks) # split to array $names
IFS=$SAVEIFS   # Restore IFS

for lk in ${locks[@]}; do
# while IFS= read -r lk; do 
    echo "... $lk ..."
    lk_content=$(cat ${locks_folder}/$lk)
    server=$(echo $lk_content | cut -d " " -f 1)
    process=$(echo $lk_content | cut -d " " -f 2)
    echo "ssh ${server}.cs.tau.ac.il"
    kill_0_message=$(ssh ${server}.cs.tau.ac.il "kill -0 ${process}; exit")
    echo "$kill_0_message"
    if [[ $kill_0_message =~ .*$processes_not_exist_message.* ]]; then
        echo "process $lk does not exists. deleting lock..."
        rm ${locks_folder}/$lk
    fi

echo $lk
done # <<< "$locks"
echo "done!"
