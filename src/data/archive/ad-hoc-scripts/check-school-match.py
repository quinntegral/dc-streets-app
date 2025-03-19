import csv
import json

csv_file_path = "src/data/map-assets/school-locations/elem-schools-and-zones.csv"
geojson_file_path = "src/data/map-assets/school-locations/elem-school-coords.geojson"

school_names = set()
with open(csv_file_path, newline="", encoding="utf-8-sig") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        school_name = row["School Name"].replace(" Middle School", "").replace(" Education Campus", "").replace(" Academy", "").strip().lower()
        school_names.add(school_name)

with open(geojson_file_path, encoding="utf-8") as geojson_file:
    geojson_data = json.load(geojson_file)

geojson_school_names = set(
    feature["properties"]["School Name"].replace(" Middle School", "").replace(" Education Campus", "").replace(" Academy", "").strip().lower()
    for feature in geojson_data["features"]
)

# find unmatched
matched_zones = geojson_school_names & school_names
unmatched_zones = geojson_school_names - school_names
unmatched_schools = school_names - geojson_school_names

print("\nMatched School Zones:", sorted(matched_zones))
print("\nUnmatched School Zones:", sorted(unmatched_zones))
print("\nUnmatched Schools", sorted(unmatched_schools))