import requests
from bs4 import BeautifulSoup
import datetime

yahooSymbol = {'Shanghai Composite':'000001.SS','CSI 300':'000300.SS','HSCEI':'^HSCE', 'OSEBX':'OSEBX.OL', 'iShare High Yield':'HYG', 'US 10 Yr':'^TNX'}



print(getValueFromYahoo('000300.SS'))
'''
import json 

with open('json/osebx_history.json') as jsonFile:
    data = json.load(jsonFile)
data.update()
'''