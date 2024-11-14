import os
import glob
import subprocess
import multiprocessing


def init_pipeline(folder):
    os.chdir(folder)
    command = "(time python init_pipeline.py) >& pipeline_init.log"
    print(folder, command)
    subprocess.check_call(command, shell=True)


#folders = sorted(glob.glob("./0*"))
folders = sorted([_ for _ in glob.glob("./0*")
                  if int(os.path.basename(_)) > 11])

for folder in folders:
    if '016' in folder:
        continue
    print(folder)
    init_pipeline(os.path.abspath(folder))
    os.chdir('..')


#print(folders)
#processes = 5
#with multiprocessing.Pool(processes=processes) as pool:
#    workers = []
#    for folder in folders:
#        abs_path = os.path.abspath(folder)
#        workers.append(pool.apply_async(init_pipeline, (abs_path,)))
#    pool.close()
#    pool.join()
#
#    _ = [worker.get() for worker in workers]
