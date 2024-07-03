#!/bin/bash

#SBATCH -e /scratch/mmb/mromagosa/AFCluster/%j.err
#SBATCH -o /scratch/mmb/mromagosa/AFCluster/%j.out
#SBATCH --job-name 1DEG_5
#SBATCH --time=96:00:00
#SBATCH --gres=gpu:1
#SBATCH -c 8
#SBATCH --partition=mmb_gpu_2080
#SBATCH --gres gpu:rtx2080:1
###SBATCH --tres-bind=gres/gpu:verbose,closest

echo "Start at $(date)"



python RunAF2multi.py /scratch/mmb/mromagosa/AFCluster/msas1DEG/EX_{101..150}.a3m --model_num 1 --recycles 3 --output_dir out1DEG --af2_dir /apps/alpha_fold



echo "End at $(date)"

