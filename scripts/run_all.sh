#!/bin/bash
set -e

list=(
  "katl week"
  "kbdl week"
  "kbfi week"
  "kbwi week"
  "kcle week"
)

# Iterate through each tuple
for element in "${list[@]}"; do
    # Split the element into two strings
    airport="${element%% *}"
    time="${element#* }"
    echo "Pair: $airport, $time"
    python process.py data=${data} airports=${airport}
done