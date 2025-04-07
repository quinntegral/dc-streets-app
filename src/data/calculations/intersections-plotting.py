import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString, Point
import os
import matplotlib.pyplot as plt

# create results dir if it doesn't exist
results_dir = "src/data/calculations/results"
os.makedirs(results_dir, exist_ok=True)

# load big files
streets_gdf = gpd.read_parquet("src/data/calculations/streets.parquet",
                               columns=["StreetID", "predicted_crashes_2022", "geometry"]).to_crs(3857)
streets_sample = streets_gdf.sample(frac=0.5, random_state=31)

census_blocks_gdf = gpd.read_parquet("src/data/calculations/census-blocks.parquet",
                                     columns=["OBJECTID", "geometry"]).to_crs(3857)
census_blocks_gdf["centroid"] = census_blocks_gdf.geometry.centroid
census_blocks_sample = census_blocks_gdf.sample(frac=0.0005, random_state=31)

# load school locations from CSV, create GDFs
def load_school_csv(filepath):
    df = pd.read_csv(filepath, usecols=["SchoolID", "Latitude", "Longitude"])
    df["geometry"] = df.apply(lambda row: Point(row["Longitude"], row["Latitude"]), axis=1)
    return gpd.GeoDataFrame(df, geometry="geometry", crs=4326).to_crs(3857)
    # return gpd.GeoDataFrame(df, geometry="geometry", crs=3857)

# just one highschool
school_levels = {
    "high": load_school_csv("src/data/calculations/school-coords/dummy-hs.csv")
}

# process school levels
for level_name, school_gdf in school_levels.items():

    # census block and school cross-merge
    merged_gdf = census_blocks_sample[['OBJECTID', 'centroid']].merge(
        school_gdf[['SchoolID', 'geometry']], how='cross'
    )
    # naive routing: draw lines for all census block & school combos
    merged_gdf['geometry'] = merged_gdf.apply(lambda row: LineString([row['centroid'], row['geometry']]), axis=1)
    lines_gdf = gpd.GeoDataFrame(merged_gdf[['OBJECTID', 'SchoolID', 'geometry']], crs=3857)
    lines_gdf = lines_gdf.rename(columns={'OBJECTID': 'census_block_id', 'SchoolID': 'school_id'})

    # join on intersecting street & line combos
    intersecting_streets = gpd.sjoin(streets_sample, lines_gdf, how='inner', predicate='intersects')
    intersecting_streets = intersecting_streets.drop(columns=['geometry'])

    # save results (GeoParquet for efficiency)
    # output_file = f"{results_dir}/intersections_{level_name}.parquet"
    # intersecting_streets.to_parquet(output_file)

# PLOTTING
fig, ax = plt.subplots(figsize=(10, 8))
streets_sample.plot(ax=ax, color="gray", linewidth=0.5, alpha=0.7, label="Streets sample")
census_blocks_sample.set_geometry("centroid").plot(ax=ax, color="purple", markersize=50, label="Census Block Centroids sample")
school_gdf = school_levels["high"]
school_gdf.plot(ax=ax, color="green", markersize=50, label="Anacostia High School")
lines_gdf.plot(ax=ax, color="blue", linewidth=1, linestyle="dashed", label="Lines")

intersecting_streets_gdf = streets_gdf[streets_gdf["StreetID"].isin(intersecting_streets["StreetID"])]
intersecting_streets_gdf.plot(ax=ax, color="red", linewidth=1.5, label="Intersecting Streets w/ Lines")

plt.title("Census Block to School Connections")
plt.legend()
plt.show()