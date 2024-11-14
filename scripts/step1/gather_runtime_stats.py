import os
import glob
from astropy.time import Time


log_dir = "/pscratch/sd/d/descdm/roman-desc-sims/drp/step1/000/submit/u/descdm/step1_000_w_2024_22/20240609T004129Z/logging"


def parse_line(line):
    timestamp = line[len("INFO "):len("INFO 2024-06-09T13:40:32.217")]
    return Time(timestamp, format="isot")


log_file = os.path.join(log_dir, 'visit_detector_5025070501810_105.stderr')
with open(log_file) as fobj:
    lines = fobj.readlines()
    for line in lines:
        if line.startswith("INFO"):
            t_start = parse_line(line)
            break
    for line in lines[-6:]:
        if not line.startswith("INFO"):
            continue
        t_end = parse_line(line)
