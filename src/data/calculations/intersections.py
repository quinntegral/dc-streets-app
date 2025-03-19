import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString, Point
import time
import os

# create results dir if it doesn't exist
results_dir = "src/data/calculations/results"
os.makedirs(results_dir, exist_ok=True)

# load big files
streets_gdf = gpd.read_parquet("src/data/calculations/streets.parquet",
                               columns=["StreetID", "predicted_crashes_2022", "geometry"]).to_crs(3857)

census_blocks_gdf = gpd.read_parquet("src/data/calculations/census-blocks.parquet",
                                     columns=["OBJECTID", "geometry"]).to_crs(3857)
census_blocks_gdf["centroid"] = census_blocks_gdf.geometry.centroid

# load school locations from CSV, create GDFs
def load_school_csv(filepath):
    df = pd.read_csv(filepath, usecols=["SchoolID", "Latitude", "Longitude"])
    df["geometry"] = df.apply(lambda row: Point(row["Longitude"], row["Latitude"]), axis=1)
    # return gpd.GeoDataFrame(df, geometry="geometry", crs=4326).to_crs(3857)
    return gpd.GeoDataFrame(df, geometry="geometry", crs=3857)

school_levels = {
    "high": load_school_csv("src/data/calculations/school-coords/high-schools.csv"),
    "middle": load_school_csv("src/data/calculations/school-coords/middle-schools.csv"),
    "elem": load_school_csv("src/data/calculations/school-coords/elem-schools.csv")
}

code_timing_results = []

# process school levels
for level_name, school_gdf in school_levels.items():
    start_time = time.time()

    # census block and school combinations
    merged_gdf = census_blocks_gdf[['OBJECTID', 'centroid']].merge(
        school_gdf[['SchoolID', 'geometry']], how='cross'
    )
    # naive routing approach: draw lines for all census block & school combos
    merged_gdf['geometry'] = merged_gdf.apply(lambda row: LineString([row['centroid'], row['geometry']]), axis=1)
    
    lines_gdf = gpd.GeoDataFrame(merged_gdf[['OBJECTID', 'SchoolID', 'geometry']], crs=3857)
    lines_gdf = lines_gdf.rename(columns={'OBJECTID': 'census_block_id', 'SchoolID': 'school_id'})

    # join on intersecting street & line combos
    intersecting_streets = gpd.sjoin(streets_gdf, lines_gdf, how='inner', predicate='intersects')
    intersecting_streets = intersecting_streets.drop(columns=['geometry'])

    # save results (GeoParquet instead of GeoJSON for efficiency)
    output_file = f"{results_dir}/intersections_{level_name}.parquet"
    intersecting_streets.to_parquet(output_file)

    end_time = time.time()
    duration = end_time - start_time
    print(f"Saved: {output_file} ({duration:.2f} seconds)")

    # record timing results
    code_timing_results.append(f"{level_name}: {duration:.2f} seconds")

# Save timing results to file
timing_file = f"{results_dir}/timing_results.txt"
with open(timing_file, "w") as f:
    f.write("\n".join(code_timing_results))

print(f"Saved timing results to {timing_file}")