import os
import numpy as np
import pandas as pd

script_template = """from desc.gen3_workflow import start_pipeline
graph = start_pipeline("bps_step1_%(job_folder)s.yaml")
"""

with open("bps_step1_template.yaml") as fobj:
    template = ''.join(fobj.readlines())
curdir = os.path.abspath('.')

num_jobs = 60
df0 = pd.read_parquet("raw_data_summary.parquet")
exposures = sorted(set(df0['exposure']))
indexes = np.linspace(0, len(exposures)+1, num_jobs+1, dtype=int)

for job_number, (imin, imax) in enumerate(list(zip(indexes[:-1], indexes[1:]))):
    sublist = exposures[imin:imax]
    exposure_list = f"({min(sublist)}..{max(sublist)})"
    job_folder = f"{job_number:03d}"
    job_dir = os.path.join(curdir, job_folder)
    os.makedirs(job_dir, exist_ok=True)
    script_file = os.path.join(job_dir, "init_pipeline.py")
    if not os.path.isfile(script_file):
        with open(script_file, "w") as fobj:
            fobj.write(script_template % locals())
    outfile = os.path.join(job_dir, f"bps_step1_{job_number:03d}.yaml")
    if not os.path.isfile(outfile):
        with open(outfile, "w") as fobj:
            fobj.write(template % locals())
