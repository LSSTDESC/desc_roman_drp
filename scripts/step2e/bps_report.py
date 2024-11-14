#!/usr/bin/env python
import os
import glob
from desc.gen3_workflow import ParslGraph


parsl_graph = sorted(glob.glob(f"submit/u/descdm/step2e*/"
                               "2024*/parsl_graph_config.pickle"))[-1]

assert os.path.isfile(parsl_graph)
graph = ParslGraph.restore(parsl_graph, use_dfk=False)
graph.status()
