set +e
P=0

source /specific/elkon/hagailevi/PRS/codebase/parse_args.sh $@
source /specific/elkon/hagailevi/PRS/codebase/parse_chrs.sh
eval $(parse_chrs $chrs)


if [[ -z $max_threads ]]; then
    max_threads=70
fi

declare -a pid=()
for chr in ${chrs_range[@]}; do
namefile="${chr}.phased";
maxPos=$(tail -n 1 /specific/elkon/hagailevi/data-scratch/imputation/maps/1000G_ALL_impute2/1000GP_Phase3/genetic_map_chr${chr}_combined_b37.txt | awk '{print $1}')
nrChunk=$(expr ${maxPos} "/" 5000000)
nrChunk2=$(expr ${nrChunk} "+" 1)
start="0"
for chunk in $(seq 1 $nrChunk2); do

    endchr=$(expr $start "+" 5000000)
    startchr=$(expr $start "+" 1)
    echo "start a new process"
    # {
      ((P+=1))
      if [[ ! -f /specific/netapp5/gaga/gaga-pd/prs_data/datasets/dec/${target}/impute2/chr${chr}.${chunk}.legend ]]; then
         ( impute2 \
             -m /specific/elkon/hagailevi/data-scratch/imputation/maps/1000G_ALL_impute2/1000GP_Phase3/genetic_map_chr${chr}_combined_b37.txt \
             -h /specific/netapp5/gaga/gaga-pd/prs_data/raw/dec/gd_aj/Phase\ 2/Ref\ panel/${chr}.merged.snp_indel.hap.gz \
             -l /specific/netapp5/gaga/gaga-pd/prs_data/raw/dec/gd_aj/Phase\ 2/Ref\ panel/${chr}.merged.snp_indel.legend \
             -known_haps_g /specific/netapp5/gaga/gaga-pd/prs_data/datasets/dec/${target}/impute2/chr${chr}.phased.haps \
             -g /specific/netapp5/gaga/gaga-pd/prs_data/datasets/dec/${target}/original/raw/chr${chr}.gen \
             -int ${startchr} ${endchr} \
             -Ne 20000 \
             -allow_large_regions \
             -o /specific/netapp5/gaga/gaga-pd/prs_data/datasets/dec/${target}/impute2/chr${chr}.${chunk}.legend  || true )  & pids+=($!);  

      else
          echo "legend file for  ${chr} ${startchr} ${endchr} (chr${chr}.${chunk}.legend) already exists. skipping...";   
          P=$((P-1)) 
      fi 
     # } || {
     #     echo "skipping interval ${chrs} ${startchr} ${endchr} "
     # }

     start=${endchr}
     # if [ $P -gt $max_threads ]; then
         echo "waiting... (${#pids[@]}  == $max_threads ?)"
         while [[ ${#pids[@]}  -eq $max_threads ]]; do
             counter=-1
             for pid in ${pids[@]}; do 
                 # echo "$pid ${#pids[@]}"
                 counter=$((counter+1))
                 if  [[ $(kill -0 $pid  2>&1) ]]  ; then 
                     echo "remove index $counter: ${pids[counter]}"
                     unset 'pids[counter]'
                     P=$((P-1))
                 fi
             declare -a new_pids=()
             for i in ${pids[@]}; do
                 new_pids+=($i)
                 # echo ${new_pids[@]} 
             done
             pids=(${new_pids[@]})
             unset new_pids
             done
             echo "# of p: ${#pids[@]} (${pids[@]})"
             sleep 5
         done
             # P=0
         # wait "${pids[@]}"
         # declare -a pids=();
         # echo "done until ${chr}_${startchr}_${endchr}"
     # fi
echo "end while" 
done
done
wait "${pids[@]}"
echo "done!"

