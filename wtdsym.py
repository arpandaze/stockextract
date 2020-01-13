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

 with open('json/data.json','r+') as file:
                dictionary = {}
                try:
                    dictionary = json.load(file)
                except:
                    pass
                dictionary.update(parsedJSON)
                file.seek(0)
                file.truncate(0)
                json.dump(dictionary,file)

#BLOCK 1
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
#END


