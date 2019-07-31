import math
import json
from System.Technical import ConvertFloatToDecimal


@ConvertFloatToDecimal
def GetConfig(configName):
    file = open('Configs/%s.conf' % configName)
    config = json.load(file)
    file.close()
    return config


def GetBalance(GetBalance, QuotedCurrency):
    Accounts = GetBalance(QuotedCurrency)
    Balance = {}
    MainBalance = 0
    for balance in Accounts:
        if balance['currency'] == QuotedCurrency:
            MainBalance = balance['available']
        elif balance['reserved'] or balance['available']:
            Balance.update(
                {
                    balance['currency']:
                        (balance['reserved'], balance['available'])
                })
    return MainBalance, Balance


def checkPriceCyrrency(ask, bid, config):
    if not (ask and bid):
        return False
    askPrice = ask - ask*config['StockFee']
    bidPrice = bid + bid*config['StockFee']
    profit = (askPrice-bidPrice) / bidPrice * 100
    return (profit >= config['Profit']) and (bid >= config['MinPrice'])


def generateInfoSymbol(symbol, ask, bid, volume, api, config, MaxPrice):
    rank = (ask-bid) / bid*volume
    if rank >= config["MinRank"]:
        quantityIncrement = api.GetInfoSumbols(symbol)['quantityIncrement']
        if quantityIncrement <= (MaxPrice/bid):
            return {
                'ask': ask,
                'bid': bid,
                'rank': rank,
                'quantityIncrement': quantityIncrement
            }


def GetTickers(api, config, MaxPrice):
    AllTicker = api.GetTickers()
    Traded = {}
    for Ticker in AllTicker:
        if (Ticker['bid'] is None) or \
                (config['QuotedCurrency'] not in Ticker['symbol']):
            continue
        symbol = Ticker['symbol']
        ask = Ticker['ask']
        bid = Ticker['bid']
        if checkPriceCyrrency(ask, bid, config):
            Traded[symbol] = generateInfoSymbol(
                symbol,
                ask,
                bid,
                Ticker['volume'],
                api,
                config,
                MaxPrice
            )
    return Traded


def BuyCurrencys(TradedCurrency, MaxPrice, CreateOrders):
    for key in list(TradedCurrency):
        currency = TradedCurrency[key]
        quantity = \
            math.trunc(
                MaxPrice /
                currency['bid'] /
                currency['quantityIncrement']) * \
            currency['quantityIncrement']
        CreateOrders(key, "buy", quantity, currency['bid'])
    return {}


def SellCurrencys(TradedCurrency, CreateOrders):
    for key in list(TradedCurrency):
        currency = TradedCurrency[key]
        CreateOrders(key, "sell", currency['quantity'], currency['ask'])
    return {}
