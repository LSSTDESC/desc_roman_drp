import lsst.daf.butler as daf_butler

repo = "/repo/roman-desc-sims"
collections = ['u/descdm/step2b_w_2024_22/20240808T143015Z',
               'u/descdm/step2a_outputs_w_2024_22',
               'u/descdm/step1_output_w_2024_22',
               'LSSTCam/defaults']

butler = daf_butler.Butler(repo, collections=collections)

where = ("instrument='LSSTCam' and skymap='DC2_cells_v1' "
         "and visit in (5025070501810..5025071901170)")
where = None

refs = set(butler.registry.queryDatasets("calexp", where=where))
print(len(refs))

           
