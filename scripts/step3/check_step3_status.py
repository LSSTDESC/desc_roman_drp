import os
import glob
import time
from desc.gen3_workflow import ParslGraph

run_folders = sorted([_ for _ in glob.glob("0*") if _ != '034'])
for folder in run_folders[37:]:
    os.chdir(folder)
    parsl_graph = sorted(glob.glob(f"submit/u/descdm/step3_{folder}_w_2024_22/2024*/parsl_graph_config.pickle"))[-1]

    graph = ParslGraph.restore(parsl_graph, use_dfk=True)

    df = graph.df.query("task_type == 'makeWarp'")
    finished = len(df.query("(status == 'exec_done' or status == 'failed')"))
    total = len(df)
    print(folder, total, total - finished)
    if finished > 0:
        print(f"running finalize for folder {folder}:", end="  ")
        t0 = time.time()
        graph.finalize()
        print((time.time() - t0)/60., flush=True)
    graph.shutdown()
    os.chdir('..')
