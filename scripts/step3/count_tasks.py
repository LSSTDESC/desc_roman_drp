import os
import glob
from collections import defaultdict
import pandas as pd

pattern = "0*/submit/u/descdm/step3_0*_w_2024_22"
submit_folders = sorted(_ for _ in glob.glob(pattern) if "034/submit" not in _)

print(len(submit_folders))

qg_files = []
for submit_folder in submit_folders:
    submit_dir = sorted(glob.glob(os.path.join(submit_folder, '2024*')))[-1]
    qg_file = os.path.join(submit_dir, 'quantumGraphGeneration.out')
    assert os.path.isfile(qg_file)
    qg_files.append(qg_file)
print(len(qg_files))

data = defaultdict(list)
for qg_file in qg_files:
    partition = qg_file.split('/')[0]
    found_quanta = False
    with open(qg_file, 'r') as fobj:
        lines = fobj.readlines()
        for line in lines:
            if line.startswith('Quanta'):
                found_quanta = True
                data['partition'].append(partition)
            if found_quanta:
                if 'makeWarp' in line:
                    count = int(line.strip().split()[0])
                    data['makeWarp'].append(count)
                elif 'assembleCoadd' in line:
                    count = int(line.strip().split()[0])
                    data['assembleCoadd'].append(count)
df0 = pd.DataFrame(data)

                    
