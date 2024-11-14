from collections import defaultdict
import pandas as pd
import lsst.daf.butler as daf_butler

repo = "/global/cfs/cdirs/lsst/production/gen3/roman-desc-sims/repo"

butler = daf_butler.Butler(repo)
collections = []
for collection in butler.registry.queryCollections():
    if "sfp_test_w_bfk" in collection:
        collections.append(collection)

butler = daf_butler.Butler(repo, collections=collections)

refs = list(set(butler.registry.queryDatasets("calexp").expanded()))
print(len(refs))

data = defaultdict(list)
for ref in refs:
    visit = ref.dataId['visit']
    if visit in set(data['visit']):
        continue
    data['visit'].append(visit)
    data['science_program'].append(ref.dataId.records['visit'].science_program)
df = pd.DataFrame(data)

print(df)
