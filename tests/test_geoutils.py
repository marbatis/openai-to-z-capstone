import math

import pytest

from zexplorer.geoutils import bbox_from_center


# Helper functions matching the implementation's approximations
def _expected_dlat(half_size_m: float) -> float:
    return half_size_m / 111_320.0


def _expected_dlon(lat_deg: float, half_size_m: float) -> float:
    return half_size_m / (111_320.0 * math.cos(math.radians(lat_deg)))


@pytest.mark.parametrize(
    "lat, lon, half_m",
    [
        (0.0, -60.0, 100_000.0),  # Equator, ~100 km half-size
        (60.0, -60.0, 100_000.0),  # Northern mid-high latitude
        (-60.0, -60.0, 100_000.0),  # Southern mid-high latitude
    ],
)
def test_bbox_center_and_sizes(lat, lon, half_m):
    bbox = bbox_from_center(lat, lon, half_m)
    min_lon, min_lat, max_lon, max_lat = bbox

    # Basic ordering
    assert min_lon < max_lon, "min_lon should be less than max_lon"
    assert min_lat < max_lat, "min_lat should be less than max_lat"

    # Center should be preserved (within float tolerance)
    calc_center_lat = (max_lat + min_lat) / 2.0
    calc_center_lon = (max_lon + min_lon) / 2.0
    assert pytest.approx(calc_center_lat, rel=1e-12, abs=1e-12) == lat
    assert pytest.approx(calc_center_lon, rel=1e-12, abs=1e-12) == lon

    # Half spans should match the simple spherical approximations used by the function
    dlat = (max_lat - min_lat) / 2.0
    dlon = (max_lon - min_lon) / 2.0
    assert pytest.approx(dlat, rel=1e-6) == _expected_dlat(half_m)
    assert pytest.approx(dlon, rel=1e-6) == _expected_dlon(lat, half_m)


def test_longitude_scale_inflates_toward_poles():
    half_m = 100_000.0  # ~100 km
    # Equator
    bbox_eq = bbox_from_center(0.0, 0.0, half_m)
    dlon_eq = (bbox_eq[2] - bbox_eq[0]) / 2.0

    # At 60 degrees latitude, cos(60)=0.5 so expected dlon doubles
    bbox_60 = bbox_from_center(60.0, 0.0, half_m)
    dlon_60 = (bbox_60[2] - bbox_60[0]) / 2.0
    assert pytest.approx(dlon_60, rel=1e-6) == 2.0 * dlon_eq


def test_latitude_scale_constant_with_lat():
    half_m = 100_000.0
    dlat_eq = (bbox_from_center(0.0, 0.0, half_m)[3] - bbox_from_center(0.0, 0.0, half_m)[1]) / 2.0
    dlat_60 = (
        bbox_from_center(60.0, 0.0, half_m)[3] - bbox_from_center(60.0, 0.0, half_m)[1]
    ) / 2.0
    # Using the same approximation as the function, dlat does not depend on latitude
    assert pytest.approx(dlat_60, rel=1e-12) == dlat_eq
