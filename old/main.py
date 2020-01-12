import json
import requests
import datetime

SAPI_TOKEN = "Tpk_eb3e0daef86247048427e83fb5c2ede6"
API_TOKEN = "pk_f1b496ecb58f4a0899b852387232de43"
ACCOUNT_NO = "e70f30abda8214d4b9aaf8e1123516a2"
SECRET = "Tsk_95821557e2ea49ccb2dd8e837aa56b84"

BASE_URL = "https://cloud.iexapis.com"
SBASE_URL = "https://sandbox.iexapis.com"
ticker = '.INX'

lastYearDate = str(datetime.datetime.now()-datetime.timedelta(days=366))[:10].replace("-","")


def currentStockData(BASE_URL,ticker,API_TOKEN):
    api_request = requests.get("{}/stable/stock/{}/quote?token={}".format(BASE_URL,ticker,API_TOKEN))
    return api_request.content

def historicalStockData(BASE_URL,ticker,date,API_TOKEN):
    api_request = requests.get("{}/stable/stock/{}/chart/date/{}?token={}&chartByDay=true".format(BASE_URL,ticker,date,API_TOKEN))
    return api_request.content

def currentForexData(BASE_URL,symbol,API_TOKEN):
    api_request = requests.get("{}/stable/fx/latest?symbols={}&token={}".format(BASE_URL,symbol,API_TOKEN))
    return api_request.content

def historicalForexData(BASE_URL,symbol,date,API_TOKEN):
    api_request = requests.get("{}/stable/fx/historical?symbols={}&on={}&token={}".format(BASE_URL,symbol,date,API_TOKEN))
    return api_request.content

a = currentStockData(BASE_URL,ticker,API_TOKEN)
print(a)
json_file = json.loads(a)
print(json_file)