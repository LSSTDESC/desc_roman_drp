#
# shifter --image lsstsqre/centos:7-stack-lsst_distrib-w_2024_12
#
set -o ignoreeof  # Disable ctrl-d logout

source /opt/lsst/software/stack/loadLSST.bash
setup lsst_distrib

export OMP_NUM_THREADS=1
export NUMEXPR_MAX_THREADS=1
export OMP_PROC_BIND=false

sw_dir=/pscratch/sd/d/descdm/roman-desc-sims/sw
setup -r ${sw_dir}/gen3_workflow -j
setup -r ${sw_dir}/sims_ci_pipe -j

export PATH=~/bin:${PATH}

version=`eups list lsst_distrib | sed 's/\s\+/\n/g' | grep w_[0-9]*_[0-9]*`
export WEEKLY=${version}

PS1='(`hostname` ${version}) '
