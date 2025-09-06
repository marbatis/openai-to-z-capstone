Given this area of interest (WGS84 bounding box) and mission list,
suggest 3–5 publicly downloadable scenes/tiles with IDs and links, suitable for canopy-penetrating
or canopy-informative analysis. Return JSON with fields: source_type, id, url, reason.
AOI: {{min_lon}}, {{min_lat}}, {{max_lon}}, {{max_lat}}
Missions: Sentinel-2, Landsat-8/9, GEDI, OpenTopography LiDAR
Constraints: Week-long temporal spread; minimal cloud cover; native resolution preferred.
