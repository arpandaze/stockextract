import json
import requests
from bs4 import BeautifulSoup
import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

API_TOKEN = 'iqp1xrePcCdLNDWQLEagN517asfLpU6Mqo2KrcMAtkGa77yyHFa2GI6IZDXn'
WTD_BASE_URL = "https://api.worldtradingdata.com/api/v1/stock"
WTD_HISTORY_BASE_URL = "https://api.worldtradingdata.com/api/v1/history"

ticker_names = [
                'S&P 500',
                'Nasdaq Comp',
                'Dow Jones',
                'Russell2000',
                'OSEBX',
                'OMXS30B',
                'Euro Stoxx 50',
                'DAX',
                'CAC 40',
                'FTSE 100',
                'FTSE MIB',
                'IBEX 35',
                'PSI 20',
                'Nikkei 225',
                'KOSPI',
                'HANG SENG',
                'Bombay SENSEX',
                'CSI 300',
                'Shanghai Composite',
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
                'GBPNOK',
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
                'Euro Stoxx 50':'^SX5E',
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

yahoo_symbol = {
                'Shanghai Composite':'000001.SS',
                'CSI 300':'000300.SS',
                'HSCEI':'^HSCE',
                'OSEBX':'OSEBX.OL',
                'iShare High Yield':'HYG',
                'US 10 Yr':'^TNX',
                'USDNOK':'USDNOK=X',
                'USDJPY':'USDJPY=X',
                'EURUSD':'EURUSD=X',
                'GBPNOK':'GBPNOK=X',
                'EURNOK':'EURNOK=X',
                'Gull':'GC=F'
               }

bloomberg_symbol = {
                        'Trend Global':'TRENDEN:NO',
                        'Trend Europa':'TRENDEU:NO',
                        'Trend USA':'TRENDUS:NO',
                        'Olje':'CO1:COM',
                        'Kobber':'LMCADS03:COM',
                        'Aluminium':'LMAHDS03:COM'
                   }

def date(day):
    if(day == 'yesterday'):
        return str(datetime.datetime.now()-datetime.timedelta(days=1))[:10]
    elif(day == 'lastyear'):
        return str(datetime.datetime.now()-datetime.timedelta(days=365))[:10]
    elif(day == 'yearstart'):
        return str(datetime.datetime.now())[0:4]+'-01-01'
    elif(day == '' or day == 'today'):
        return str(datetime.datetime.now())[:10]
    else:
        return 'Error!'

def getDataFromYahoo(symbol):
    try:
        return_data = {}
        url = requests.get("https://finance.yahoo.com/quote/{}".format(symbol))
        soup = BeautifulSoup(url.content,features='lxml')
        header_block = list(soup.find_all(id='quote-header-info')[0].children)
        price_text = header_block[2].find_all('span')[0].get_text()
        day_change_block = header_block[2].find_all('span')[1].get_text()
        percent_day_change = str(float(day_change_block[day_change_block.index('(')+1:day_change_block.index(')')-1]))
        return_data = {'price':price_text, 'change_pct':percent_day_change}
        return return_data
    except:
        print('Error while getting data from yahoo!')
        return ''

def getBloombergData(ticker_name):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options,executable_path=r'webdriver.exe')
    driver.get("https://www.bloomberg.com/quote/{}".format(bloomberg_symbol[ticker_name]))
    raw_html = str(driver.page_source.encode("utf-8"))
    driver.close()
    soup = BeautifulSoup(raw_html,'lxml')
    textBlock = soup.find_all('span',string='{}'.format(bloomberg_symbol[ticker_name]))
    valueDataBlock = textBlock[0].find_parent('section').findNext('section').find_all('span')
    currentValue = valueDataBlock[0].get_text().replace(',','')
    changePercent = str(float(valueDataBlock[3].get_text()[:-1]))
    try:
        ytdValue=soup.find_all('span',string='YTD Return')[0].nextSibling.get_text()
        ytdValue=str(float(ytdValue[:-1]))
    except:
        ytdValue=''
    try:
        oneYearReturnValue=soup.find_all('span',string='1 Year Return')[0].nextSibling.get_text()
        oneYearReturnValue=str(float(oneYearReturnValue[:-1]))
    except:
        oneYearReturnValue=''

    returnJSON = {bloomberg_symbol[ticker_name]:{date('today'):{'price':currentValue,'day_change':changePercent, 'year_change':oneYearReturnValue, 'ytd_change':ytdValue}}}
    return returnJSON

def getCurrentDataFromWTC(symbol):
    infos = {'symbol':symbol, 'api_token':API_TOKEN}
    api_requests = requests.get(WTD_BASE_URL,params=infos)
    try:
        return json.loads(api_requests.content)
    except:
        print("Unexpected Error #1")
