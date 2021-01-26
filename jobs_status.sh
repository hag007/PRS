#!/bin/sh
source colors.sh
locks_folder="/specific/elkon/hagailevi/PRS/locks"
completed_jobs_folder="/specific/elkon/hagailevi/PRS/completed_jobs"

printf "${YELLOW}\t\t\t\t****jobs summary****\n"
echo "${RED}locks: "
printf "\tstatus per file\n"
ls ${locks_folder} -1 | xargs -n 1 -I A bash -c 'printf "\t\t"; cat "'${locks_folder}'/'A'" | tr "\n" " "; printf "\t\tA\n";' | sort
printf "\tsummary\n"
ls ${locks_folder} -1 | xargs -I A cat "${locks_folder}/A" | sort | uniq -c | awk '{print "\t\t"$2"\t"$1 }' | sort
printf "\n\n"
echo "${GREEN}completed jobs: "
printf "\tstatus per file\n"
ls ${completed_jobs_folder} -1 | xargs -n 1 -I A bash -c 'printf "\t\t"; printf "\t\tA\n";' | sort | uniq -c 
# ls ${completed_jobs_folder} -1 | xargs -n 1 -I A bash -c 'printf "\t\t"; cat "'${completed_jobs_folder}'/'A'" | tr "\n" " "; printf "\t\tA\n";' | sort
printf "\tsummary\n"
ls ${completed_jobs_folder} -1 | xargs -I A cat "${completed_jobs_folder}/A" | sort | awk '{print "\t\t"$1 }' | sort | uniq -c
printf "\n\n"
echo ${NORMAL}
