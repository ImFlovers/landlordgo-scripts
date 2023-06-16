import requests
import json
import random
import time
import schedule
import os

url = "https://rewards.landlordgo.r10s.r5y.io"
headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru'
}

# tokens list
tokens = [
    "Bearer ",
    "Bearer ",
    # Add other tokens if necessary
]

# console clear
# os.system('cls' if os.name == 'nt' else 'clear')

def fetch_json(method, url, headers, data):
    response = requests.request(method, url, headers=headers, data=json.dumps(data))
    parsed = response.json()
    return parsed

def fetch_token(token):
    headers["Authorization"] = token
    response = fetch_json("GET", url + "/free-coins/ad-reward-token", headers, {})
    return response["token"]

def get_coins(token):
    data = {
        'token': token
    }
    return fetch_json("POST", url + '/free-coins/ad-reward-token/claim', headers, data)

def fetch_token_pride(token):
    headers["Authorization"] = token
    response = fetch_json("GET", url + "/free-influence/ad-reward-token", headers, {})
    return response["token"]

def get_pride(token):
    data = {
        'token': token
    }
    return fetch_json("POST", url + '/free-influence/ad-reward-token/claim', headers, data)

def get_boost(token):
    data = {
        'token': token
    }
    return fetch_json("POST", url + '/free-boost/claim', headers, data)

def get_rent(token):
    data = {
        'token': token
    }
    return fetch_json("POST", 'https://profit.landlordgo.r10s.r5y.io/rent', headers, data)

def get_chest_multi():
    return fetch_json("GET", 'https://chests.landlordgo.r10s.r5y.io/multi', headers, {})

def get_chest(id, reward_id, claim_cost):
    data = {
        'rewardId': reward_id,
        'claimCost': claim_cost
    }
    return fetch_json("POST", 'https://chests.landlordgo.r10s.r5y.io/multi/' + id, headers, data)

def fetch_double_rent_token(token):
    headers["Authorization"] = token
    response = fetch_json("GET", 'https://rewards.landlordgo.r10s.r5y.io/double-rent/ad-reward-token', headers, {})
    return response["token"]

def get_double_rent(token):
    data = {
        'token': token
    }
    return fetch_json("POST", 'https://rewards.landlordgo.r10s.r5y.io/double-rent/ad-reward-token/claim', headers, data)

def claim_rewards():
    status = []

    for token in tokens:
        try:
            token = token.strip()
            token = fetch_token(token)
            get_coins(token)
            get_boost(token)
            get_rent(token)
            status.append((len(status), True))
        except Exception as err:
            status.append((len(status), False))

        try:
            token = token.strip()
            token = fetch_token_pride(token)
            get_pride(token)
            status.append((len(status), True))
        except Exception as err:
            status.append((len(status), False))

        try:
            chests_data = get_chest_multi()

            for reward_id in chests_data['hiddenRewards']:
                get_chest(chests_data['id'], reward_id, chests_data['claimCost'][0]['type'])
            status.append((len(status), True))
        except Exception as err:
            status.append((len(status), False))

        try:
            token = token.strip()
            token = fetch_double_rent_token(token)
            get_double_rent(token)
            status.append((len(status), True))
        except Exception as err:
            status.append((len(status), False))

    return status

# automatic pick-up every hour 6 times
for i in range(100000):
    claim_rewards()
    time.sleep(120)  # wait n time