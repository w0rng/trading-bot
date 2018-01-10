import HitBtcApi
import Config
import sys

def GetBalance(keys):
	_balances = HitBtcApi.GetBalance(keys, Config.QuotedCurrency)
	main = 0
	balances = {}
	for balance in _balances:
		if balance['currency'] == Config.QuotedCurrency:
			Config.MainBalance = float(balance['available'])
		elif (balance['available'] != '0') | (balance['reserved'] != '0'):
			Config.Balance[balance['currency']] = {'available': balance['available'], 'reserved': balance['reserved']}
	return(main, balances)

def GetTickers():
	try:
		AllTicker = HitBtcApi.GetTickers()
		Traded = {}
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
				Traded[symbol] = {'ask': ask, 'bid': bid, 'rank': rank, 'quantityIncrement':quantityIncrement}

		Config.TradedCurrency = dict(sorted(Traded.items(), key=lambda t: t[1]['rank'], reverse=True))
	except:
		print("ERROR GetTickers")
		print(sys.exc_info()[1].args[0])