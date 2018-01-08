import HitBtcApi
import Config
import Logics
import numpy as np
import math
import time
import sys

def SortedOrders(keys, orders):
	try:
		currencys = Config.TradedCurrency
		purchasedCurrencies = currencys
		for order in orders:
			if (order['side'] == 'buy') and (order['status'] == 'new'):
				for currency in currencys:
					if currency.symbol == order['symbol']:
						purchasedCurrencies.remove(currency)
						break
				HitBtcApi.CancelOrders(keys, order['clientOrderId'])
		Config.TradedCurrency = purchasedCurrencies
	except:
		print("ERROR SortedOrders")
		print(sys.exc_info()[1].args[0])

def RemoveBadTradedCurrency():
	try:
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
	except:
		print("ERROR RemoveBadTradedCurrency")
		print(sys.exc_info()[1].args[0])

def RemoveBadMarketCurency():
	try:
		currencys = Config.TradedCurrency
		goodCurrency = []
		for currency in currencys:
			candles = HitBtcApi.GetCandles(currency.symbol, Config.Period)

			y = [(float(candle['open']) + float(candle['close']))/2 for candle in candles]
			x = range(0, len(candles))

			fit = np.polyfit(x,y,1)
			fit_fn = np.poly1d(fit)
			Degree = math.degrees(math.atan(fit_fn[1]))

			if (Logics.should_buy(candles)) and (Degree >= Config.MinDegree) and (Degree <= Config.MaxDegree):
				minY = min(y)
				r = fit_fn(x)[y.index(minY)] - minY
				r -= r * 0.1
				minPrice = float(fit_fn(x)[len(x) - 1] - r)
				
				if currency.ask >= minPrice:
					goodCurrency.append(currency)
		Config.TradedCurrency = goodCurrency
	except:
		print("ERROR RemoveCurencyBadMarket")
		print(sys.exc_info()[1].args[0])

def SellCurrencys(keys):
	try:
		currencys = Config.TradedCurrency
		for currency in currencys:
			print("\033[92m",time.strftime('%H:%M'),"BUY ", currency.quantity, currency.symbol, currency.bid * currency.quantity,"\033[0m")
			HitBtcApi.CreateOrders(keys, currency.symbol, "sell", currency.quantity, currency.ask)
			print("\033[91m",time.strftime('%H:%M'),"SELL ", currency.quantity, currency.symbol, currency.ask * currency.quantity,"\033[0m")
			profit = (currency.ask * currency.quantity - currency.bid * currency.quantity)
			StockFee = currency.ask * currency.quantity * Config.StockFee + currency.bid * currency.quantity * Config.StockFee
			print("\033[96m+", profit-StockFee, "\033[0m")
		Config.TradedCurrency.clear()
	except:
		print("ERROR SellCurrencys")
		print(sys.exc_info()[1].args[0])

def BuyCurrencys(keys):
	try:
		currencys = Config.TradedCurrency
		temp = []
		maxIndex = min(Config.Quantity - len(Config.Balance), len(currencys))
		for i in range(0, maxIndex):
			currency = currencys[i]
			currency.quantity = math.trunc(Config.MaxPrice / currency.bid / currency.quantityIncrement) * currency.quantityIncrement
			HitBtcApi.CreateOrders(keys, currency.symbol, "buy", currency.quantity, currency.bid)
			temp.append(currency)

		Config.TradedCurrency = temp
	except:
		print("ERROR BuyCurrencys")
		print(sys.exc_info()[1].args[0])