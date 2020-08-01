from typing import List, Tuple


def decimal_coordinates(lat: List[int], lon: List[int]) -> Tuple[float, float]:
    """Convert coordinates in [int, int, int] format to floats."""
    if int(lat[0]) < 0:
        lat_dec = int(lat[0]) + (-1 * (float(lat[1]) / 60)) + (-1 * (float(lat[2]) / 3600))
    else:
        lat_dec = int(lat[0]) + (float(lat[1]) / 60) + (float(lat[2]) / 3600)
    if int(lon[0]) < 0:
        lon_dec = int(lon[0]) + (-1 * (float(lon[1]) / 60)) + (-1 * (float(lon[2]) / 3600))
    else:
        lon_dec = int(lon[0]) + (float(lon[1]) / 60) + (float(lon[2]) / 3600)
    return lat_dec, lon_dec
