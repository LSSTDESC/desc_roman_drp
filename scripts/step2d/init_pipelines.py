import os
import glob
import subprocess
import multiprocessing


def init_pipeline(folder):
    os.chdir(folder)
    command = "(time python init_pipeline.py) >& pipeline_init.log"
    subprocess.check_call(command, shell=True)


folders = [_ for _ in sorted(glob.glob("./0*"))
           if os.path.basename(_) not in ('000', '057')]

print(folders)

processes = len(folders)
with multiprocessing.Pool(processes=processes) as pool:
    workers = []
    for folder in folders:
        workers.append(pool.apply_async(init_pipeline, (folder,)))
    pool.close()
    pool.join()

    _ = [worker.get() for worker in workers]


