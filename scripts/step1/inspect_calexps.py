import os
from collections import defaultdict
import pandas as pd
import lsst.daf.butler as daf_butler
from lsst.obs.lsst import LsstCam
camera = LsstCam.getCamera()
detectors = {_.getName(): i for i, _ in enumerate(camera)}

repo = "/global/cfs/cdirs/lsst/production/gen3/roman-desc-sims/repo"

butler = daf_butler.Butler(repo)
collections = [f'u/descdm/step1_{i:03d}_w_2024_22' for i in range(40, 60)]
print(collections)

butler = daf_butler.Butler(repo)

#where = ("(exposure=5029112200250 and detector=102) or "
#         "(exposure=5030012400200 and detector=99)")
#where = "exposure in (5029112200250,5030012400200)"
where = None

for collection in collections:
    refs = list(set(butler.registry.queryDatasets("calexp", where=where,
                                                  collections=[collection])
                    .expanded()))
    exp = butler.get(refs[0])
    md = exp.getMetadata()
    print(collection, len(refs), md['RUNNUM'])
    assert os.path.isfile(butler.getURI(refs[0]).path)

#data = defaultdict(list)
#for ref in refs:
#    visit = ref.dataId['visit']
#    data['visit'].append(visit)
#    data['science_program'].append(ref.dataId.records['visit'].science_program)
#    det_name = ref.dataId.records['detector'].full_name
#    data['det_name'].append(det_name)
#    data['detector'].append(detectors[det_name])
#df0 = pd.DataFrame(data)
#
#print(len(df0))
