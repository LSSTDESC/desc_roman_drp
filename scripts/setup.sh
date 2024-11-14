if [ -z "$1" ]
then
    # set up the most recently available weekly
    foo=`/usr/bin/ls -rt /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib | grep ^w_20`
    weekly_version=`echo $foo | awk -F ' ' '{print $NF}'`
else
    # set up the requested weekly
    weekly_version=$1
fi
export WEEKLY=${weekly_version}

LSST_DISTRIB=/cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib/${weekly_version}
source ${LSST_DISTRIB}/loadLSST-ext.bash
setup lsst_distrib
export OMP_NUM_THREADS=1
export NUMEXPR_MAX_THREADS=1
export OMP_PROC_BIND=false

sw_dir=/global/u1/d/descdm/jchiang/sw
setup -r ${sw_dir}/gen3_workflow -j

wq_env=${sw_dir}/wq_env

export PYTHONPATH=${wq_env}/lib/python3.11/site-packages:${PYTHONPATH}
export PATH=~/bin:${wq_env}/bin:${PATH}

export DAF_BUTLER_REPOSITORY_INDEX=/global/cfs/cdirs/lsst/production/gen3/shared/data-repos.yaml

PS1="\[\033]0;\w\007\][`hostname` ${weekly_version}] "
