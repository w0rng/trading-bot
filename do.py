from decimal import Decimal
import HitBtcApi
import Config
import numpy as np
import math
import time

def SortedOrders(keys):
	orders = HitBtcApi.GetOrders(keys)
	for order in orders:
		if (order['side'] == 'buy'):
			if (order['symbol'] in Config.TradedCurrency) & (order['status'] == 'new'):
				Config.TradedCurrency.pop(order['symbol'])
			elif (order['status'] == 'partiallyFilled'):
				Config.TradedCurrency[order['symbol']]['quantity'] = Decimal(order['cumQuantity'])
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
		try:
			y = [(float(candle['open']) + float(candle['close']))/2 for candle in candles]
			x = range(len(candles))

			fit = np.polyfit(x,y,1)
			fit_fn = np.poly1d(fit)
			degree = math.degrees(math.atan(fit_fn[1]))

			#Logics.should_buy(candles) &
			if (degree >= Config.MinDegree) & (degree <= Config.MaxDegree):
				minY = min(y)
				r = fit_fn(x)[y.index(minY)] - minY
				r -= r * 0.1
				minPrice = Decimal(fit_fn(x)[len(x) - 1] - r)

				maxY = max(y)
				r = fit_fn(x)[y.index(maxY)] - maxY
				r -= r * 0.1
				maxPrice = Decimal(fit_fn(x)[len(x) - 1] - r)
					
				if (currency['ask'] < minPrice) | (currency['ask'] > maxPrice):
					Config.TradedCurrency.pop(key)
		except:
			Config.TradedCurrency.pop(key)

def Chopping():
	n = Config.Quantity - len(Config.Balance)
	currencys = Config.TradedCurrency
	Config.TradedCurrency = {key: currencys[key] for key in list(currencys) if list(currencys).index(key) < n}

def SellCurrencys(keys):
	for key in list(Config.TradedCurrency):
		currency = Config.TradedCurrency[key]
		informations(key, currency)
		HitBtcApi.CreateOrders(keys, key, "sell", currency['quantity'], currency['ask'])
	Config.TradedCurrency.clear()

def BuyCurrencys(keys):
	for key in list(Config.TradedCurrency):
		currency = Config.TradedCurrency[key]
		currency['quantity'] = Decimal(math.trunc(Config.MaxPrice / currency['bid'] / currency['quantityIncrement']) * currency['quantityIncrement'])
		HitBtcApi.CreateOrders(keys, key, "buy", currency['quantity'], currency['bid'])

def informations(key, currency):
	print("\033[92m",time.strftime('%H:%M'),"BUY ", currency['quantity'], key, currency['bid'] * currency['quantity'],"\033[0m")
	print("\033[91m",time.strftime('%H:%M'),"SELL ", currency['quantity'], key, currency['ask'] * currency['quantity'],"\033[0m")
	askPrice = currency['ask'] - currency['ask'] * Config.StockFee
	bidPrice =  currency['bid'] + currency['bid'] * Config.StockFee
	profit = (askPrice - bidPrice)/bidPrice
	print("\033[96m+", profit, "\033[0m")