#!/bin/bash

# For running in production mode on Perlmutter:
#SBATCH --image=docker:lsstsqre/centos:7-stack-lsst_distrib-w_2024_22

#SBATCH -q regular
#SBATCH --time=13:00:00

##SBATCH -q debug
##SBATCH --time=00:10:00

#SBATCH --constraint=cpu
#SBATCH -A m1727
#SBATCH -L scratch,cfs

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --array=0-1

working_dir=/pscratch/sd/d/descdm/roman-desc-sims/drp/step3
run_script=${working_dir}/run_command.sh

if [[ $SLURM_ARRAY_TASK_ID == 0 ]]; then
    cd ${working_dir}/034a
    srun shifter ${run_script} python ../run_pipeline.py &
fi

if [[ $SLURM_ARRAY_TASK_ID == 1 ]]; then
    cd ${working_dir}/034b
    srun shifter ${run_script} python ../run_pipeline.py &
fi

wait
