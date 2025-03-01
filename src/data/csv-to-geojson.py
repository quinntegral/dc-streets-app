import csv
import json
from shapely import wkt
from shapely.geometry import mapping

# Initialize a list to hold GeoJSON features
features = []

# Open and read the CSV file
with open('src/data/fixed-streets-with-linestring.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        geom = wkt.loads(row['geom_wkt'])
        properties = {key: value for key, value in row.items() if key not in ['geom_wkt','geom']}
        
        # Create a feature with geometry and properties
        feature = {
            'type': 'Feature',
            'geometry': mapping(geom),
            'properties': properties
        }
        features.append(feature)

# Create a FeatureCollection
feature_collection = {
    'type': 'FeatureCollection',
    'features': features
}

# Write the FeatureCollection to a GeoJSON file
with open('src/data/final-fixed-streets.json', 'w') as f:
    json.dump(feature_collection, f, indent=1)