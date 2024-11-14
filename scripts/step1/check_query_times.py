import time
import lsst.daf.butler as daf_butler

repo = "/repo/roman-desc-sims"
butler = daf_butler.Butler(repo)

collection_template = 'u/descdm/step1_%(job_id)03d_w_2024_22'

for job_id in range(60):
    collection = collection_template % locals()
    t0 = time.time()
    refs = set(butler.registry.queryDatasets(
        "calexp", collections=[collection]).expanded())
    dt = time.time() - t0
    print(f"{collection}  {len(refs):6d}  {dt:.2f}")
