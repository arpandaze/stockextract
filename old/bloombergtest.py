import requests
import bs4

url = requests.get("https://www.bloomberg.com/quote/OSEBX:IND")
print(url.content)