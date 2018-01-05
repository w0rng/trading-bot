import HitBtcApi
import Config
import Logics
from sklearn import linear_model
from math import atan

def SortedOrders(keys, orders):
	currencys = Config.TradedCurrency
	purchasedCurrencies = currencys
	for order in orders:
		if order['side'] == 'buy':
			for currency in currencys:
				if currency.symbol == order['symbol']:
					purchasedCurrencies.remove(currency)
					break
			HitBtcApi.CancelOrders(keys, order['clientOrderId'])

def RemoveBadTradedCurrency():
	currencys = Config.TradedCurrency
	goodCurrency = []
	for currency in currencys:
		if (currency.rank >= Config.MinRank) and (currency.quantityIncrement <= (Config.MaxPrice / currency.bid)):
			goodCurrency.append(currency)
	Config.TradedCurrency = goodCurrency

def RemoveCurencyFallingMarket():
	currencys = Config.TradedCurrency
	goodCurrency = []
	for currency in currencys:
		candles = HitBtcApi.GetCandles(currency.symbol, Config.Period)
		x = [[(float(candle['open']) + float(candle['close']))/2] for candle in candles]
		y = [i for i in range(0, len(candles))]
		regr = linear_model.LinearRegression()
		regr.fit(x, y)
		if (Logics.should_buy(candles)) or (atan(regr.score(x, y)) > 0.17):
			goodCurrency.append(currency)
	Config.TradedCurrency = goodCurrency

#def RemovalAvailableCurrencies():
#	orders = Config.orders
#	currencys = Config.TradedCurrency
#
#	for currency in currencys:
#		for order in orders:
#			if currency.symbol == order['symbol']:
#				currencys.remove(currency)
#	Config.TradedCurrency = currency

#def SellCurrencys():
