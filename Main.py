from time import sleep
from decimal import Decimal
from API.HitBtcApi import HitBtcAPI
import System.Accomplish as Accomplish
import System.Sortings as Sortings


config = Accomplish.GetConfig('HitBtc')
api = HitBtcAPI(config['PublicKey'], config['SecretKey'])
TradedCurrency = {}


while True:
    TradedCurrency = Sortings.SortedOrders(TradedCurrency, api, config)
    TradedCurrency = Accomplish.SellCurrencys(TradedCurrency, api.CreateOrders)
    MainBalance, Balance = Accomplish.GetBalance(
        api.GetBalance, config['QuotedCurrency'])
    if len(Balance) < config['Quantity']:
        MaxPrice = Decimal(MainBalance / (config['Quantity']-len(Balance)))
        TradedCurrency = Accomplish.GetTickers(api, config, MaxPrice)
        TradedCurrency = Sortings.RemoveBadCurrencys(
            TradedCurrency, Balance, config)
        TradedCurrency = Sortings.RemoveBadMarkets(TradedCurrency, config, api)
        TradedCurrency = Sortings.Chopping(
            TradedCurrency, Balance, config['Quantity'])
        TradedCurrency = Accomplish.BuyCurrencys(
            TradedCurrency, MaxPrice, api.CreateOrders)
    sleep(config['Sleep'])
