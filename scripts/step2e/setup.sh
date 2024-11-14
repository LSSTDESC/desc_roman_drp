if [ -z "$1" ]
then
    # set up the most recently available weekly
    foo=`/usr/bin/ls -rt /cvmfs/sw.lsst.eu/linux-x86_64/lsst_distrib | grep ^w_20`
    weekly_version=`echo $foo | awk -F ' ' '{print $NF}'`
    weekly_version=w_2024_22
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

export DRP_STEP=`echo $PWD | awk -F '/' '{print $NF}'`

export DAF_BUTLER_REPOSITORY_INDEX=/global/cfs/cdirs/lsst/production/gen3/shared/data-repos.yaml

sw_dir=/global/homes/d/descdm/jchiang/sw
setup -r ${sw_dir}/gen3_workflow -j
setup -r ${sw_dir}/desc_roman_drp -j

wq_env=${sw_dir}/wq_env

export PYTHONPATH=${wq_env}/lib/python3.11/site-packages:${PYTHONPATH}
export PATH=~/bin:${wq_env}/bin:${PATH}

PS1="\[\033]0;\w\007\][`hostname` ${weekly_version}] "
