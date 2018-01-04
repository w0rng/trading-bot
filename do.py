import HitBtcApi
import Config
import Logics
from sklearn import linear_model
from math import atan

def SortedOrders(keys, orders):
	Config.Orders.clear()
	for order in orders:
		if order['side'] == 'buy':
			HitBtcApi.CancelOrders(keys, order['clientOrderId'])
		else:
			Config.Orders.append(order)

def SortCurrencyTraded():
	a = Config.TradedCurrency
	i = 0
	while i < len(a):
		if (a[i][3] < 0.5) or (float(HitBtcApi.GetInfoSumbols(a[i][0])['quantityIncrement']) > Config.MaxPrice / float(a[i][1])) or (a[i][0].find(Config.QuotedCurrency) == -1):
			del a[i]
		else:
			i += 1
	Config.TradedCurrency = a


def RemoveBadTradedCurrency():
	currencys = Config.TradedCurrency
	tempCurrencys = []
	for currency in currencys:
		temp = HitBtcApi.GetCandles(currency[0], Config.Period)
		x = []
		y = []
		i = 0
		for candles in temp:
			x.append([(float(candles['open']) + float(candles['close']))/2])
			y.append([i])
			i += 1
		regr = linear_model.LinearRegression()
		regr.fit(x, y)
		if Logics.should_buy(temp): 
			if atan(regr.score(x, y)) * currency[3] > 500:
				tempCurrencys.append(currency)
	Config.TradedCurrency = tempCurrencys