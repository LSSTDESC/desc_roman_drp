#!/bin/bash
#
# This wrapper script could be used with a shifter image to wrap a
# command line like this:
#
# # shifter --image=lsstsqre/centos:7-stack-lsst_distrib-w_2024_12 /pscratch/sd/d/descdm/roman-desc-sims/drp/cl_wrapper.sh <command line>
#
source /opt/lsst/software/stack/loadLSST.bash
setup lsst_distrib

export OMP_NUM_THREADS=1
export NUMEXPR_MAX_THREADS=1
export OMP_PROC_BIND=false

sw_dir=/pscratch/sd/d/descdm/roman-desc-sims/sw
setup -r ${sw_dir}/gen3_workflow -j

wq_env=${sw_dir}/wq_env
export PYTHONPATH=${wq_env}/lib/python3.11/site-packages:${PYTHONPATH}
export PATH=${wq_env}/bin:${PATH}

$*
exit $?
