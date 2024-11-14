import os
import glob
import subprocess
import multiprocessing


def init_pipeline(folder):
    os.chdir(folder)
    command = "(time python init_pipeline.py) >& pipeline_init.log"
    subprocess.check_call(command, shell=True)


#folders = '003 004 006 009 016 017 020 033 038 041 042 043 045 046'.split()
folders = sorted(glob.glob("./0*"))

processes = len(folders)
with multiprocessing.Pool(processes=processes) as pool:
    workers = []
    for folder in folders:
        workers.append(pool.apply_async(init_pipeline, (folder,)))
    pool.close()
    pool.join()

    _ = [worker.get() for worker in workers]


