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
    sheet['C21'] = float(jsData['price'])
    sheet['B22'] = float(jsData['price'])
#######################BUSDUSDT#####################
    with open('dataMarket.json', 'w') as outfile:
        json.dump(busd_usdt.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)
    print(f"market:{jsData['price']} usdt")
    sheet['D21'] = float(jsData['price'])
    sheet['B23'] =float(jsData['price'])
#######################BTCBUSD##############################
    with open('dataMarket.json', 'w') as outfile:
        json.dump(btc_usdt.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)
    print(f"market:{jsData['price']} usdt")
    sheet['D22'] = float(jsData['price'])
    sheet['C23'] =float(jsData['price'])
#######################BNBUSDT##############################
    with open('dataMarket.json', 'w') as outfile:
        json.dump(BNB_usdt.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)
    print(f"market:{jsData['price']} usdt")
    sheet['E21'] = float(jsData['price'])
    sheet['B24'] = float(jsData['price'])

#######################ETHUSDT##############################
    with open('dataMarket.json', 'w') as outfile:
        json.dump(ETH_usdt.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)
    print(f"market:{jsData['price']} usdt")
    sheet['F21'] = float(jsData['price'])
    sheet['B25'] = float(jsData['price'])

#######################RUBUSDT##############################
    with open('dataMarket.json', 'w') as outfile:
        json.dump(RUB_usdt.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)
    print(f"market:{jsData['price']} usdt")
    sheet['G21'] = float(jsData['price'])
    sheet['B26'] = float(jsData['price'])
#######################BTCBNB##############################
    with open('dataMarket.json', 'w') as outfile:
        json.dump(btc_bnb.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)
    print(f"market:{jsData['price']} usdt")
    sheet['E22'] =float(jsData['price'])
    sheet['C24'] = float(jsData['price'])
#######################BNBBUSD##############################
    with open('dataMarket.json', 'w') as outfile:
        json.dump(bnb_busd.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)
    print(f"market:{jsData['price']} usdt")
    sheet['E23'] = float(jsData['price'])
    sheet['D24'] = float(jsData['price'])

#######################ETHBTC ##############################
    with open('dataMarket.json', 'w') as outfile:
        json.dump(eth_btc.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)
    print(f"market:{jsData['price']} usdt")
    sheet['F22'] = float(jsData['price'])
    sheet['C25'] = float(jsData['price'])

#######################ETHBUSD ##############################
    with open('dataMarket.json', 'w') as outfile:
        json.dump(eth_busd.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)
    print(f"market:{jsData['price']} usdt")
    sheet['F23'] = float(jsData['price'])
    sheet['D25'] = float(jsData['price'])
#######################ETHBNB##############################
    with open('dataMarket.json', 'w') as outfile:
        json.dump(eth_bnb.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)
    print(f"market:{jsData['price']} usdt")
    sheet['F24'] = float(jsData['price'])
    sheet['E25'] = float(jsData['price'])

#######################BTCRUB##############################
    with open('dataMarket.json', 'w') as outfile:
        json.dump(btc_rub.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)
    print(f"market:{jsData['price']} usdt")
    sheet['G22'] = float(jsData['price'])
    sheet['C26'] = float(jsData['price'])


#######################BUSDRUB##############################
    with open('dataMarket.json', 'w') as outfile:
        json.dump(busd_rub.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)
    print(f"market:{jsData['price']} usdt")
    sheet['G23'] = float(jsData['price'])
    sheet['D26'] = float(jsData['price'])

#######################BNBRUB##############################
    with open('dataMarket.json', 'w') as outfile:
        json.dump(bnb_rub.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)
    print(f"market:{jsData['price']} usdt")
    sheet['G24'] = float(jsData['price'])
    sheet['E26'] = float(jsData['price'])
#######################ETHRUB##############################
    with open('dataMarket.json', 'w') as outfile:
        json.dump(eth_rub.json(), outfile)
    
    with open('dataMarket.json') as file:   
        jsData = json.load(file)
    print(f"market:{jsData['price']} usdt")
    sheet['G25'] = float(jsData['price'])
    sheet['F26'] = float(jsData['price'])

    book.save("binance.xlsx")
    book.close()
