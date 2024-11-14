import os
import glob
from desc.gen3_workflow import ParslGraph

parsl_graph = "submit/u/descdm/step2b_DM-45773_w_2024_22/20240815T224442Z/parsl_graph_config.pickle"
assert os.path.isfile(parsl_graph)

parsl_config = dict(retries=1, monitoring=True, checkpoint=False,
                    executor="ThreadPool", max_threads=3)

graph = ParslGraph.restore(parsl_graph, parsl_config=parsl_config)

graph.status()
graph.run(block=True)
