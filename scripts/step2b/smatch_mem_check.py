import sys
import gc
from smatch import Matcher
import fitsio
from process_info import ProcessInfo


proc = ProcessInfo()

ra_col, dec_col = "ra", "dec"

def get_primary_dtype(primary_bands):
    """Get the numpy datatype for the primary star catalog.

    Parameters
    ----------
    primary_bands : `list` [`str`]
        List of primary bands.

    Returns
    -------
    dtype : `numpy.dtype`
        Datatype of the primary catalog.
    """
    max_len = max([len(primary_band) for primary_band in primary_bands])

    dtype = [('isolated_star_id', 'i8'),
             (ra_col, 'f8'),
             (dec_col, 'f8'),
             ('primary_band', f'U{max_len}'),
             ('source_cat_index', 'i4'),
             ('nsource', 'i4')]

    for band in primary_bands:
        dtype.append((f'source_cat_index_{band}', 'i4'))
        dtype.append((f'nsource_{band}', 'i4'))

    return dtype


primary_bands = ['i', 'z', 'r', 'g', 'y', 'u']
match_radius = 1.0

star_source_cat = fitsio.read("star_source_cat-2877_part1.fits")
print("star_source_cat", proc.get_info())

dtype = get_primary_dtype(primary_bands)
primary_star_cat = None
for primary_band in primary_bands:
    print("primary_band", proc.get_info())
    use = (star_source_cat['band'] == primary_band)

    ra = star_source_cat[ra_col][use]
    dec = star_source_cat[dec_col][use]

    with Matcher(ra, dec) as matcher:
        print("entered matcher context for band", primary_band, proc.get_info())
        try:
            # New smatch API
            idx = matcher.query_groups(match_radius/3600., min_match=1)
        except AttributeError:
            # Old smatch API
            idx = matcher.query_self(match_radius/3600., min_match=1)
    del matcher
    gc.collect()
    print("exited matcher context for band", primary_band, proc.get_info())
    print(sys.getsizeof(idx))

    count = len(idx)
