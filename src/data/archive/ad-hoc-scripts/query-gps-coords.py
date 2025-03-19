import csv
import requests
import urllib.parse

MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoicXVpbm50ZWdyYWwiLCJhIjoiY20ydzg2YmVsMDQyajJqcHdtMWFpeDkxZSJ9.aGne6BrJD-xknl274LKPVQ"
MAPBOX_GEOCODE_URL = "https://api.mapbox.com/search/geocode/v6/forward"

input_file = "src/data/calculations/school-locations/middle-schools.csv"
output_file = "src/data/calculations/school-locations/middle-schools-new.csv"

def get_coordinates(address):
    encoded_address = urllib.parse.quote(address)
    params = {
        "q": address,
        "access_token": MAPBOX_ACCESS_TOKEN
    }
    response = requests.get(MAPBOX_GEOCODE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if "features" in data and data["features"]:
            lon = data["features"][0]["properties"]["coordinates"]["longitude"]
            lat = data["features"][0]["properties"]["coordinates"]["latitude"]
            print(f"API RESPONSE NAME: {data['features'][0]['properties']['name']}")
            return lat, lon
    else:
        print(f"RESPONSE ERROR: {response.status_code} - {response.text}")
    return None, None

def process_csv():
    with open(input_file, newline='', encoding='utf-8') as infile, \
         open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        headers = next(reader)
        
        # Check for 'ID' column, add if missing
        if 'ID' not in headers:
            headers.insert(0, 'ID')

        # Write the new headers with Latitude and Longitude
        writer.writerow(headers + ["Latitude", "Longitude"])

        for i, row in enumerate(reader, start=1):
            # Add ID if missing
            if len(row) == len(headers) - 1:
                row.insert(0, i)

            school_name = row[1]  # Adjust for added ID column
            address = row[2]
            print(f"GETTING ADDRESS ({address}) OF {school_name}")
            lat, lon = get_coordinates(address)
            print(f"FOUND COORDINATES ({lat}, {lon})\n")

            writer.writerow(row + [lat, lon])

if __name__ == "__main__":
    process_csv()
