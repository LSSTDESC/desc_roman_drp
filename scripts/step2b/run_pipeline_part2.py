import os
import glob
from desc.gen3_workflow import ParslGraph

parsl_graph = "submit/u/descdm/step2b_part2_w_2024_22/20240814T194051Z/parsl_graph_config.pickle"
assert os.path.isfile(parsl_graph)

parsl_config = dict(retries=1, monitoring=True, checkpoint=False,
                    executor="ThreadPool", max_threads=1)

graph = ParslGraph.restore(parsl_graph, parsl_config=parsl_config)

graph.status()
graph.run(block=True)
