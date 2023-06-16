import os
import json
import requests
import numpy as np
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.exceptions import RequestException
import threading
import random

# Set headers for authorization
headers = {
    "Authorization": "Bearer "
}

# Configure parameters for making requests
session = requests.Session()
retry = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# Create a list of coordinates with random values
coordinates = [(str(random.uniform(0.0, 90.0)), str(random.uniform(0.0, 90.0))) for _ in range(55000)]

# URLs for requests
venues_url = "https://venues.landlordgo.r10s.r5y.io/nearby?latitude={}&longitude={}"
property_url = "https://portfolio.landlordgo.r10s.r5y.io/property/state/view?id={}"

# Function to make a request and get venues data
def get_venues_data(lat, lng):
    try:
        response = session.get(venues_url.format(lat, lng), headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error getting data for coordinates ({lat}, {lng})')
    except RequestException as e:
        print(f'Error making a request for coordinates ({lat}, {lng}): {str(e)}')
    return None

# Function to make a request and get property statistics
def get_property_statistics(property_id):
    try:
        response = session.get(property_url.format(property_id), headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error getting statistics for property with ID {property_id}')
    except RequestException as e:
        print(f'Error making a request for property with ID {property_id}: {str(e)}')
    return {}

# Create an empty dictionary to store venues data
venues_data_dict = {}
venues_data_lock = threading.Lock()

# Function to process completed tasks
def process_completed_task(future):
    result = future.result()
    if result:
        with venues_data_lock:
            for venue in result:
                property_id = venue.get("id")
                if property_id not in venues_data_dict:
                    venues_data_dict[property_id] = venue

# Create a thread pool to make requests in multiple threads
with ThreadPoolExecutor(max_workers=50) as executor:
    futures = []
    # Iterate through all coordinates and send requests to get nearby venues
    for lat, lng in coordinates:
        future = executor.submit(get_venues_data, lat, lng)
        future.add_done_callback(process_completed_task)
        futures.append(future)

    # Process the results of requests as they complete
    for future in tqdm(as_completed(futures), total=len(futures), desc='Fetching venues data'):
        pass

# Convert the dictionary to a list of venues data
venues_data = list(venues_data_dict.values())

# Sort venues data in descending order based on remaining_shares
venues_data.sort(key=lambda x: x.get("remaining_shares", 0), reverse=True)

# Save the data to a file
with open('venues_data.json', 'w', encoding='utf-8') as f:
    json.dump(venues_data, f, ensure_ascii=False, indent=4)

# List to store property statistics
statistics = []
statistics_lock = threading.Lock()

# Function to process property statistics
def process_property(venue):
    property_id = venue.get("id")
    name_property = venue.get("name")
    name_id = venue.get("category", {}).get("nameID")
    latitude = venue.get("location", {}).get("latitude")
    longitude = venue.get("location", {}).get("longitude")

    if property_id and name_id:
        statistics_data = get_property_statistics(property_id)
        if statistics_data:
            owned_view = statistics_data.get(property_id, {}).get("ownedView", {})
            max_shares = owned_view.get("maxShares", 0)
            bought_shares = owned_view.get("boughtShares", 0)
            remaining_shares = max_shares - bought_shares

            level_up = statistics_data.get(property_id, {}).get("levelUp", {}).get("Finished", {})
            tier = level_up.get("tier")

            with statistics_lock:
                statistics.append({
                    "name_property": name_property,
                    "id": property_id,
                    "name_id": name_id,
                    "tier": tier,
                    "latitude": latitude,
                    "longitude": longitude,
                    "max_shares": max_shares,
                    "bought_shares": bought_shares,
                    "remaining_shares": remaining_shares,
                })
        else:
            print(f'Error getting statistics for property with ID {property_id}')

# Create a thread pool to process property statistics
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = []
    # Iterate through venues data and submit tasks to process property statistics
    for venue in venues_data:
        future = executor.submit(process_property, venue)
        futures.append(future)

    # Process the results of tasks as they complete
    for future in tqdm(as_completed(futures), total=len(futures), desc='Processing property statistics'):
        pass

# Save property statistics to a file
with open('statistics.json', 'w', encoding='utf-8') as f:
    sorted_statistics = sorted(statistics, key=lambda x: x["remaining_shares"], reverse=True)
    json.dump(sorted_statistics, f, ensure_ascii=False, indent=4)

print('Data successfully written to files.')
