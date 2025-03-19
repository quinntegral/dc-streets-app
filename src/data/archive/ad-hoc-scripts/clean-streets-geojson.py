import geopandas as gpd

# Input and output file paths
input_file = 'src/data/all-streets-data.geojson'
output_parquet = 'src/data/street-scores-v1.parquet'
output_geojson = 'src/data/all-streets-cleaned.geojson'

def convert_geojson():
    gdf = gpd.read_file(input_file)

    gdf = gdf[['routename','predicted_crashes_2022', 'crash_count_2022', 'geometry']]

    gdf['ID'] = gdf.index

    gdf = gdf[["ID", "routename", 'predicted_crashes_2022', 'crash_count_2022', 'geometry']]

    gdf.to_parquet(output_parquet, index=False)
    print(f"Converted to Parquet: {output_parquet}")

    gdf.to_file(output_geojson, driver='GeoJSON')
    print(f"Updated GeoJSON: {output_geojson}")

if __name__ == "__main__":
    convert_geojson()
