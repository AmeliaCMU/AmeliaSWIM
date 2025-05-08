#!/bin/bash

#SBATCH -p RM-small
#SBATCH -t 1:00:00
#SBATCH --cpus-per-task=32
#SBATCH -n 1
#SBATCH -o /ocean/projects/cis220039p/jaypat/AMELIA_NEURIPS/AmeliaSWIM/slurm_logs/%j.out

airport=$1
data=$2

set -x
. /jet/home/jaypat/.bashrc

conda activate swim

cd /ocean/projects/cis220039p/jaypat/AMELIA_NEURIPS/AmeliaSWIM

srun python process.py data=${data} airports=${airport}
