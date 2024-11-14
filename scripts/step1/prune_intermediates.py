import os
import glob
import time
import lsst.daf.butler as daf_butler


def get_dsrefs(butler, collection, visit_range,
               dstypes=("icExp", "postISRCCD")):
    refs = []
    where = f"instrument='LSSTCam' and visit in {visit_range}"
    for dstype in dstypes:
        refs.extend(butler.registry.queryDatasets(dstype,
                                                  collections=[collection],
                                                  where=where))
    return refs


repo = "/repo/roman-desc-sims"
butler = daf_butler.Butler(repo, writeable=True)

tranche_dirs = [f"{i:03d}" for i in range(60)]
for tranche_dir in tranche_dirs[30:]:
    collection = f"u/descdm/step1_{tranche_dir}_w_2024_22"
    bps_file = f"{tranche_dir}/bps_step1_{tranche_dir}.yaml"
    with open(bps_file) as fobj:
        for line in fobj:
            if "dataQuery" in line:
                visit_range = line[line.find("("):].strip('"\n')
    refs = get_dsrefs(butler, collection, visit_range)
    print(f"{tranche_dir}: pruning {len(refs)} dataset refs", end="  ")
    t0 = time.time()
    butler.pruneDatasets(refs, unstore=True, purge=True)
    print("execution time:", (time.time() - t0)/60., "mins")
