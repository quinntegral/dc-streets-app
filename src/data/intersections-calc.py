import json
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, LineString

# get files & set CRS to 3857 for calc accuracy. current CRS is EPSG:4326
block_groups_gdf = gpd.read_file("src/data/block-groups.geojson",
                                 columns=["OBJECTID","geometry"]).to_crs(3857)
# i think high school gdf is using EPSG:4326
high_schools_gdf = gpd.read_file("src/data/high-schools-w-coords.geojson",
                                 columns=["School Name", "geometry"]).to_crs(3857)
streets_gdf = gpd.read_file("src/data/final-fixed-streets.geojson",
                            columns=["crash_count_2022", "geometry", "routename", "blockkey"]).to_crs(3857)

# calc centroids bc geopandas doesn't like point properties
block_groups_gdf["centroid"] = block_groups_gdf.geometry.centroid

# merge block groups & high schools and make lines
merged_gdf = block_groups_gdf[['OBJECTID', 'centroid']].merge(
    high_schools_gdf[['School Name', 'geometry']], how='cross'
)
merged_gdf['geometry'] = merged_gdf.apply(lambda row: LineString([row['centroid'], row['geometry']]), axis=1)

# line
lines_gdf = gpd.GeoDataFrame(merged_gdf[['geometry', 'OBJECTID', 'School Name']], crs=3857)
lines_gdf = lines_gdf.rename(columns={'OBJECTID': 'block_group_id', 'School Name': 'high_school_id'})

# spatial join w/ streets to find intersections
intersecting_streets = gpd.sjoin(streets_gdf, lines_gdf, how='inner', predicate='intersects')

# save results
intersecting_streets.to_file("src/data/intersecting_streets.geojson", driver='GeoJSON')