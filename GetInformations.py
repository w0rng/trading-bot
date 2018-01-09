import HitBtcApi
import Config
from Currency import Currency
import sys

def GetBalance(keys, quotedCurrency):
	_balances = HitBtcApi.GetBalance(keys, quotedCurrency)
	main = 0
	balances = []
	for balance in _balances:
		if balance['currency'] == quotedCurrency:
			main = float(balance['available'])
		elif (balance['available'] != '0') | (balance['reserved'] != '0'):
			balances.append(balance)
	return(main, balances)

def GetAllOrders(keys):
	return HitBtcApi.GetOrders(keys)

def GetTickers():
	try:
		AllTicker = HitBtcApi.GetTickers()
		Traded = []
		for Ticker in AllTicker:
			if (Ticker['bid'] == None) | (Ticker['symbol'].find(Config.QuotedCurrency) == -1):
				continue
			
			symbol = Ticker['symbol']
			ask = float(Ticker['ask'])
			bid = float(Ticker['bid'])

			askPrice = ask + ask * (Config.StockFee + Config.Profit)
			bidPrice =  bid + bid * Config.StockFee

			if (askPrice > bidPrice):
				rank = ((ask - bid)/bid)*float(Ticker['volume'])
				quantityIncrement = float(HitBtcApi.GetInfoSumbols(symbol)['quantityIncrement'])
				Traded.append(Currency(Ticker['symbol'], ask, bid, rank, quantityIncrement))

		Traded.sort(reverse=True, key=lambda t: t.rank)
		return Traded
	except:
		print("ERROR GetTickers")
		print(sys.exc_info()[1].args[0])