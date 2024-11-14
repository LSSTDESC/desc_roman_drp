import os
import glob
from desc.gen3_workflow import ParslGraph

pattern = "submit/u/descdm/step3_wfd_0*_w_2024_22/*/parsl_graph_config.pickle"
parsl_graph = sorted(glob.glob(pattern))[-1]

graph = ParslGraph.restore(parsl_graph)

