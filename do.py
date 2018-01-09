import HitBtcApi
import Config
import Logics
import numpy as np
import math
import time

def SortedOrders(keys, orders):
	for order in orders:
		if (order['side'] == 'buy') & (order['status'] == 'new'):
			for currency in Config.TradedCurrency[:]:
				if currency.symbol == order['symbol']:
					Config.TradedCurrency.remove(currency)
					break
			HitBtcApi.CancelOrders(keys, order['clientOrderId'])

def RemoveBadCurrencys():
	for currency in Config.TradedCurrency[:]:
		if (currency.rank < Config.MinRank) | (currency.quantityIncrement > Config.MaxPrice / currency.bid):
			Config.TradedCurrency.remove(currency)
		else:
			for b in  Config.Balance:
				if b['currency'] + Config.QuotedCurrency == currency.symbol:
					Config.TradedCurrency.remove(currency)
					break

def RemoveBadMarkets():
	for currency in Config.TradedCurrency[:]:
		candles = HitBtcApi.GetCandles(currency.symbol, Config.Period)

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
				
			if (currency.ask < minPrice) | (currency.ask > maxPrice):
				Config.TradedCurrency.remove(currency)

def SellCurrencys(keys):
	for currency in Config.TradedCurrency[:]:
		informations(currency)
		HitBtcApi.CreateOrders(keys, currency.symbol, "sell", currency.quantity, currency.ask)
	Config.TradedCurrency.clear()

def BuyCurrencys(keys):
	temp = []
	maxIndex = min(Config.Quantity - len(Config.Balance), len(Config.TradedCurrency))
	for i in range(maxIndex):
		currency = Config.TradedCurrency[i]
		currency.quantity = math.trunc(Config.MaxPrice / currency.bid / currency.quantityIncrement) * currency.quantityIncrement
		HitBtcApi.CreateOrders(keys, currency.symbol, "buy", currency.quantity, currency.bid)
		temp.append(currency)
	Config.TradedCurrency = temp

def informations(currency):
	print("\033[92m",time.strftime('%H:%M'),"BUY ", currency.quantity, currency.symbol, currency.bid * currency.quantity,"\033[0m")
	print("\033[91m",time.strftime('%H:%M'),"SELL ", currency.quantity, currency.symbol, currency.ask * currency.quantity,"\033[0m")
	profit = (currency.ask * currency.quantity - currency.bid * currency.quantity)
	StockFee = currency.ask * currency.quantity * Config.StockFee + currency.bid * currency.quantity * Config.StockFee
	print("\033[96m+", profit-StockFee, "\033[0m")