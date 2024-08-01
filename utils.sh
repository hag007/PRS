# $1 = cluster ; $2 = seperator
# example: ("1;2;3") -> ("1" "2" "3")
#sep_to_array() {
#	IFS=${2} read -ra dis <<< "${1}"
#	echo ${dis[@]}
#}

split_to_array() {
    input="$1"
    separator="$2"
    temp_IFS=$IFS
    IFS="$separator" read -ra arr <<< "$input"
    res="${arr[@]}"
    IFS=${temp_IFS}
    echo $res
    
}

merge_array() {
    sep=$1
    shift
    input=("$@")
    temp_IFS=$IFS
    IFS=$sep
    res="${input[*]}"
    IFS=${temp_IFS}
    echo "$res"
}

