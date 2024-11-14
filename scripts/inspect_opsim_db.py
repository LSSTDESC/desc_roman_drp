import os
import sqlite3
import pandas as pd

opsim_db_file = ("/global/cfs/cdirs/descssim/imSim/lsst/data/"
                 "baseline_v3.2_10yrs.db")
assert os.path.isfile(opsim_db_file)

query = ("select * from observations "
         "where 3.58 < fieldRA and fieldRA < 15.42 and "
         "-48.26 < fieldDec and fieldDec < -39.74 and "
         "38064 <= observationId and observationId <= 1104696")
#         "60860.0 < observationStartMJD and observationStartMJD < 62621.0")

with sqlite3.connect(opsim_db_file) as con:
    df0 = pd.read_sql(query, con)

print(len(df0))

"""
sample visits to check BFK:
>u: 49245
>g: 38064
>r: 1020331
>i: 547846
>z: 377527
y: 128973
"""