'''
def getCurrencyDataWithBase(base,valueDate):
    print(valueDate)
    if(valueDate == str(date('today'))):
        url = CURRENCY_BASE_URL + '/latest'
    else:
        url = CURRENCY_BASE_URL + '/{}'.format(valueDate)
    infos = {'base':base,'symbols':'JPY,USD,NOK,EUR,GBP'}
    api_requests = requests.get(url,params=infos)
    jsonFile = json.loads(api_requests.content)
    print(jsonFile)
    EURNOK = 1/float(jsonFile['rates']['EUR'])
    USDNOK = 1/float(jsonFile['rates']['USD'])
    GBPNOK = 1/float(jsonFile['rates']['GBP'])
    EURUSD = float(EURNOK/USDNOK)
    USDJPY = USDNOK*float(jsonFile['rates']['JPY'])
    returnJSON = {"EURNOK":EURNOK,"USDNOK":USDNOK,"GBPNOK":GBPNOK,"EURUSD":EURUSD, "USDJPY":USDJPY}
    return returnJSON

def getCurrencyData():
    jsonFile = getCurrencyDataWithBase('NOK',date('today'))
    jsonYesterdayFile = getCurrencyDataWithBase('NOK',date('yesterday'))
    returnEURNOK = {'price':jsonFile['EURNOK'], 'change_pct':'{}'.format((float(jsonFile['EURNOK'])-float(jsonYesterdayFile['EURNOK']))/float(jsonYesterdayFile['EURNOK'])*100)}
    returnUSDNOK = {'price':jsonFile['USDNOK'], 'change_pct':'{}'.format((float(jsonFile['USDNOK'])-float(jsonYesterdayFile['USDNOK']))/float(jsonYesterdayFile['USDNOK'])*100)}
    returnGBPNOK = {'price':jsonFile['GBPNOK'], 'change_pct':'{}'.format((float(jsonFile['GBPNOK'])-float(jsonYesterdayFile['GBPNOK']))/float(jsonYesterdayFile['GBPNOK'])*100)}
    returnEURUSD = {'price':jsonFile['EURUSD'], 'change_pct':'{}'.format((float(jsonFile['EURUSD'])-float(jsonYesterdayFile['EURUSD']))/float(jsonYesterdayFile['EURUSD'])*100)}
    returnUSDNOK = {'price':jsonFile['USDJPY'], 'change_pct':'{}'.format((float(jsonFile['USDJPY'])-float(jsonYesterdayFile['USDJPY']))/float(jsonYesterdayFile['USDJPY'])*100)}
    combinedReturn = {'EURNOK':returnEURNOK,'USDNOK':returnUSDNOK, 'GBPNOK':returnGBPNOK, 'EURUSD':returnEURUSD, 'USDNOK':returnUSDNOK}
    return combinedReturn
'''

def findLocalHistoryData(tickerName,date):
    try:
        ticker_filename = 'json/data.json'
        with open(ticker_filename,'r') as file:
            jsonDictionary = json.load(file)
            return jsonDictionary[wtd_symbol[tickerName]][date]['price']
    except:
        print('Error finding local data! #29')
        return ''

def writeLocalHistory(data):
     with open('json/data.json','r+') as file:
                dictionary = {}
                try:
                    dictionary = json.load(file)
                except:
                    pass
                dictionary.update(data)
                file.seek(0)
                file.truncate(0)
                json.dump(dictionary,file)

def getAllValues():
    allData = {}
    for ticker_name in ticker_names:
        if ticker_name in ','.join(wtd_symbol).split(','):
            
            #For current price and day_change
            responseJSON = getCurrentDataFromWTC(wtd_symbol[ticker_name])
            currentPrice = responseJSON['data'][0]['price']
            day_change = responseJSON['data'][0]['change_pct']

            #For Year Change
            year_change = ""
            priceLastYear = findLocalHistoryData(ticker_name,date('lastyear'))
            try:
                year_change = str((float(currentPrice)-float(priceLastYear))/(float(priceLastYear))*100)
            except:
                year_change = ''

            #For YTD Change
            ytd_change = ""
            priceOnYearStart = findLocalHistoryData(ticker_name,date('yearstart'))
            try:
                ytd_change = str(((float(currentPrice)-float(priceOnYearStart))/float(priceOnYearStart))*100)
            except:
                ytd_change = ''

            parsedJSON = {wtd_symbol[ticker_name]:{date('today'):{'price':currentPrice,'day_change':day_change, 'year_change':year_change, 'ytd_change':ytd_change}}}
            allData.update(parsedJSON)
        
        elif ticker_name in ','.join(yahoo_symbol).split(','):
            resposeDataYahoo = getDataFromYahoo(yahoo_symbol[ticker_name])
            currentPrice = resposeDataYahoo['price']
            day_change = resposeDataYahoo['change_pct']

            #For Year Change
            year_change = ""
            priceLastYear = findLocalHistoryData(ticker_name,date('lastyear'))
            try:
                year_change = str((float(currentPrice)-float(priceLastYear))/(float(priceLastYear))*100)
            except:
                year_change = ''

            #For YTD Change
            ytd_change = ""
            priceOnYearStart = findLocalHistoryData(ticker_name,date('yearstart'))
            try:
                ytd_change = str(((float(currentPrice)-float(priceOnYearStart))/float(priceOnYearStart))*100)
            except:
                ytd_change = ''

            parsedJSON = {yahoo_symbol[ticker_name]:{date('today'):{'price':currentPrice,'day_change':day_change, 'year_change':year_change, 'ytd_change':ytd_change}}}
            allData.update(parsedJSON)
        
        elif ticker_name in ','.join(bloomberg_symbol).split(','):
            resposeDataBloomberg = getBloombergData(ticker_name)
            currentPrice = resposeDataBloomberg[bloomberg_symbol[ticker_name]][date('today')]['price']
            day_change = resposeDataBloomberg[bloomberg_symbol[ticker_name]][date('today')]['day_change']
            year_change = resposeDataBloomberg[bloomberg_symbol[ticker_name]][date('today')]['year_change']
            ytd_change = resposeDataBloomberg[bloomberg_symbol[ticker_name]][date('today')]['ytd_change']
            allData.update(resposeDataBloomberg)


    writeLocalHistory(allData)
    return allData
    


print(getBloombergData("Trend Global"))