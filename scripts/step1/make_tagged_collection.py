import os
from collections import defaultdict
import click
import pandas as pd
import lsst.daf.butler as daf_butler

repo = "/repo/roman-desc-sims"
butler = daf_butler.Butler(repo, writeable=True)


step = "step1"
collections = sorted(set(butler.registry.queryCollections(
    f"u/descdm/{step}_???_w_2024_22/2024*")))
print("# collections:", len(collections), end='\n\n', flush=True)
#print(collections, flush=True, end='\n\n')

# Find all of the available dataset types from the refs, omitting the
# ones that will cause unique key constraint errors, e.g., 'packages',
# and any of the forms '*_config', '*_schema'.
dstype = "*"
refs = sorted(set(butler.registry.queryDatasets(
    dstype, collections=collections[0])))
print("# refs:", len(refs), end='\n\n', flush=True)

dstypes = set()
for ref in refs:
    dstype_name = ref.datasetType.name
    if (dstype_name == 'packages'
        or dstype_name.split('_')[-1] in ('config',)):
        continue
    dstypes.add(dstype_name)

print("dataset types:", flush=True)
print(dstypes, end='\n\n', flush=True)

#dstypes = {'source', 'sourceTable', 'isr_log', 'icSrc',
#           'characterizeImage_log', 'calibrate_metadata',
#           'transformSourceTable_metadata', 'postISRCCD',
#           'calexpBackground', 'icExp', 'transformSourceTable_log',
#           'src', 'characterizeImage_metadata', 'isr_metadata',
#           'srcMatch', 'icExpBackground', 'writeSourceTable_log',
#           'calexp', 'calibrate_log', 'writeSourceTable_metadata',
#           'srcMatchFull'}
#
refs = sorted(set(butler.registry.queryDatasets(
    dstypes, collections=collections)))
print("# refs:", len(refs), end='\n\n', flush=True)

#tagged_collection = f"u/descdm/{step}_output_w_2024_22"
#
#try:
#    butler.registry.queryCollections(tagged_collection)
#except daf_butler.registry.MissingCollectionError:
#    pass
#else:
#    print(f"Collection {tagged_collection} exists. ", flush=True)
#    if click.confirm("Overwrite?", default=True):
#        butler.registry.removeCollection(tagged_collection)
#    else:
#        sys.exit(0)
#
#butler.registry.registerCollection(tagged_collection)
#butler.registry.associate(tagged_collection, refs)
