from __future__ import annotations

from typing import Tuple, List
from math import cos, radians

def bbox_from_center(lat: float, lon: float, half_size_m: float) -> List[float]:
    """
    Rough bbox from center in meters (WGS84 degrees). Good enough for ~100km AOIs.
    Returns [min_lon, min_lat, max_lon, max_lat].
    """
    # Approx conversions
    dlat = half_size_m / 111_320.0
    dlon = half_size_m / (111_320.0 * cos(radians(lat)))
    return [lon - dlon, lat - dlat, lon + dlon, lat + dlat]
