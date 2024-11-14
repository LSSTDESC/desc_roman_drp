import os
import glob
import subprocess
import multiprocessing

done = ["000", "001", "002", "003", "004",
        "005", "006", "007", "008", "009",
        "010", "011", "012", "013", "014",
        "016", "017", "018", "019", "020",
        "021", "022", "023", "024", "025",
        "026", "027", "034"]

root_dir = "/pscratch/sd/d/descdm/roman-desc-sims/drp/WFD/step3"

def run_init_pipeline(subdir):
    os.chdir(subdir)
    command = "(time python init_pipeline.py) >& pipeline_init.log"
    subprocess.check_call(command, shell=True)

subdirs = sorted(glob.glob(os.path.join(root_dir, "0??")))

processes = 15

with multiprocessing.Pool(processes=processes) as pool:
    workers = []
    for subdir in subdirs:
        if os.path.basename(subdir) in done:
            continue
        workers.append(pool.apply_async(run_init_pipeline, (subdir,)))
    pool.close()
    pool.join()
    _ = [worker.get() for worker in workers]

