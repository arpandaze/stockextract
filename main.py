import json
import requests
from bs4 import BeautifulSoup
import datetime

API_TOKEN = 'lrvOK0nt8PySs9AG9NuRXjshPdkY5o02xMGQswjW3OZfP4B1yfDTeV5bs7Nf'
WTD_BASE_URL = "https://api.worldtradingdata.com/api/v1/stock"
WTD_HISTORY_BASE_URL = "https://api.worldtradingdata.com/api/v1/history"

CURRENCY_BASE_URL = "https://api.exchangeratesapi.io/latest"

ticker_names = [
                'S&P 500',
                'Nasdaq Comp',
                'Dow Jones',
                'Russell2000',
                'OSEBX',
                'OMXS30B',
                'Euro Stoxx 50',
                'DAX', 'CAC 40',
                'FTSE 100',
                'FTSE MIB',
                'IBEX 35',
                'PSI 20',
                'Nikkei 225',
                'KOSPI',
                'HANG SENG',
                'Bombay SENSEX',
                'CSI 300',
                'FTSE China A50',
                '3188 HK',
                'HSCEI',
                'The Big Four Kina',
                'Olje',
                'Kobber',
                'Aluminium',
                'Gull',
                'USDNOK',
                'EURNOK',
                'EURUSD',
                'USDJPY',
                'iShare High Yield',
                'US 10 Yr',
                'Trend Global',
                'Trend Europa',
                'Trend USA'
                ]

wtd_symbol = {
                'S&P 500':'^INX',
                'Nasdaq Comp':'^IXIC',
                'Dow Jones':'^DJI',
                'Russell2000':'^RUT',
                'OMXS30B':'^OMXS30',
                'Euro Stoxx 50':'SX5E',
                'DAX':'^DAX',
                'CAC 40':'^PX1',
                'FTSE 100':'^UKX',
                'FTSE MIB':'^FTSEMIB',
                'IBEX 35':'^IB',
                'PSI 20':'^PSI20',
                'Nikkei 225':'^NI225',
                'KOSPI':'KOSPI.KS',
                'HANG SENG':'^HSI',
                'Bombay SENSEX':'^SENSEX',
                'FTSE China A50':'^XIN9',
                '3188 HK':'3188.HK'
              }

def date(day):
    if(day == 'yesterday'):
        return str(datetime.datetime.now()-datetime.timedelta(days=1))[:10]
    elif(day == 'lastyear'):
        return str(datetime.datetime.now()-datetime.timedelta(days=365))[:10]
    elif(day == '' or day == 'today'):
        return str(datetime.datetime.now())[:10]
    else:
        return 'Error!'

def getValueFromYahoo(symbol):
    url = requests.get("https://finance.yahoo.com/quote/{}".format(symbol))
    soup = BeautifulSoup(url.content,features='lxml')
    header_block = soup.find_all(id='quote-header-info')[0].children
    text_block = list(header_block)[2].find_all('span')[0].get_text()
    return text_block

def getCurrentData(symbol):
    infos = {'symbol':symbol, 'api_token':API_TOKEN}
    api_requests = requests.get(WTD_BASE_URL,params=infos)
    try:
        return json.loads(api_requests.content)
    except:
        print("Unexpected Error #1")

def getCurrencyDataWithBase(base):
    infos = {'base':base}
    api_requests = requests.get(CURRENCY_BASE_URL,params=infos)
    try:
        return json.loads(api_requests.content)
    except:
        print("Unexpected Error #2")

def getCurrentCurrencyData():
    jsonFile = getCurrencyDataWithBase('NOK')
    EURNOK = 1/float(jsonFile['rates']['EUR'])
    USDNOK = 1/float(jsonFile['rates']['USD'])
    GBPNOK = 1/float(jsonFile['rates']['GBP'])
    EURUSD = float(EURNOK/USDNOK)
    USDJPY = USDNOK*float(jsonFile['rates']['JPY'])
    print(jsonFile)
    return ','.join((str(USDNOK),str(EURNOK),str(GBPNOK),str(EURUSD),str(USDJPY)))

print()