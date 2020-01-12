import requests
import json


def
url = 'https://api.worldtradingdata.com/api/v1/stock'
params = {
  'symbol': '^DJI',
  'api_token': 'lrvOK0nt8PySs9AG9NuRXjshPdkY5o02xMGQswjW3OZfP4B1yfDTeV5bs7Nf'
}
response = requests.request('GET', url, params=params)
print(response.json())