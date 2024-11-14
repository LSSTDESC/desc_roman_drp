import os
import numpy as np
import pandas as pd

curdir = os.path.abspath('.')
step = os.path.basename(curdir)

script_template = """from desc.gen3_workflow import start_pipeline
graph = start_pipeline("bps_%(step)s_%(job_folder)s.yaml")
graph.shutdown()
"""

with open(f"bps_{step}_template.yaml") as fobj:
    template = ''.join(fobj.readlines())

num_jobs = 60
df0 = pd.read_parquet("../raw_data_summary.parquet")
exposures = sorted(set(df0['exposure']))
indexes = np.linspace(0, len(exposures)+1, num_jobs+1, dtype=int)

for job_number, (imin, imax) in enumerate(list(zip(indexes[:-1], indexes[1:]))):
    sublist = exposures[imin:imax]
    visit_list = f"({min(sublist)}..{max(sublist)})"
    job_folder = f"{job_number:03d}"
    job_dir = os.path.join(curdir, job_folder)
    os.makedirs(job_dir, exist_ok=True)

    script_file = os.path.join(job_dir, "init_pipeline.py")
    with open(script_file, "w") as fobj:
        fobj.write(script_template % locals())

    outfile = os.path.join(job_dir, f"bps_{step}_{job_number:03d}.yaml")
    with open(outfile, "w") as fobj:
        fobj.write(template % locals())
