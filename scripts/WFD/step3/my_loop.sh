#!/bin/bash

slurm_array_task_id=3

for index in {0..4}
do
    task_id=$(($slurm_array_task_id + $index))
    folder=$(printf "%03d" $task_id)
    echo $folder
done
