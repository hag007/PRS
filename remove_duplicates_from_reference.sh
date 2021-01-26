#!/bin/sh

source constants.sh
source chr_args.sh

population_source=$1
population_destination=$2

res=$(parse_chrs $3)
eval "declare -a chrs=${res#*=}";
echo "test"
echo ${chrs}
for a in ${chrs[@]}; do
    echo $a
    cat ${reference_path}1000G_${population_source}/chr${a}.vcf | awk '{(!a[$1, $2]++ && !b[$3]++)}' > ${reference_path}1000G_${population_destination}/chr${a}.vcf
    echo 'done chr'${a}
done

# # for a in ( ${1} ); do
# a=$1
#     cat chr${a}.vcf | awk '/^#/{print}; !/^#/{if (!uniq[$3]++ && !seen[$2]++) print}' > ../1000G_EAS/chr${a}.vcf
#     echo 'done chr'${a}
# 
# # done
# 
#   
