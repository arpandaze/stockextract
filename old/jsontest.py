import json

file = open("stock.json",'r')
json_file = json.loads(file.read())
print(json_file["symbol"])