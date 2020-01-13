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
'''
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

'''
