#!/bin/bash
set -e

list=(
  "kpdx week"
  "kphl week"
  "kphx week"
  "kphx week"
  "kpit week"
  "kpvd week"
  "kpwk week"
  "ksan week"
)



# Iterate through each tuple
for element in "${list[@]}"; do
    # Split the element into two strings
    airport="${element%% *}"
    time="${element#* }"
    echo "Pair: $airport, $time"
    python process.py data=${time} airports=${airport}
done