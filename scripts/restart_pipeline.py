import os
import sys
from desc.gen3_workflow import ParslGraph

parsl_graph = sys.argv[1]
assert os.path.isfile(parsl_graph)

graph = ParslGraph.restore(parsl_graph)

graph.status()
