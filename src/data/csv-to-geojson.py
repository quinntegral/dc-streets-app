import csv
import json
from shapely import wkt
from shapely.geometry import mapping
import geopandas as gpd
import pandas as pd

# FIX THIS
# use geopandas to convert from csv to geojson
df = pd.read_csv("src/data/fixed-streets-with-linestring.csv")
df.to_file("src/data/final-fixed-streets.geojson", driver='GeoJSON')

# features = []

# with open('src/data/fixed-streets-with-linestring.csv', newline='') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         geom = wkt.loads(row['geom_wkt'])
#         properties = {key: value for key, value in row.items() if key not in ['geom_wkt','geom']}
        
#         feature = {
#             'type': 'Feature',
#             'geometry': mapping(geom),
#             'properties': properties
#         }
#         features.append(feature)

# feature_collection = {
#     'type': 'FeatureCollection',
#     'features': features
# }

# with open('src/data/final-fixed-streets.json', 'w') as f:
#     json.dump(feature_collection, f, indent=1)