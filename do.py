import HitBtcApi
import Config
import Logics
from sklearn import linear_model
from math import atan

def SortedOrders(keys, orders):
	Config.Orders.clear()
	for order in orders:
		if order['side'] == 'buy':
			temp = Config.TradedCurrency
			for currency in temp:
				if(order['symbol'] == currency.symbol):
					temp.remove(currency)
			HitBtcApi.CancelOrders(keys, order['clientOrderId'])
			Config.TradedCurrency = temp

def SortCurrencyTraded():
	a = Config.TradedCurrency
	for currency in a:
		if ((currency.rank < 0.5) #если маленький ранг
		or (currency.quantityIncrement > Config.MaxPrice / currency.bid)): #если на можем позволить минимум
			a.remove(currency)
	Config.TradedCurrency = a

def RemoveBadTradedCurrency():
	currencys = Config.TradedCurrency
	for currency in currencys:
		temp = HitBtcApi.GetCandles(currency.symbol, Config.Period)
		x = []
		y = []
		i = 0
		for candles in temp:
			x.append([(float(candles['open']) + float(candles['close']))/2])
			y.append([i])
			i += 1
		regr = linear_model.LinearRegression()
		regr.fit(x, y)
		if not Logics.should_buy(temp): 
			if atan(regr.score(x, y)) * currency.rank <= 500:
				currencys.remove(currency)
	Config.TradedCurrency = currency

def RemovalAvailableCurrencies():
	orders = Config.orders
	currencys = Config.TradedCurrency

	for currency in currencys:
		for order in orders:
			if currency.symbol == order['symbol']:
				currencys.remove(currency)
	Config.TradedCurrency = currency

#def SellCurrencys():
