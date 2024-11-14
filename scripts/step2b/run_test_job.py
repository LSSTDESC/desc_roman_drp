from desc.gen3_workflow import start_pipeline, ParslGraph

graph = start_pipeline("bps_step2b_test_job.yaml")
#graph = ParslGraph.restore("/pscratch/sd/d/descdm/roman-desc-sims/drp/step2b/submit/u/descdm/"
#                           "step2b_test_job_w_2024_22/"
#                           "20240812T170608Z/parsl_graph_config.pickle")

graph.status()

graph.run(block=True)
