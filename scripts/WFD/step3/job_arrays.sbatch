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
#SBATCH --array=0,5,10,15,20,25,30,35,40,45,50,55,60

nodes=$SLURM_ARRAY_TASK_COUNT
echo "# nodes:" $nodes

working_dir=/pscratch/sd/d/descdm/roman-desc-sims/drp/WFD/step3
run_script=${working_dir}/run_command.sh

for index in {0..4}
do
    task_id=$(($SLURM_ARRAY_TASK_ID+$index))
    folder=$(printf "%03d" $task_id)
    cd ${working_dir}/${folder}
    shifter ${run_script} python ../run_pipeline.py &
done
wait
