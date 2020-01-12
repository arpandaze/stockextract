import requests
import json
from bs4 import BeautifulSoup
import pandas

def convert_to_csv():
    xlsx_OSEBX = pandas.read_excel('a.xlsx')
    xlsx_OSEBX.to_csv('data.csv',sep=',')
array = open('data.csv','r').read().split('\n')
for i in array:
    array[array.index(i)]=i.split(',')
array.remove([''])
data={}
for i in array[1:]:
    #print(i[1])
    data[i[1]]=[]
    data[i[1]].append({'value':'{}'.format(i[2])})

with open('osebx.json','w') as file:
    json.dump(data, file)