from bs4 import BeautifulSoup
def getBloomberg():
    soup = BeautifulSoup(open('web.html'),features='lxml')
    valueDataBlock=soup.find_all('span',string='TRENDEU:NO')[0].find_parent('section').nextSibling.find_all('span')
    currentValue = valueDataBlock[0].get_text().replace(',','')
    changePercent = valueDataBlock[3].get_text()
    ytdValue=soup.find_all('span',string='YTD Return')[0].nextSibling.get_text()
    oneYearReturnValue=soup.find_all('span',string='1 Year Return')[0].nextSibling.get_text()
    value = ','.join((currentValue,changePercent,ytdValue,oneYearReturnValue))
    return value



print(getCurrentCurrencyData())