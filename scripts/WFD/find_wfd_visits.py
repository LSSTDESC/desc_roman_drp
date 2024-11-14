import os
import glob
import sqlite3
import pandas as pd

# Get list of simulated visits from file system
root_dir = "/global/cfs/cdirs/lsst/production/roman-desc-sims/raw_data"
visit_dirs = sorted(glob.glob(os.path.join(root_dir, '*')))
all_visits = [int(os.path.basename(_)) for _ in visit_dirs]
print("# simulated visits:", len(all_visits))

opsim_db_file = ("/global/cfs/cdirs/descssim/imSim/lsst/data/"
                 "baseline_v3.2_10yrs.db")
assert os.path.isfile(opsim_db_file)

query = ("select * from observations "
         "where 3.58 < fieldRA and fieldRA < 15.42 and "
         "-48.26 < fieldDec and fieldDec < -39.74 and "
         "38064 <= observationId and observationId <= 1104696 and "
         "target==''")
#         "60860.0 < observationStartMJD and observationStartMJD < 62621.0")

with sqlite3.connect(opsim_db_file) as con:
    df0 = pd.read_sql(query, con)

print(len(df0))

wfd_visits = set(df0['observationId']).intersection(all_visits)
print(len(wfd_visits))

