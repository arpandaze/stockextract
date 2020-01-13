from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import datetime

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

def getBloomberg(ticker_name):
    '''
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options,executable_path=r'webdriver.exe')
    driver.get("https://www.bloomberg.com/quote/TRENDEU:NO")
    raw_html = str(driver.page_source.encode("utf-8"))
    driver.close()
    soup = BeautifulSoup(raw_html,'lxml')
    '''
    textBlock = soup.find_all('span',string='TRENDEU:NO')
    valueDataBlock = textBlock[0].find_parent('section').findNext('section').find_all('span')
    currentValue = valueDataBlock[0].get_text().replace(',','')
    changePercent = str(float(valueDataBlock[3].get_text()[:-1]))
    try:
        ytdValue=soup.find_all('span',string='YTD Return')[0].nextSibling.get_text()
    except:
        ytdValue=''
    try:
        oneYearReturnValue=soup.find_all('span',string='1 Year Return')[0].nextSibling.get_text()
    except:
        oneYearReturnValue=''

    returnJSON = {bloomberg_symbol[ticker_name]:{date('today'):{'price':currentValue,'day_change':changePercent, 'year_change':oneYearReturnValue, 'ytd_change':ytdValue}}}
    return returnJSON

print(getBloomberg('Trend USA'))