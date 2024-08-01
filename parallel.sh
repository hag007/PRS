# To run parallel processes, set the following params in the caller scope (before calling `wait_for_threads`):
# 1. `processes`: list of strings representing commands you wish to execute.
# You can simply write rach command as string (e.g., cmd='...')
# and then put it in the `processes` array: `processes+=("$cmd")`
# 2. `threads` (optional): # of threads allocated to the pool (default is 1000)

##### LEGACY ######
# 1.1. if you have limited number of processes that you wish to run at once, set `threads=-1`
# 1.2. if you have a high number of processes, set `threads` to the number of processes you wish to be running in parallel.
# 1.2.1 In this case, you need to set the following lines in the caller scope:
# 1.2.1.1. Wrap the process execution in loops.
# 1.2.1.2. In each iteration, run a single process with `` at the end
# 1.2.1.3. After the loop, add the line `wait " ${pids[@]}"; echo "done!"`
###################
function wait_for_threads {
    if [[ -z $threads ]]; then echo "threads param was not provided. Set to 10000"; threads=1000; else echo "number of threads allocated: ${threads}"; fi
#    echo "$processes"
    for process in "${processes[@]}"; do
#            echo "$process"
        (eval "$process" || true) &
        pids+=($!)

        while [[ ${#pids[@]} -ge $threads ]]; do
            counter=-1
            for pid in "${pids[@]}"; do
                counter=$((counter + 1))
                if [[ $(kill -0 $pid 2>&1) ]]; then
                    echo "remove index $counter: ${pids[counter]}"
                    unset 'pids[counter]'
                fi
            done

            # The following block is for updating the length of pids array (arrays' length in bash do not update automatically after modifying it)
            declare -a new_pids=()
            for i in "${pids[@]}"; do
                new_pids+=($i)
            done
            pids=(${new_pids[@]})
            unset new_pids

            echo "# of elements in pids: ${#pids[@]}"
            sleep 5
        done
        echo "Check if new processes are in waiting"
    done
    wait "${pids[@]}"
    echo "done!"
}
