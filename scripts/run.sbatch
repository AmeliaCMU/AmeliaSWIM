#!/bin/bash

#SBATCH -p RM-shared
#SBATCH -t 48:00:00
#SBATCH --cpus-per-task=32
#SBATCH -n 1
#SBATCH -o /ocean/projects/cis220039p/jaypat/boeing/boeing_swim_preprocess/outputs/%j.out

set -x
. /jet/home/jaypat/.bashrc

conda activate swim

cd /ocean/projects/cis220039p/jaypat/boeing/boeing_swim_preprocess

srun python process.py data=apr airports=kdca
