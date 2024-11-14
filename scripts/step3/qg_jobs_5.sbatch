#!/bin/bash

# For running in production mode on Perlmutter:
#SBATCH --image=docker:lsstsqre/centos:7-stack-lsst_distrib-w_2024_22

#SBATCH -q regular
#SBATCH --time=24:00:00

##SBATCH -q debug
##SBATCH --time=00:10:00

#SBATCH --constraint=cpu
#SBATCH -A m1727
#SBATCH -L scratch,cfs

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1

working_dir=/pscratch/sd/d/descdm/roman-desc-sims/drp/step3
run_script=${working_dir}/run_command.sh

cd ${working_dir}/034
shifter ${run_script} python init_pipeline_a.py >& pipeline_init_a.log &
shifter ${run_script} python init_pipeline_b.py >& pipeline_init_b.log &

wait
