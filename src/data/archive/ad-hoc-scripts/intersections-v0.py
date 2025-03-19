import geopandas as gpd
from shapely.geometry import LineString
import time
import os


# create results directory if it doesn't exist
results_dir = "src/data/calculations/results"
os.makedirs(results_dir, exist_ok=True)

# load data. NOTE: ALL OF THIS USED TO BE GEOJSON SO NEED TO MAKE IT WORK W PARQUET
census_blocks_gdf = gpd.read_file("src/data/calculations/census-blocks.parquet", 
                                  columns=["OBJECTID", "geometry"]).to_crs(3857)
census_blocks_gdf["centroid"] = census_blocks_gdf.geometry.centroid

school_levels = {
    "high": gpd.read_file("src/data/calculations/school-locations/high-schools.csv",
                          columns=["ID", "Latitude", "Longtiude"]).to_crs(3857),
    "middle": gpd.read_file("src/data/calculations/school-locations/middle-schools.csv",
                            columns=["ID", "Latitude", "Longtiude"]).to_crs(3857),
    "elem": gpd.read_file("src/data/calculations/school-locations/elem-schools.csv",
                          columns=["ID", "Latitude", "Longtiude"]).to_crs(3857)
}

# don't need street geometry sicne we have ID
streets_gdf = gpd.read_file("src/data/calculations/streets.parquet",
                            columns=["ID","predicted_crashes_2022"]).to_crs(3857)

code_timing_results = []

# process each school level
for level_name, school_gdf in school_levels.items():
    start_time = time.time()

    #school_gdf = school_gdf.rename(columns={"geometry": f"geometry_{level_name}"})

    merged_gdf = census_blocks_gdf[['OBJECTID', 'centroid']].merge(
        school_gdf[['ID', f"geometry_{level_name}"]], how='cross'
    )

    merged_gdf['geometry'] = merged_gdf.apply(lambda row: LineString([row['centroid'], row[f"geometry_{level_name}"]]), axis=1)
    
    lines_gdf = gpd.GeoDataFrame(merged_gdf[['geometry', 'OBJECTID', 'ID']])
    lines_gdf = lines_gdf.rename(columns={'OBJECTID': 'census_block_id', 'ID': 'school_id'}).set_crs(3857)

    intersecting_streets = gpd.sjoin(streets_gdf, lines_gdf, how='inner', predicate='intersects')
    # don't save geometry column
    output_file = f"{results_dir}/intersecting_streets_{level_name}.geojson"
    intersecting_streets.to_file(output_file, driver='GeoJSON')

    end_time = time.time()
    duration = end_time - start_time
    print(f"Saved: {output_file} ({duration:.2f} seconds)")

    # record timing results
    timing_results.append(f"{level_name}: {duration:.2f} seconds")

# save timing results to file
timing_file = f"{results_dir}/timing_results.txt"
with open(timing_file, "w") as f:
    f.write("\n".join(code_timing_results))

print(f"Saved timing results to {timing_file}")