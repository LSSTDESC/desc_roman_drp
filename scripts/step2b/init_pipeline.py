from desc.gen3_workflow import start_pipeline
graph = start_pipeline("bps_step2b_DM-45773.yaml")
graph.shutdown()
