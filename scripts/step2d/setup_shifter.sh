#
# shifter --image lsstsqre/centos:7-stack-lsst_distrib-w_2024_22
#
set -o ignoreeof  # Disable ctrl-d logout

source /opt/lsst/software/stack/loadLSST.bash
setup lsst_distrib

export OMP_NUM_THREADS=1
export NUMEXPR_MAX_THREADS=1
export OMP_PROC_BIND=false

export DRP_STEP=`echo $PWD | awk -F '/' '{print $NF}'`

export DAF_BUTLER_REPOSITORY_INDEX=/global/cfs/cdirs/lsst/production/gen3/shared/data-repos.yaml

sw_dir=/global/homes/d/descdm/jchiang/sw
setup -r ${sw_dir}/gen3_workflow -j
setup -r ${sw_dir}/sims_ci_pipe -j
setup -r ${sw_dir}/desc_roman_drp -j

export PATH=~/bin:${PATH}

version=`eups list lsst_distrib | sed 's/\s\+/\n/g' | grep w_[0-9]*_[0-9]*`
export WEEKLY=${version}

PS1='(`hostname` ${version}) '
