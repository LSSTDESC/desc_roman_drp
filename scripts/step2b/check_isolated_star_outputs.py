import os
import glob
import pandas as pd

root_path = "/global/cfs/cdirs/lsst/production/gen3/roman-desc-sims/repo/u/descdm/step2b_w_2024_22/20240809T204319Z"

pattern = os.path.join(root_path, "isolated_star_sources", "*", "*parq")
isolated_star_source_files = sorted(glob.glob(pattern))
print(len(isolated_star_source_files))

for item in isolated_star_source_files:
    tract = int(os.path.basename(os.path.dirname(item)))
    df = pd.read_parquet(item)
    print(tract, len(df))
#
#
#
#pattern = os.path.join(root_path, "isolated_star_sources", "*", "*parq")
#isolated_star_source_files = sorted(glob.glob(pattern))
#print(len(isolated_star_source_files))



