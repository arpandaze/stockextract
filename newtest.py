import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random

with open('proxy.txt','r') as proxyFile:
    #proxyList=proxyFile.read().split('\n')
    content = proxyFile.read()

def randomProxy():
    parameters = {'limit':'1','format':'txt','type':'https'}
    baseURL = 'http://pubproxy.com/api/proxy'
    request = requests.get(baseURL, params=parameters)
    return request.content

def getBloomberg():
    valueDataBlock = []
    while(valueDataBlock == []):
        proxy = '87.120.179.74:4145'
        print(proxy)
        userAgent = UserAgent()
        header = {'User-Agent': userAgent.random}
        print(header)
        proxyDictionary = {'http':'socks4://{}'.format(proxy),'https':'socks4://{}'.format(proxy)}
        url = requests.get('https://www.bloomberg.com/quote/TRENDEU:NO',headers=header,proxies=proxyDictionary)
        soup = BeautifulSoup(url.content,features='lxml')
        textBlock = soup.find_all('span',string='TRENDEU:NO')
        print(url.content)

    valueDataBlock = textBlock[0].find_parent('section').nextSibling.find_all('span')
    currentValue = valueDataBlock[0].get_text().replace(',','')
    changePercent = valueDataBlock[3].get_text()
    ytdValue=soup.find_all('span',string='YTD Return')[0].nextSibling.get_text()
    oneYearReturnValue=soup.find_all('span',string='1 Year Return')[0].nextSibling.get_text()
    value = ','.join((currentValue,changePercent,ytdValue,oneYearReturnValue))
    return value
data = getBloomberg()
while(data == []):
    getBloomberg()
print(data)