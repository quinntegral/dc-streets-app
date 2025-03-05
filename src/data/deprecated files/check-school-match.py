import csv
import json

csv_file_path = "src/data/dc-elem-schools.csv"
geojson_file_path = "src/data/dc-elem-school-zones.geojson"

# load elementary school names from CSV
school_names = set()
school_zones_from_csv = set()
with open(csv_file_path, newline="", encoding="utf-8-sig") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        school_name = row["School Name"].replace(" Elementary School", "").replace(" Education Campus", "").replace(" Bilingual School", "").strip().lower()
        school_names.add(school_name)
        school_zone_from_csv = row["School Zone"].strip().lower()
        school_zones_from_csv.add(school_zone_from_csv)

# load school zones from GeoJSON
with open(geojson_file_path, encoding="utf-8") as geojson_file:
    geojson_data = json.load(geojson_file)

geojson_school_names = set(
    feature["properties"]["NAME"].replace(" Elementary School", "").replace(" Education Campus", "").strip().lower()
    for feature in geojson_data["features"]
)

# find unmatched **zones** (zones with no matching school in the CSV)
# matched_zones = geojson_school_names & school_names
# unmatched_zones = geojson_school_names - school_names
unmatched_schools = school_names - geojson_school_names
unmatched_zones = geojson_school_names - school_zones_from_csv

# print(f"\n{school_zones_from_csv}")

# print("\nMatched School Zones:", sorted(matched_zones))
print("\nUnmatched School Zones:", sorted(unmatched_zones))
#print("\nUnmatched Schools", sorted(unmatched_schools))