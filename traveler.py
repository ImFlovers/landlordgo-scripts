import requests
import datetime
import math
import requests
import schedule
import time
import os
from colorama import init, Fore, Back, Style
init(autoreset=True)

# Setting headers for authorization
headers = {
    "Authorization": "Bearer "
}

# Cleaning the console at startup
os.system('cls' if os.name == 'nt' else 'clear')

# Getting Travel data
url_journey = "https://agent.landlordgo.r10s.r5y.io/v2"
response_journey = requests.get(url_journey, headers=headers)

# Checking the response status and repeating the request in case of an error
while response_journey.status_code != 200:
    print("Error fetching journey data, retrying...")
    response_journey = requests.get(url_journey, headers=headers)

# Getting travel data in the form of a dictionary
journey_data = response_journey.json()

# Getting the date and time of arrival from the travel data
arrival_str = journey_data["arrivalDate"][:-1]
arrival_utc = datetime.datetime.fromisoformat(arrival_str)

# Getting the current date and time in UTC format
now_utc = datetime.datetime.utcnow()

# Calculating the remaining time until arrival
time_remaining = arrival_utc - now_utc

# Calculation of the number of times to activate acceleration
num_activations = math.ceil(time_remaining.total_seconds() / 3600)

# Output of information for debugging
# print("Journey data:", journey_data)
# print("Time remaining:", time_remaining)
# print("Number of activations:", num_activations)

# URL for getting the acceleration token
url_token = "https://agent.landlordgo.r10s.r5y.io/v2/speed-up/advert/ad-reward-token"

# URL to activate acceleration
url_activate = "https://agent.landlordgo.r10s.r5y.io/v2/speed-up/advert/ad-reward-token/claim"

# Function to perform acceleration
def speed_up():
    # Getting travel data
    response_journey = requests.get(url_journey, headers=headers)
    journey_data = response_journey.json()

    # Getting arrival date and time from travel data
    arrival_str = journey_data["arrivalDate"][:-1]
    arrival_utc = datetime.datetime.fromisoformat(arrival_str)

    # Getting the current date and time in UTC format
    now_utc = datetime.datetime.utcnow()

    # Calculating the remaining time until arrival
    time_remaining = arrival_utc - now_utc

    # Calculation of the number of times you need to activate acceleration
    num_activations = math.ceil(time_remaining.total_seconds() / 3600)

    # Activating acceleration the right number of times
    for i in range(num_activations):
        # Executing a request to get an acceleration token
        while True:
            response_token = requests.get(url_token, headers=headers)
            if response_token.status_code == 200:
                break

        # Getting a token from a response
        token = response_token.json()["token"]

        # Executing a request to activate acceleration using the received token
        data = {
            "token": token
        }
        response_activate = requests.post(url_activate, headers=headers, json=data)

        # Output of the response for debugging
        print(Fore.BLUE + "=" * 50)
        print(f"{Fore.LIGHTMAGENTA_EX}Response: {Fore.WHITE}" + str(response_activate.json()))
        print(Fore.BLUE + "=" * 50)
        
        # clearing the console from the flood
        #  time.sleep(0.8)
        # os.system('cls' if os.name == 'nt' else 'clear')

# Starting acceleration before arrival every 10 seconds
while True:
    speed_up()
    time.sleep(10)