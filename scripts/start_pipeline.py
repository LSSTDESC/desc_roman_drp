from desc.gen3_workflow import start_pipeline

graph = start_pipeline("bps_sfp.yaml")
graph.status()
#graph.run()
