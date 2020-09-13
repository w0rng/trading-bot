from time import sleep
from decimal import Decimal
from API.HitBtcApi import HitBtcAPI
import System.Accomplish as Accomplish
import System.Sorting as Sorting


config = Accomplish.get_config('HitBtc')
api = HitBtcAPI(config['PublicKey'], config['SecretKey'])
TradedCurrency = {}


while True:
    TradedCurrency = Sorting.sorted_orders(TradedCurrency, api, config)
    TradedCurrency = Accomplish.sell_currency(TradedCurrency, api.CreateOrders)
    MainBalance, Balance = Accomplish.get_balance(
        api.GetBalance, config['QuotedCurrency'])
    if len(Balance) < config['Quantity']:
        MaxPrice = Decimal(MainBalance / (config['Quantity']-len(Balance)))
        TradedCurrency = Accomplish.get_tickers(api, config, MaxPrice)
        TradedCurrency = Sorting.remove_bad_currency(
            TradedCurrency, Balance, config)
        TradedCurrency = Sorting.remove_bad_markets(
            TradedCurrency, config, api)
        TradedCurrency = Sorting.chopping(
            TradedCurrency, Balance, config['Quantity'])
        Accomplish.buy_currency(TradedCurrency, MaxPrice, api.CreateOrders)
    sleep(int(config['Sleep']))
