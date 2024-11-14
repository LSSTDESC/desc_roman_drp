import os
import glob
from desc.gen3_workflow import ParslGraph, start_pipeline

#parsl_graph = "submit/u/descdm/step2b_part1_w_2024_22/20240814T193415Z/parsl_graph_config.pickle"
#assert os.path.isfile(parsl_graph)
#
#parsl_config = dict(retries=1, monitoring=True, checkpoint=False,
#                    executor="ThreadPool", max_threads=1)

#graph = ParslGraph.restore(parsl_graph, parsl_config=parsl_config)
graph = start_pipeline("bps_step2b_part1.yaml")

graph.status()
#graph.run(block=True)
