import json
import requests

API_TOKEN = "Tpk_eb3e0daef86247048427e83fb5c2ede6"
ACCOUNT_NO = "e70f30abda8214d4b9aaf8e1123516a2"
SECRET = "Tsk_95821557e2ea49ccb2dd8e837aa56b84"

BASE_URL = "https://sandbox.iexapis.com/"

api_request = requests.get("{base_url}stable/stock/aapl/quote?token=Tpk_eb3e0daef86247048427e83fb5c2ede6".format(BASE_URL,))
print(api_request.content)