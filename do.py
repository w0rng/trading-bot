import HitBtcApi
import Config
import Logics
from sklearn import linear_model
import math
from decimal import Decimal

def SortedOrders(keys, orders):
	currencys = Config.TradedCurrency
	purchasedCurrencies = currencys
	for order in orders:
		if order['side'] == 'buy':
			for currency in currencys:
				print(currency.symbol, order['symbol'])
				if currency.symbol == order['symbol']:
					purchasedCurrencies.remove(currency)
					break
			HitBtcApi.CancelOrders(keys, order['clientOrderId'])
	Config.TradedCurrency = purchasedCurrencies

def RemoveBadTradedCurrency():
	currencys = Config.TradedCurrency
	goodCurrency = []
	for currency in currencys:
		if (currency.rank >= Config.MinRank) and (currency.quantityIncrement <= (Config.MaxPrice / currency.bid)):
			goodCurrency.append(currency)
	balance = Config.Balance
	temp = goodCurrency
	for currency in temp:
		for b in balance:
			if b['currency'] + Config.QuotedCurrency == currency.symbol:
				goodCurrency.remove(currency)
				break
	Config.TradedCurrency = goodCurrency

def RemoveCurencyFallingMarket():
	currencys = Config.TradedCurrency
	goodCurrency = []
	for currency in currencys:
		candles = HitBtcApi.GetCandles(currency.symbol, Config.Period)
		y = [(float(candle['open']) + float(candle['close']))/2 for candle in candles]
		x = [[i] for i in range(0, len(candles))]
		regr = linear_model.LinearRegression()
		regr.fit(x, y)
		if (Logics.should_buy(candles)) and (Decimal(math.atan(regr.coef_)) > Decimal(-0.001)):
			goodCurrency.append(currency)
	Config.TradedCurrency = goodCurrency

def SellCurrencys(keys):
	currencys = Config.TradedCurrency
	for currency in currencys:
		print("SELL ", currency.quantity, currency.symbol, currency.quantity * currency.ask)
		HitBtcApi.CreateOrders(keys, currency.symbol, "sell", currency.quantity, currency.quantity * currency.ask)

def BuyCurrencys(keys):
	currencys = Config.TradedCurrency
	temp = []
	for i in range(0, (Config.Quantity - len(Config.Balance))):
		currency = currencys[i]
		currency.quantity = math.trunc(Config.MaxPrice / currency.bid / currency.quantityIncrement) * currency.quantityIncrement
		print("BUY ", currency.quantity, currency.symbol, currency.quantity * currency.bid)
		HitBtcApi.CreateOrders(keys, currency.symbol, "buy", currency.quantity, currency.quantity * currency.bid)
		temp.append(currency)

	Config.TradedCurrency = temp