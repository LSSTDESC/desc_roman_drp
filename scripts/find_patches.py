from collections import defaultdict
import pandas as pd
import lsst.daf.butler as daf_butler
from desc_roman_sims import SurveyRegion

ra0, dec0 = 9.5, -44
lon_size, lat_size = 5, 5
survey_region = SurveyRegion(ra0, dec0, lon_size, lat_size)

repo = "/repo/roman-desc-sims"
collections = ["LSSTCam/defaults"]

butler = daf_butler.Butler(repo, collections=collections)
skymap = butler.get("skyMap", name="DC2_cells_v1")

tracts = [2534, 2535, 2536, 2537,
          2702, 2703, 2704, 2705,
          2875, 2876, 2877, 2878,
          3052, 3053, 3054, 3055, 3056,
          3233, 3234, 3235, 3236, 3237]

data = defaultdict(list)
for tract in tracts:
    for i, patch in enumerate(skymap[tract]):
        if patch.getOuterSkyPolygon().intersects(survey_region.polygon):
            data['tract'].append(tract)
            data['patch'].append(i)

df0 = pd.DataFrame(data)
