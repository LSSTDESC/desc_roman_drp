import os
import glob
from collections import defaultdict
from astropy.time import Time
import pandas as pd


def time_field(line):
    return Time(line.split()[1][:len("2024-07-05T08:52:47.346")])

def extract_log_times(qg_file):
    with open(qg_file) as fobj:
        lines = fobj.readlines()
    keys = []
    times = []
    info_targets = [("initial_query", "Processing pipeline subgraph"),
                    ("processing_initial_query",
                     "Iterating over query results to associate quanta with"),
                    ("processing_subqueries", "Initial bipartite graph has"),
                    ("writing_QG", "Writing QuantumGraph")]
    info_key, target = info_targets.pop(0)
    for line in lines:
        if target in line:
            keys.append(info_key)
            times.append(time_field(line))
            try:
                info_key, target = info_targets.pop(0)
            except IndexError:
                pass
        elif "Found" in line:
            dstype = line.strip().split()[-1][1:-2]
            keys.append(dstype)
            times.append(time_field(line))

    dts = {}
    for i in range(1, len(keys)):
        dts[keys[i-1]] = (times[i] - times[i-1]).value * 24 * 3600.0
    if times:
        dts['total'] = (times[-1] - times[0]).value * 24 *60.0
    return dts

dfs = {}
steps = [f"step{i}" for i in range(1, 4)]
for step in steps:
    data = defaultdict(list)
    print(step)
    tranche_folders = sorted(glob.glob(os.path.join(step, "0??")))
    for folder in tranche_folders:
        tranche = int(os.path.basename(folder))
        pattern = os.path.join(folder, "submit/u/descdm/step*/2024*",
                               "quantumGraphGeneration.out")
        try:
            qg_file = sorted(glob.glob(pattern))[-1]
        except IndexError:
            continue

        dts = extract_log_times(qg_file)
        if not dts:
            continue
        data["step"].append(step)
        data["tranche"].append(tranche)

        for key, dt in dts.items():
            data[key].append(dt)
    dfs[step] = pd.DataFrame(data)
