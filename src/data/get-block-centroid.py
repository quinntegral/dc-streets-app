import geopandas as gpd
import json

# get geojson featureCollection
with open("src/data/block-groups.geojson") as f:
    collection = json.load(f)

# convert featurecollection to geopandas
gdf = gpd.GeoDataFrame.from_features(collection["features"])

# get centroid of featurecollection
gdf["centroid"] = gdf.geometry.centroid

# add back to geojson as property
gdf["centroid"] = gdf["centroid"].apply(lambda point: [point.x, point.y])

for feature, centroid in zip(collection["features"], gdf["centroid"]):
    feature["properties"]["centroid"] = centroid

with open("src/data/block-groups-and-centroids.geojson", "w") as f:
    json.dump(collection, f)