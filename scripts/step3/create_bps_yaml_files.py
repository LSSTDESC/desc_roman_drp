import os
import numpy as np
import pandas as pd

def make_query_list(input_list):
    my_list = sorted(set(input_list))
    previous = my_list[0]
    segments = []
    current_segment = [previous]
    for current in my_list[1:]:
        if current != previous + 1:
            current_segment.append(previous)
            segments.append(current_segment)
            current_segment = [current]
        previous = current
    current_segment.append(current)
    segments.append(current_segment)

    items = []
    for segment in segments:
        if segment[0] == segment[1]:
            items.append(str(segment[0]))
        elif segment[0] + 1 == segment[1]:
            items.extend(str(_) for _ in segment)
        else:
            items.append(f"{segment[0]}..{segment[1]}")
    index_list = ','.join(items)
    return index_list


script_template = """from desc.gen3_workflow import start_pipeline
graph = start_pipeline("bps_step3_%(job_folder)s.yaml")
graph.shutdown()
"""

with open("bps_step3_template.yaml") as fobj:
    template = ''.join(fobj.readlines())
curdir = os.path.abspath('.')

df0 = pd.read_parquet("../survey_region_patches.parquet")
tracts = sorted(set(df0['tract']))
max_num_patches = 20

patch_lists = []
for tract in tracts:
    print(tract)
    patches = sorted(df0.query(f"tract=={tract}")['patch'])
    if len(patches) > max_num_patches:
        num_chunks = len(patches) // max_num_patches
        if len(patches) % max_num_patches:
            num_chunks += 1
        indexes = np.linspace(0, len(patches) + 1, num_chunks + 1, dtype=int)
        for imin, imax in zip(indexes[:-1], indexes[1:]):
            patch_lists.append((tract, make_query_list(patches[imin:imax])))
    else:
        patch_lists.append((tract, make_query_list(patches)))

for job_number, (tract, patch_list) in enumerate(patch_lists):
    job_folder = f"{job_number:03d}"
    job_dir = os.path.join(curdir, job_folder)
    os.makedirs(job_dir, exist_ok=True)
    script_file = os.path.join(job_dir, "init_pipeline.py")
    if True:
#    if not os.path.isfile(script_file):
        with open(script_file, "w") as fobj:
            fobj.write(script_template % locals())
    outfile = os.path.join(job_dir, f"bps_step3_{job_number:03d}.yaml")
    with open(outfile, "w") as fobj:
        fobj.write(template % locals())
