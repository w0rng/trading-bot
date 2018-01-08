import HitBtcApi
import Config
import json
from types import SimpleNamespace as Namespace
import sys

def GetMainBalance(keys, quotedCurrency):
	try:
		balances = HitBtcApi.GetBalance(keys, quotedCurrency)
		for balance in balances:
			if balance['currency'] == quotedCurrency:
				return float(balance['available'])
	except:
		print("ERROR GetMainBalance")
		print(sys.exc_info()[1].args[0])

def GetNotZeroBalances(keys, quotedCurrency):
	try:
		allBalance = HitBtcApi.GetBalance(keys, quotedCurrency)
		notZeroBalance = []
		for balance in allBalance:
			if ((balance['available'] != '0') or (balance['reserved'] != '0')) and (balance['currency'] != quotedCurrency):
				notZeroBalance.append(balance)
		return notZeroBalance
	except:
		print("ERROR GetNotZeroBalances")
		print(sys.exc_info()[1].args[0])

def GetAllOrders(keys):
	return HitBtcApi.GetOrders(keys)

def GetTickers():
	try:
		AllTicker = HitBtcApi.GetTickers()
		Traded = []
		for Ticker in AllTicker:
			if ((Ticker['bid'] != None) and
			((float(Ticker['ask']) + float(Ticker['ask']) * (Config.StockFee + Config.Profit) >= float(Ticker['bid']) + float(Ticker['bid']) * Config.StockFee)) and
			(Ticker['symbol'].find(Config.QuotedCurrency) != -1)):
				ask = float(Ticker['ask'])
				bid = float(Ticker['bid'])
				volume = float(Ticker['volume'])
				rank = ((ask - bid)/bid)*volume

				temp = json.loads(Config.Mask, object_hook=lambda d: Namespace(**d))
				temp.symbol = Ticker['symbol']
				temp.ask = ask
				temp.bid = bid
				temp.rank = rank
				temp.quantityIncrement = float(HitBtcApi.GetInfoSumbols(temp.symbol)['quantityIncrement'])
				Traded.append(temp)

		Traded.sort(reverse=True, key=lambda t: t.rank)
		return Traded
	except:
		print("ERROR GetTickers")
		print(sys.exc_info()[1].args[0])