#!/bin/bash

# For running in production mode on Perlmutter:
#SBATCH --image=docker:lsstsqre/centos:7-stack-lsst_distrib-w_2024_22

#SBATCH -q regular
#SBATCH --time=5:00:00

##SBATCH -q debug
##SBATCH --time=00:10:00

#SBATCH --constraint=cpu
#SBATCH -A m1727
#SBATCH -L scratch,cfs

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --array=0-59

nodes=$SLURM_ARRAY_TASK_COUNT
echo "# nodes:" $nodes

working_dir=/pscratch/sd/d/descdm/roman-desc-sims/drp/step2a
run_script=${working_dir}/run_command.sh

folder=$(printf "%03d" $SLURM_ARRAY_TASK_ID)
cd ${working_dir}/${folder}

srun shifter ${run_script} python ../run_pipeline.py &

wait
