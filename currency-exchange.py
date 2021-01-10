#import modules
import requests as req
from json import loads

#Get data test - uses Euro by default
response = req.get(url='https://api.exchangeratesapi.io/latest')
#Deserialise response into Python dictionary
exchangeDict = loads(response.text)

print(exchangeDict['rates']['CAD'])
