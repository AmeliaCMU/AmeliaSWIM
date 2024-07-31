#!/bin/bash

# Define an array of tuples, each containing 2 strings
list=(
    "kpwk default"
    "kbfi default"    
    "khwd default"
    "kmem default"
    "kmke default"
    "koak default"
    "korl default"
)

# Iterate through each tuple
for element in "${list[@]}"; do
    # Split the element into two strings
    string1="${element%% *}"
    string2="${element#* }"
    echo "Pair $((i+1)): $string1, $string2"

    sbatch scripts/run_pair.sbatch "$string1" "$string2"
done