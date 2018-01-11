from decimal import Decimal
import HitBtcApi
import Config
import sys

def GetBalance(keys):
	_balances = HitBtcApi.GetBalance(keys, Config.QuotedCurrency)
	Config.Balance.clear()
	for balance in _balances:
		if balance['currency'] == Config.QuotedCurrency:
			Config.MainBalance = Decimal(balance['available'])
		elif (balance['reserved'] != '0') | (balance['available'] != '0'):
			Config.Balance.update({balance['currency']: None})

def GetTickers():
	try:
		AllTicker = HitBtcApi.GetTickers()
		Traded = {}
		for Ticker in AllTicker:
			if (Ticker['bid'] == None) | (Config.QuotedCurrency not in Ticker['symbol']):
				continue
			
			symbol = Ticker['symbol']
			ask = Decimal(Ticker['ask'])
			bid = Decimal(Ticker['bid'])

			askPrice = ask - ask * Config.StockFee
			bidPrice =  bid + bid * Config.StockFee
			profit = (askPrice - bidPrice)/bidPrice * 100

			if (profit >= Config.Profit) & (bid >= Config.MinPrice):
				rank = Decimal((ask - bid)/bid)*Decimal(Ticker['volume'])
				quantityIncrement = Decimal(HitBtcApi.GetInfoSumbols(symbol)['quantityIncrement'])
				Traded[symbol] = {'ask': ask, 'bid': bid, 'rank': rank, 'quantityIncrement':quantityIncrement}

		Config.TradedCurrency = dict(sorted(Traded.items(), key=lambda t: t[1]['rank'], reverse=True))
	except:
		print("ERROR GetTickers")
		print(sys.exc_info()[1].args[0])