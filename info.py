import requests
import datetime
import math
import requests
import schedule
import time
import sys
import os
import json
from colorama import init, Fore, Back, Style

init(autoreset=True)

# Setting headers for authorization
headers = {
    "Authorization": "Bearer "
}


# Constants for URLs
URL_PROFILE = "https://player.landlordgo.r10s.r5y.io/profile/{write ur accound id}"
URL_BALANCE = "https://player.landlordgo.r10s.r5y.io/?playerId={write ur accound id}"
URL_CATEGORIES = "https://category-trends.landlordgo.r10s.r5y.io/v2"
URL_TRADING = "https://stock-exchange.landlordgo.r10s.r5y.io/price-graph/coin/influence/sell"

#Basic garbage

def get_profile_info():
    """
    Getting User profile information
    """
    # executing a request for profile data
    response = requests.get(URL_PROFILE, headers=headers)
    # getting profile data in the form of a dictionary
    profile_data = response.json()
    print_profile_info(profile_data)
    
def get_balance_info():
    """
    Getting information about the user's balance
    """
    # executing a request to get balance data
    response = requests.get(URL_BALANCE, headers=headers)
    # getting balance data in the form of a dictionary
    balance_data = response.json()["balance"]
    print_balance_info(balance_data)

def get_category_info():
    """
    Getting information about categories
    """
    # executing a request for profile data
    response = requests.get(URL_CATEGORIES, headers=headers)
    # getting profile data in the form of a dictionary
    category_info = response.json()
    print_category_info(category_info)

def get_trade_info():
    """
    Getting information about the Influence course
    """
    # executing a request for profile data
    response = requests.get(URL_TRADING, headers=headers)
    # getting profile data in the form of a dictionary
    trade_info = response.json()
    print_trade_info(trade_info)

def print_profile_info(profile_data):
    """
    Output of user profile information to the console
    """
    print(Fore.BLUE + "=" * 50)
    print(f"{Fore.MAGENTA}{Style.BRIGHT}{'User Information':^50}")
    print(Fore.BLUE + "=" * 50)
    print(f"{Fore.LIGHTMAGENTA_EX}{'Name:':<2} {Fore.WHITE}{profile_data['name']}")
    print(f"{Fore.LIGHTMAGENTA_EX}{'LVL:':<2} {Fore.WHITE}{profile_data['level']}")
    print(f"{Fore.LIGHTMAGENTA_EX}{'The Cost of an Empire:':<2} {Fore.WHITE}{profile_data['empireValue']}")
    print(f"{Fore.LIGHTMAGENTA_EX}{'playerID:':<2} {Fore.WHITE}{profile_data['playerID']}\n")

def print_balance_info(balance_data):
    """
    Output of information about the user's balance to the console
    """
    print(Fore.BLUE + "=" * 50)
    print(f"{Fore.MAGENTA}{Style.BRIGHT}{'Balance Information':^50}")
    print(Fore.BLUE + "=" * 50)
    print(f"{Fore.LIGHTMAGENTA_EX}{'Money:':<2} {Fore.WHITE}{balance_data['cash']}")
    print(f"{Fore.LIGHTMAGENTA_EX}{'Gold:':<2} {Fore.WHITE}{balance_data['coins']}")
    print(f"{Fore.LIGHTMAGENTA_EX}{'Influence:':<2} {Fore.WHITE}{balance_data['influence']}\n")

def print_trade_info(trade_info):
    """
    Output of information about the Influence course
    """
    print(Fore.BLUE + "=" * 50)
    print(f"{Fore.MAGENTA}{Style.BRIGHT}{'Information on the Influence course':^50}")
    print(Fore.BLUE + "=" * 50)
    for value in trade_info["values"][-2:]:
        print(f"{Fore.LIGHTMAGENTA_EX}{'Exchange rate coin --> influence:':<2} {Fore.BLUE}{value['exchangeRateInTime']['exchangeRate']}")
        print(f"{Fore.LIGHTMAGENTA_EX}{'Profit from the exchange:':<2} {Fore.GREEN}{value['exchangeProfit']['amount']} influence")
        print(Fore.BLUE + "-" * 50)

def print_category_info(categories_data):
    """
    Output information about categories to the console
    """
    print(Fore.BLUE + "=" * 50)
    print(f"{Fore.MAGENTA}{Style.BRIGHT}{'Information by Category':^50}")
    print(Fore.BLUE + "=" * 50)
    print(f"{Fore.LIGHTMAGENTA_EX}{'Current category:':<2} {Fore.WHITE}{categories_data['current']['categoryName']}")
    print(f"{Fore.LIGHTMAGENTA_EX}{'End time of the current category:':<2} {Fore.RED}{categories_data['current']['endTime']}")
    print(f"{Fore.LIGHTMAGENTA_EX}{'Trend of the current category:':<2} {Fore.GREEN}{categories_data['current']['trend']}%")
    print(Fore.BLUE + "=" * 50)
    print(f"{Fore.MAGENTA}{Style.BRIGHT}{'What is next by category?':^50}")
    print(Fore.BLUE + "=" * 50)
    if categories_data["next"]:
        print(f"{Fore.MAGENTA}{Style.BRIGHT}{'Category after the current one:':<2} {Fore.BLUE}{categories_data['next'][0]['categoryName']}")
    else:
        print(Fore.RED + "The next category is not defined...")
    print(Style.RESET_ALL)
{Fore.WHITE}
while True:
    try: 
        # clearing the console
        os.system('cls' if os.name == 'nt' else 'clear')

        get_profile_info()
        get_balance_info()
        get_trade_info()
        get_category_info()

    except Exception as e:
        print(Fore.RED + "Ошибка:", e)

    # delay by N seconds
    time.sleep(12)