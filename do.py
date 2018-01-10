import HitBtcApi
import Config
import Logics
import numpy as np
import math
import time

def SortedOrders(keys):
	orders = HitBtcApi.GetOrders(keys)
	for order in orders:
		if (order['side'] == 'buy') & (order['status'] == 'new'):
			if order['symbol'] in Config.TradedCurrency:
				Config.TradedCurrency.pop(order['symbol'])
			HitBtcApi.CancelOrders(keys, order['clientOrderId'])

def RemoveBadCurrencys():
	for key in list(Config.TradedCurrency):
		currency = Config.TradedCurrency[key]
		if (currency['rank'] < Config.MinRank) | (currency['quantityIncrement'] > Config.MaxPrice / currency['bid']):
			Config.TradedCurrency.pop(key)
		elif key.replace(Config.QuotedCurrency, "") in Config.Balance:
			Config.TradedCurrency.pop(key)

def RemoveBadMarkets():
	for key in list(Config.TradedCurrency):
		currency = Config.TradedCurrency[key]

		candles = HitBtcApi.GetCandles(key, Config.Period)
		y = [(float(candle['open']) + float(candle['close']))/2 for candle in candles]
		x = range(len(candles))

		fit = np.polyfit(x,y,1)
		fit_fn = np.poly1d(fit)
		Degree = math.degrees(math.atan(fit_fn[1]))

		if Logics.should_buy(candles) & (Degree >= Config.MinDegree) & (Degree <= Config.MaxDegree):
			minY = min(y)
			r = fit_fn(x)[y.index(minY)] - minY
			r -= r * 0.1
			minPrice = float(fit_fn(x)[len(x) - 1] - r)

			maxY = max(y)
			r = fit_fn(x)[y.index(maxY)] - maxY
			r -= r * 0.1
			maxPrice = float(fit_fn(x)[len(x) - 1] - r)
				
			if (currency['ask'] < minPrice) | (currency['ask'] > maxPrice):
				Config.TradedCurrency.pop(key)

def Chopping():
	i = Config.Quantity - len(Config.Balance)
	for key in list(Config.TradedCurrency):
		if i < Config.Quantity:
			i += 1
		else:
			Config.TradedCurrency.pop(key)

def SellCurrencys(keys):
	for key in Config.TradedCurrency.copy().keys():
		currency = Config.TradedCurrency[key]
		informations(currency)
		HitBtcApi.CreateOrders(keys, key, "sell", currency['quantity'], currency['ask'])
	Config.TradedCurrency.clear()

def BuyCurrencys(keys):
	for key in Config.TradedCurrency.copy().keys():
		currency = Config.TradedCurrency[key]
		currency['quantity'] = math.trunc(Config.MaxPrice / currency['bid'] / currency['quantityIncrement']) * currency['quantityIncrement']
		HitBtcApi.CreateOrders(keys, key, "buy", currency['quantity'], currency['bid'])

def informations(currency):
	print("\033[92m",time.strftime('%H:%M'),"BUY ", currency['quantity'], currency['symbol'], currency['bid'] * currency['quantity'],"\033[0m")
	print("\033[91m",time.strftime('%H:%M'),"SELL ", currency['quantity'], currency['symbol'], currency['ask'] * currency['quantity'],"\033[0m")
	profit = (currency['ask'] * currency['quantity'] - currency['bid'] * currency['quantity'])
	StockFee = currency['ask'] * currency['quantity'] * Config['StockFee'] + currency['bid'] * currency['quantity'] * Config['StockFee']
	print("\033[96m+", profit-StockFee, "\033[0m")