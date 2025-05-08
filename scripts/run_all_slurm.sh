#!/bin/bash
set -e

# Array of 2-field “tuples”:  "<icao> <period>", all lowercase
list=(
  "katl week"
  "kbdl week"
  "kbfi week"
  "kbwi week"
  "kcle week"
  "kclt week"
  "kcvg week"
  "kden week"
  "kdfw week"
  "kdtw week"
  "kfll week"
  "khou week"
  "khwd week"
  "kiad week"
  "kiah week"
  "klas week"
  "klga week"
  "kmci week"
  "kmco week"
  "kmem week"
  "kmia week"
  "kmke week"
  "kmsp week"
  "koak week"
  "kord week"
  "korl week"
  "kpdx week"
  "kphl week"
  "kphx week"
  "kpit week"
  "kpvd week"
  "kpwk week"
  "ksan week"
  "ksdf week"
  "kslc week"
  "ksna week"
  "kstl week"
  "phnl week"
)

# Iterate through each tuple
for element in "${list[@]}"; do
    # Split the element into two strings
    string1="${element%% *}"
    string2="${element#* }"
    echo "Pair $((i+1)): $string1, $string2"

    sbatch scripts/run_pair.sbatch "$string1" "$string2"
done