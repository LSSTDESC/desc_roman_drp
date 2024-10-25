import os
import lsst.daf.butler as daf_butler

repo = "/global/cfs/cdirs/lsst/production/gen3/roman-desc-sims/repo"
collections = ["u/descdm/preview_data_step3_2877_19_w_2024_12/20240403T150003Z",
               "u/descdm/preview_data_step2_w_2024_12/20240327T174129Z",
               "u/descdm/preview_data_step2_w_2024_12/20240326T175855Z",
               "u/descdm/preview_data_step1_w_2024_12/20240326T152819Z",
               "u/descdm/preview_data_step1_w_2024_12/20240324T050830Z",
               "u/descdm/preview_data",
               "refcats/roman-desc-sims",
               "skymaps"]

butler = daf_butler.Butler(repo, collections=collections)

dstypes = ["skyMap", "uw_stars_aug_2021_tp", "raw", "calexp", "src",
           "deepCoadd_nImage", "deepCoadd_calexp", "deepCoadd_forced_src"]
refs = set()
for dstype in dstypes:
    for ref_iter in butler.registry.queryDatasets(dstype).byParentDatasetType():
        print(ref_iter.parentDatasetType.name)
        refs = refs.union(set(_ for _ in ref_iter.expanded()))
refs = list(refs)
print(len(refs))

output_dir = "preview_data"
os.makedirs(output_dir, exist_ok=True)

with butler.export(directory=output_dir,
                   filename="roman-desc-sims_preview_data_export.yaml",
                   transfer="copy") as exporter:
    exporter.saveDatasets(refs)
    for collection in collections:
        print(collection, flush=True)
        exporter.saveCollection(collection)
