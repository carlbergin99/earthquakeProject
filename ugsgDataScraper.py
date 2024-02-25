# Use ugsg API to get earthquake data from the US

import requests
import pandas as pd

def fetch_earthquake_data():
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2024-02-23&endtime=2024-02-24"
    response = requests.get(url)
    earthquake_data = response.json()

    # Initialize a list to hold the earthquake data
    earthquake_list = []

    # Iterate through each earthquake event in the fetched data
    for earthquake in earthquake_data['features']:
        # Extract relevant information for each earthquake
        id = earthquake['id']
        magnitude = earthquake['properties']['mag']
        place = earthquake['properties']['place']
        time = earthquake['properties']['time']
        longitude = earthquake['geometry']['coordinates'][0]
        latitude = earthquake['geometry']['coordinates'][1]
        depth = earthquake['geometry']['coordinates'][2]

        # Append the extracted information to the list
        earthquake_list.append([id, magnitude, place, time, longitude, latitude, depth])

    # Convert the list into a pandas DataFrame
    columns = ['ID', 'Magnitude', 'Place', 'Time', 'Longitude', 'Latitude', 'Depth']
    earthquake_df = pd.DataFrame(earthquake_list, columns=columns)

    # Convert Time from UNIX timestamp (milliseconds) to a readable format
    earthquake_df['Time'] = pd.to_datetime(earthquake_df['Time'], unit='ms')

    print(earthquake_data)
    return earthquake_df


test = fetch_earthquake_data()