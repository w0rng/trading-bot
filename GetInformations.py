import HitBtcApi
import Config

def GetMainBalance(keys, quotedCurrency):
	balances = HitBtcApi.GetBalance(keys, quotedCurrency)
	for balance in balances:
		if balance['currency'] == quotedCurrency:
			return float(balance['available'])

def GetNotZeroBalances(keys, quotedCurrency):
	allBalance = HitBtcApi.GetBalance(keys, quotedCurrency)
	notZeroBalance = []
	for balance in allBalance:
		if (balance['available'] != '0') and (balance['currency'] != quotedCurrency):
			notZeroBalance.append(balance)
	return notZeroBalance

def GetAllOrders(keys):
	return HitBtcApi.GetOrders(keys)

def GetTickers():
	AllTicker = HitBtcApi.GetTickers()
	Traded = []
	for Ticker in AllTicker:
		if (Ticker['bid'] != None) and (float(Ticker['bid']) + float(Ticker['bid']) * (Config.StockFee * 2 + Config.Profit)) >= float(Ticker['ask']):
			rank = (float(Ticker['ask']) - float(Ticker['bid']))/float(Ticker['bid'])*float(Ticker['volumeQuote'])
			temp = [float(Ticker['bid']), float(Ticker['ask']), Ticker['symbol'], rank]
			Traded.append(temp)
			print(temp)