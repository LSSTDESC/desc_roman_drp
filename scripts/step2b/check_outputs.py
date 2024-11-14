import lsst.daf.butler as daf_butler

repo = "/repo/roman-desc-sims"
#collections = ["u/descdm/step2b_w_2024_22"]
collections = ["u/descdm/step2b_DM-45773_w_2024_22"]

butler = daf_butler.Butler(repo, collections=collections)

dstypes = ("isolated_star_sources", "isolated_star_cat")

refs = set(butler.registry.queryDatasets(dstypes[0]))
print(len(refs))  # Should be 91 total - 6 failures = 85 refs

refs = set(butler.registry.queryDatasets(dstypes[1]))
print(len(refs))  # Should be 91 total - 6 failures = 85 refs
