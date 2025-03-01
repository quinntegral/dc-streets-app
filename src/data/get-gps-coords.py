import csv
import requests
import urllib.parse

MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoicXVpbm50ZWdyYWwiLCJhIjoiY20ydzg2YmVsMDQyajJqcHdtMWFpeDkxZSJ9.aGne6BrJD-xknl274LKPVQ"
MAPBOX_GEOCODE_URL = "https://api.mapbox.com/search/geocode/v6/forward"

input_file = "src/data/dc-high-schools.csv"
output_file = "src/data/dc-high-schools-new.csv"

def get_coordinates(address):
    #encoded_address = urllib.parse.quote(address)
    #print(f"getting encoded address: {encoded_address}\n")
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
            print(f"API RESPONSE NAME: {data["features"][0]["properties"]["name"]}")
            return lat, lon
    return None, None

def process_csv():
    with open(input_file, newline='', encoding='utf-8') as infile, \
         open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        writer.writerow(["School Name", "Address", "Latitude", "Longitude"])
        
        for row in reader:
            school_name, address = row
            print(f"getting {address}\n")
            lat, lon = get_coordinates(address)
            print(f"{school_name}: {lat}, {lon}")
            writer.writerow([school_name, address, lat, lon])

if __name__ == "__main__":
    process_csv()