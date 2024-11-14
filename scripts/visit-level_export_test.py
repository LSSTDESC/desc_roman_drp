import os
import lsst.daf.butler as daf_butler

repo = "/repo/roman-desc-sims"
collections = ["u/descdm/preview_data_step1_w_2024_12"]

butler = daf_butler.Butler(repo, collections=collections)

dstypes = ["calexp", "src"]

refs = set()
for dstype in dstypes:
    for ref_iter in butler.registry.queryDatasets(dstype).byParentDatasetType():
        print(ref_iter.parentDatasetType.name)
        refs = refs.union(set(_ for _ in ref_iter.expanded()))
refs = list(refs)
print(len(refs))

output_dir = "export_test_000_no_elements"
os.makedirs(output_dir, exist_ok=True)

with butler.export(directory=output_dir,
                   filename=f"roman-desc-sims_{output_dir}.yaml",
                   transfer="copy") as exporter:
    exporter.saveDatasets(refs[:100], elements=None, transfer=None)
    for collection in collections:
        print(collection, flush=True)
        exporter.saveCollection(collection)
