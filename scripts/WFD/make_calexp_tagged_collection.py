import os
from collections import defaultdict
import click
import sqlite3
import pandas as pd
import lsst.daf.butler as daf_butler

def get_wfd_visits():
    opsim_db_file = ("/global/cfs/cdirs/descssim/imSim/lsst/data/"
                     "baseline_v3.2_10yrs.db")
    assert os.path.isfile(opsim_db_file)
    query = ("select observationId from observations "
             "where 3.58 < fieldRA and fieldRA < 15.42 and "
             "-48.26 < fieldDec and fieldDec < -39.74 and "
             "38064 <= observationId and observationId <= 1104696 and "
             "target==''")
    with sqlite3.connect(opsim_db_file) as con:
        df0 = pd.read_sql(query, con)
    return set(df0['observationId'])

wfd_visits = set(str(_) for _ in get_wfd_visits())

repo = "/repo/roman-desc-sims"
butler = daf_butler.Butler(repo, writeable=True)

step = "step1"
collections = sorted(set(butler.registry.queryCollections(
    f"u/descdm/{step}_???_w_2024_22/2024*")))
print("# collections:", len(collections), end='\n\n', flush=True)
#print(collections, flush=True, end='\n\n')

tagged_collection = f"u/descdm/{step}_wfd_calexp_w_2024_22"

try:
    butler.registry.queryCollections(tagged_collection)
except daf_butler.registry.MissingCollectionError:
    pass
else:
    print(f"Collection {tagged_collection} exists. ", flush=True)
    if click.confirm("Overwrite?", default=True):
        butler.registry.removeCollection(tagged_collection)
    else:
        sys.exit(0)

butler.registry.registerCollection(tagged_collection)

dstypes = {'calexp'}

for i, collection in enumerate(collections):
    refs = sorted(set(butler.registry.queryDatasets(
        dstypes, collections=[collection]).expanded()))
    wfd_refs = [_ for _ in refs
                if _.dataId.records['visit'].science_program in wfd_visits]
    print(i, len(wfd_refs), len(refs), flush=True)
    butler.registry.associate(tagged_collection, wfd_refs)
