import json
import geopandas as gpd
import pandas as pd
from shapely import wkb

# Load JSON file
with open("src/data/calculations/full-final-streets.json", "r") as f:
    data = json.load(f)

# Convert JSON to DataFrame
df = pd.DataFrame(data)

# Convert EWKB binary geometry to a Shapely geometry
df["geometry"] = df["geom"].apply(wkb.loads)

# Create a GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")

# Drop unnecessary columns
gdf = gdf.drop(columns=["geom", "geom_wkt"])

# Save as GeoJSON
gdf.to_file("src/data/final-streets.geojson", driver="GeoJSON")

print("GeoJSON file created successfully!")