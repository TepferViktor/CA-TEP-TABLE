import requests
import openpyxl
import json
from openpyxl import load_workbook

def market_parse():
    btc_usdt = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
    busd_usdt = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BUSDUSDT")
    BTC_busd = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCBUSD")
    BNB_usdt = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT")
    ETH_usdt = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT")
    RUB_usdt = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=USDTRUB")
    btc_bnb = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BNBBTC")
    bnb_busd = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BNBBUSD")
    eth_btc = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=ETHBTC")
    eth_busd = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=ETHBUSD")
    eth_bnb = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BNBETH")
    btc_rub = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCRUB")
    busd_rub = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BUSDRUB")
    bnb_rub = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BNBRUB")
    eth_rub = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=ETHRUB")
    print(btc_usdt.text)
    print(busd_usdt.text)
    print(BTC_busd.text)

    book = load_workbook('binance.xlsx')
    sheet = book.active  

    """ПОКУПКА USDT ТИНЬКОФФ"""
    with open('dataMarket.json', 'w') as outfile:
        json.dump(btc_usdt.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)


    print(f"buy:{jsData['price']} rub")
    sheet['C21'] = jsData['price']
    sheet['B22'] = jsData['price']
#######################BUSDUSDT#####################
    with open('dataMarket.json', 'w') as outfile:
        json.dump(busd_usdt.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)
    print(f"market:{jsData['price']} usdt")
    sheet['D21'] = jsData['price']
    sheet['B23'] = jsData['price']
#######################BTCBUSD##############################
    with open('dataMarket.json', 'w') as outfile:
        json.dump(btc_usdt.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)
    print(f"market:{jsData['price']} usdt")
    sheet['D22'] = jsData['price']
    sheet['C23'] = jsData['price']
#######################BNBUSDT##############################
    with open('dataMarket.json', 'w') as outfile:
        json.dump(BNB_usdt.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)
    print(f"market:{jsData['price']} usdt")
    sheet['E21'] = jsData['price']
    sheet['B24'] = jsData['price']

#######################ETHUSDT##############################
    with open('dataMarket.json', 'w') as outfile:
        json.dump(ETH_usdt.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)
    print(f"market:{jsData['price']} usdt")
    sheet['F21'] = jsData['price']
    sheet['B25'] = jsData['price']

#######################RUBUSDT##############################
    with open('dataMarket.json', 'w') as outfile:
        json.dump(RUB_usdt.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)
    print(f"market:{jsData['price']} usdt")
    sheet['G21'] = jsData['price']
    sheet['B26'] = jsData['price']
#######################BTCBNB##############################
    with open('dataMarket.json', 'w') as outfile:
        json.dump(btc_bnb.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)
    print(f"market:{jsData['price']} usdt")
    sheet['E22'] = jsData['price']
    sheet['C24'] = jsData['price']
#######################BNBBUSD##############################
    with open('dataMarket.json', 'w') as outfile:
        json.dump(bnb_busd.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)
    print(f"market:{jsData['price']} usdt")
    sheet['E23'] = jsData['price']
    sheet['D24'] = jsData['price']

#######################ETHBTC ##############################
    with open('dataMarket.json', 'w') as outfile:
        json.dump(eth_btc.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)
    print(f"market:{jsData['price']} usdt")
    sheet['F22'] = jsData['price']
    sheet['C25'] = jsData['price']

#######################ETHBUSD ##############################
    with open('dataMarket.json', 'w') as outfile:
        json.dump(eth_busd.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)
    print(f"market:{jsData['price']} usdt")
    sheet['F23'] = jsData['price']
    sheet['D25'] = jsData['price']
#######################ETHBNB##############################
    with open('dataMarket.json', 'w') as outfile:
        json.dump(eth_bnb.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)
    print(f"market:{jsData['price']} usdt")
    sheet['F24'] = jsData['price']
    sheet['E25'] = jsData['price']

#######################BTCRUB##############################
    with open('dataMarket.json', 'w') as outfile:
        json.dump(btc_rub.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)
    print(f"market:{jsData['price']} usdt")
    sheet['G22'] = jsData['price']
    sheet['C26'] = jsData['price']


#######################BUSDRUB##############################
    with open('dataMarket.json', 'w') as outfile:
        json.dump(busd_rub.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)
    print(f"market:{jsData['price']} usdt")
    sheet['G23'] = jsData['price']
    sheet['D26'] = jsData['price']

#######################BNBRUB##############################
    with open('dataMarket.json', 'w') as outfile:
        json.dump(bnb_rub.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)
    print(f"market:{jsData['price']} usdt")
    sheet['G24'] = jsData['price']
    sheet['E26'] = jsData['price']
#######################ETHRUB##############################
    with open('dataMarket.json', 'w') as outfile:
        json.dump(eth_rub.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)
    print(f"market:{jsData['price']} usdt")
    sheet['G25'] = jsData['price']
    sheet['F26'] = jsData['price']

    book.save("binance.xlsx")
    book.close()
