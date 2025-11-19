#!/bin/bash
set -e

# Array of 2-field “tuples”:  "<icao> <period>", all lowercase
list=(
  "katl amelia42/amelia42_33"
  "kbdl amelia42/amelia42_18"
  "kbos amelia42/amelia42_22"
  "kbwi amelia42/amelia42_37"
  "kcle amelia42/amelia42_15"
  "kclt amelia42/amelia42_14"
  "kdca amelia42/amelia42_9"
  "kden amelia42/amelia42_25"
  "kdfw amelia42/amelia42_41"
  "kdtw amelia42/amelia42_13"
  "kewr amelia42/amelia42_36"
  "kfll amelia42/amelia42_2"
  "khou amelia42/amelia42_5"
  "kiad amelia42/amelia42_34"
  "kiah amelia42/amelia42_29"
  "kjfk amelia42/amelia42_16"
  "klas amelia42/amelia42_4"
  "klax amelia42/amelia42_7"
  "klga amelia42/amelia42_35"
  "kmci amelia42/amelia42_40"
  "kmco amelia42/amelia42_39"
  "kmdw amelia42/amelia42_24"
  "kmem amelia42/amelia42_23"
  "kmia amelia42/amelia42_19"
  "kmke amelia42/amelia42_6"
  "kmsp amelia42/amelia42_10"
  "kmsy amelia42/amelia42_31"
  "kord amelia42/amelia42_12"
  "kpdx amelia42/amelia42_8"
  "kphl amelia42/amelia42_30"
  "kphx amelia42/amelia42_28"
  "kpit amelia42/amelia42_21"
  "kpvd amelia42/amelia42_26"
  "ksan amelia42/amelia42_27"
  "ksdf amelia42/amelia42_32"
  "ksea amelia42/amelia42_17"
  "ksfo amelia42/amelia42_42"
  "kslc amelia42/amelia42_1"
  "ksna amelia42/amelia42_3"
  "kstl amelia42/amelia42_38"
  "panc amelia42/amelia42_20"
  "phnl amelia42/amelia42_11"
)

# Iterate through each tuple
for element in "${list[@]}"; do
    # Split the element into two strings
    string1="${element%% *}"
    string2="${element#* }"
    echo "Pair $((i+1)): $string1, $string2"

    sbatch scripts/run_pair.sbatch "$string1" "$string2"
done