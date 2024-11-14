from desc.gen3_workflow import start_pipeline
graph = start_pipeline("bps_step2e.yaml")
graph.shutdown()
