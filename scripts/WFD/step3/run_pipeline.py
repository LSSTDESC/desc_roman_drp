import os
import glob
from desc.gen3_workflow import ParslGraph

folder = os.path.basename(os.path.abspath('.'))

# Find the most recent parsl graph file.
parsl_graph = sorted(glob.glob(f"submit/u/descdm/step3_wfd_{folder}_w_2024_22/2024*/parsl_graph_config.pickle"))[-1]
assert os.path.isfile(parsl_graph)

parsl_config = dict(retries=1, monitoring=True, checkpoint=False,
                    executor="ThreadPool", max_threads=24)

graph = ParslGraph.restore(parsl_graph, parsl_config=parsl_config)

graph.status()
jobs = graph.get_jobs("healSparsePropertyMaps", status=None)
jobs += graph.get_jobs("templateGen", status=None)
jobs += graph.get_jobs("deblend", status=None)
graph.run(jobs=jobs, block=True)
graph.finalize()

