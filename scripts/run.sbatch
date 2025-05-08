#!/bin/bash

#SBATCH -p cpu_long
#SBATCH --account=nvr_av_end2endav
#SBATCH --cpus-per-task=32
#SBATCH -t 2:00:00
#SBATCH -J pretrain

airport=$1
data=$2

set -x
source /home/jpatrikar/.bashrc

conda init
conda activate base
conda activate swim
source /lustre/fsw/portfolios/nvr/users/jpatrikar/anaconda3/bin/activate swim



cd /lustre/fsw/portfolios/nvr/users/jpatrikar/AmeliaSWIM

srun python process.py airports=kcvg
