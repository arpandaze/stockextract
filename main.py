import json
import requests
from bs4 import BeautifulSoup
import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from openpyxl import Workbook
from openpyxl import load_workbook
from xlsx2html import xlsx2html

API_TOKEN = 'YOUY API KEY HERE'
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
                'Olje',
                'Kobber',
                'Aluminium',
                'Gull',
                'USDNOK',
                'EURNOK',
                'GBPNOK',
                'EURUSD',
                'USDJPY',
                'iShare High Yield',
                'US 10 Yr',
                'Trend Global',
                'Trend Europa',
                'Trend USA'
                ]

symbols = { 
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
                    'Gull':'GC=F',
                    'Trend Global':'TRENDEN:NO',
                    'Trend Europa':'TRENDEU:NO',
                    'Trend USA':'TRENDUS:NO',
                    'Olje':'CO1:COM',
                    'Kobber':'LMCADS03:COM',
                    'Aluminium':'LMAHDS03:COM',
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

wtd_list = [
                'S&P 500',
                'Nasdaq Comp',
                'Dow Jones',
                'Russell2000',
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
                'FTSE China A50',
                '3188 HK'
            ]

yahoo_list = [
                'Shanghai Composite',
                'CSI 300',
                'HSCEI',
                'OSEBX',
                'iShare High Yield',
                'US 10 Yr',
                'USDNOK',
                'USDJPY',
                'EURUSD',
                'GBPNOK',
                'EURNOK',
                'Gull'
              ]

bloomberg_list = [
                        'Trend Global',
                        'Trend Europa',
                        'Trend USA',
                        'Olje',
                        'Kobber',
                        'Aluminium'
                 ]

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
        price_text = header_block[2].find_all('span')[0].get_text().replace(',','')
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
    driver.get("https://www.bloomberg.com/quote/{}".format(symbols[ticker_name]))
    raw_html = str(driver.page_source.encode("utf-8"))
    driver.close()
    soup = BeautifulSoup(raw_html,'lxml')
    textBlock = soup.find_all('span',string='{}'.format(symbols[ticker_name]))
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

    returnJSON = {symbols[ticker_name]:{date('today'):{'price':currentValue,'day_change':changePercent, 'year_change':oneYearReturnValue, 'ytd_change':ytdValue}}}
    return returnJSON

def getCurrentDataFromWTC(symbol):
    infos = {'symbol':symbol, 'api_token':API_TOKEN}
    api_requests = requests.get(WTD_BASE_URL,params=infos)
    try:
        return json.loads(api_requests.content)
    except:
        print("Unexpected Error #1")

def findLocalHistoryData(tickerName,date):
    try:
        ticker_filename = 'json/data.json'
        with open(ticker_filename,'r') as file:
            jsonDictionary = json.load(file)
            return jsonDictionary[symbols[tickerName]][date]['price']
    except:
        print('Local history missing! Continuing without it!')
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

def exportToExcel(JSONData,date,name):
    excel_workbook = load_workbook('others/stocks_temp.xlsx')
    excel_worksheet = excel_workbook.active
    dataList = []
    for ticker_name in ticker_names:
        indData = []
        base=JSONData[symbols[ticker_name]][date]

        if(base['price'] != ''):
            indData += [float(base['price'].replace(',',''))]
        else:
            indData += ['']

        if(base['day_change'] != ''):
            indData += [float(base['day_change'].replace(',',''))/100]
        else:
            indData = ['']
        
        if(base['year_change'] != ''):
            indData += [float(base['year_change'].replace(',',''))/100]
        else:
            indData += ['']
        
        if(base['ytd_change'] != ''):
            indData += [float(base['ytd_change'].replace(',',''))/100]
        else:
            indData += ['']
        dataList += [indData]
    
    #USA Tickers
    for j in range(4):
        for i in range(4):
            excel_worksheet['{}{}'.format(chr(ord('B')+i), str(4+j))] = dataList[j][i]

    #Europe Tickers
    for j in range(9):
        for i in range(4):
            excel_worksheet['{}{}'.format(chr(ord('B')+i), str(10+j))] = dataList[4+j][i]
    
    #Asia Tickers
    for j in range(9):
        for i in range(4):
            excel_worksheet['{}{}'.format(chr(ord('B')+i), str(21+j))] = dataList[13+j][i]

    #Commodities
    for j in range(4):
        for i in range(4):
            excel_worksheet['{}{}'.format(chr(ord('H')+i), str(2+j))] = dataList[22+j][i]

    #Currencies
    for j in range(5):
        for i in range(4):
            excel_worksheet['{}{}'.format(chr(ord('H')+i), str(10+j))] = dataList[26+j][i]

    #Interest & Bonds
    for j in range(2):
        for i in range(4):
            excel_worksheet['{}{}'.format(chr(ord('H')+i), str(21+j))] = dataList[31+j][i]

    #Funds
    for j in range(3):
        for i in range(4):
            excel_worksheet['{}{}'.format(chr(ord('H')+i), str(25+j))] = dataList[33+j][i]

    excel_workbook.save('{}.xlsx'.format(name))
    print("Exported to Excel!")

def exportToHTML(excel_file,export_file_name):
    out_html = xlsx2html(excel_file)
    out_html.seek(0)
    with open(export_file_name,'w') as file:
        file.write(out_html.read())

def getAllValues():
    allData = {}
    for ticker_name in ticker_names:
        if ticker_name in wtd_list:
            
            #For current price and day_change
            responseJSON = getCurrentDataFromWTC(symbols[ticker_name])
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

            parsedJSON = {symbols[ticker_name]:{date('today'):{'price':currentPrice,'day_change':day_change, 'year_change':year_change, 'ytd_change':ytd_change}}}
            allData.update(parsedJSON)
        
        elif ticker_name in yahoo_list:
            resposeDataYahoo = getDataFromYahoo(symbols[ticker_name])
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

            parsedJSON = {symbols[ticker_name]:{date('today'):{'price':currentPrice,'day_change':day_change, 'year_change':year_change, 'ytd_change':ytd_change}}}
            allData.update(parsedJSON)
        
        elif ticker_name in bloomberg_list:
            resposeDataBloomberg = getBloombergData(ticker_name)
            currentPrice = resposeDataBloomberg[symbols[ticker_name]][date('today')]['price']
            day_change = resposeDataBloomberg[symbols[ticker_name]][date('today')]['day_change']
            year_change = resposeDataBloomberg[symbols[ticker_name]][date('today')]['year_change']
            ytd_change = resposeDataBloomberg[symbols[ticker_name]][date('today')]['ytd_change']
            allData.update(resposeDataBloomberg)


    writeLocalHistory(allData)
    exportToExcel(allData,date('today'),date('today'))
    exportToHTML('{}.xlsx'.format(date('today')), '{}.html'.format(date('today')))
    return allData

getAllValues()