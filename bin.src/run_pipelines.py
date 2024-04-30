#!/usr/bin/env python
import os
import glob
import datetime
import argparse
import numpy as np
import lsst.daf.butler as daf_butler
from desc.gen3_workflow import ParslGraph


def get_dsrefs(butler, job_names):
    refs = []
    visits = set()
    for job_name in job_names:
        tokens = job_name.split('_')
        visit, detector = tokens[-2:]
        visits.add(visit)
    visits = sorted(visits)
    where = f"instrument='LSSTCam' and visit in ({min(visits)}..{max(visits)})"
    refs.extend(butler.registry.queryDatasets("icExp", where=where))
    refs.extend(butler.registry.queryDatasets("postISRCCD", where=where))
    return refs


def log(message):
    time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{time_stamp}: {message}")


parser = argparse.ArgumentParser()
parser.add_argument("--run_collection", type=str, default=None,
                    help="The run collection to process")
parser.add_argument("--ntranches", type=int, default=10,
                    help="Number of CCD-visit tranches")
parser.add_argument("--max_threads", type=int, default=4,
                    help="Maximum number of threads")
parser.add_argument("--repo", type=str, default="/repo/roman-desc-sims",
                    help="Butler repo")
args = parser.parse_args()

log(args)

run_collection = args.run_collection
if run_collection is None:
    # find the most recent run in the submit folder
    run_collection = sorted(glob.glob("submit/u/*/*/*"),
                            key=os.path.basename)[-1][len("submit/"):]
ntranches = args.ntranches
max_threads = args.max_threads
repo = args.repo

#
# Butler to use for pruning datasets after each tranche finishes.
#
collections = [run_collection]
butler = daf_butler.Butler(repo, collections=collections, writeable=True)

#
# Read in the parsl graph, setting the max_threads config for this run.
#
parsl_config = dict(retries=1, monitoring=True, checkpoint=False,
                    executor="ThreadPool", max_threads=max_threads)
parsl_graph_file = f"submit/{run_collection}/parsl_graph_config.pickle"
graph = ParslGraph.restore(parsl_graph_file, parsl_config=parsl_config)


#
# Get all of the `visit` jobs and create tranche indexes.
#
jobs = graph.get_jobs("visit", None)
indexes = np.linspace(0, len(jobs)+1, ntranches+1, dtype=int)

#
# Loop over tranches, running pipetasks and prunning intermediates.
#
for imin, imax in zip(indexes[:-1], indexes[1:]):
    current_tranche = jobs[imin:imax]
    log("Processing %s CCD-visits." % len(current_tranche))
    graph.run(current_tranche, block=True, shutdown=False)

    # Get dataset refs for intermediates, and delete them from the repo.
    refs = get_dsrefs(butler, current_tranche)
    log("Pruning %s" % len(refs))
    butler.pruneDatasets(refs, unstore=True, purge=True)
