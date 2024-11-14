import os
from collections import defaultdict
import click
import pandas as pd
import lsst.daf.butler as daf_butler

repo = "/repo/roman-desc-sims"
butler = daf_butler.Butler(repo, writeable=True)

step = os.path.basename(os.path.abspath('.'))
collections = sorted(set(butler.registry.queryCollections(
    f"u/descdm/{step}_???_w_2024_22/2024*")))
print("# collections:", len(collections), end='\n\n')

# Find all of the available dataset types from the refs, omitting the
# ones that will cause unique key constraint errors, e.g., 'packages',
# and any of the forms '*_config', '*_schema'.
dstype = "*"
refs = sorted(set(butler.registry.queryDatasets(
    dstype, collections=collections[0])))

refs = [ref for ref in refs if ref.datasetType.name == "visitSummary_schema"]
assert(len(refs) == 1)

tagged_collection = f"u/descdm/{step}_output_w_2024_22"

butler.registry.associate(tagged_collection, refs)
