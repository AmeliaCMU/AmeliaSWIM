#!/bin/bash

# Define an array of tuples, each containing 2 strings
list=(
    "kbos jan"
    "kdca apr"
    "kewr mar"    
    "kjfk apr"
    "klax may"
    "kmdw jun"
    "kmsy jul"
    "ksea aug"
    "ksfo sep"    
    "panc nov"    
)

# Iterate through each tuple
for element in "${list[@]}"; do
    # Split the element into two strings
    string1="${element%% *}"
    string2="${element#* }"
    echo "Pair $((i+1)): $string1, $string2"

    sbatch scripts/run_pair.sbatch "$string1" "$string2"
done