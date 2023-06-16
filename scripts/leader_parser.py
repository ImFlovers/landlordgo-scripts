import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import os

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

# Send a request to the server and get JSON data
url = 'https://leaderboard.landlordgo.r10s.r5y.io/lgo/api/v1.0/player_position?type=all'
response = session.get(url, headers=headers, timeout=10)
data = json.loads(response.text)

# Clear the console
os.system('cls' if os.name == 'nt' else 'clear')

# Create an empty list to store player data
players_data = []

# Create a thread pool for making requests in multiple threads
with ThreadPoolExecutor(max_workers=50) as executor:
    # Iterate through the ranking and send requests to retrieve player profiles
    futures = [executor.submit(session.get, f'https://player.landlordgo.r10s.r5y.io/profile/{player["player"]["id"]}', headers=headers, timeout=10) for player in data['ranking']]

    # Process the results of the requests
    for future in tqdm(futures, total=len(futures), desc='Fetching player profiles'):
        response = future.result()
        if response.status_code == 200:
            player_data = json.loads(response.text)
            players_data.append(player_data)
        else:
            print('Player profile not found')

# Save player data to a file
with open('dump.json', 'w', encoding='utf-8') as f:
    json.dump(players_data, f, indent=4, ensure_ascii=False)

print('Player data saved to players_data.json file')
