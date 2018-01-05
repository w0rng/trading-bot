import HitBtcApi
import Config
import json
from types import SimpleNamespace as Namespace
from decimal import Decimal

def GetMainBalance(keys, quotedCurrency):
	balances = HitBtcApi.GetBalance(keys, quotedCurrency)
	for balance in balances:
		if balance['currency'] == quotedCurrency:
			return Decimal(balance['available'])

def GetNotZeroBalances(keys, quotedCurrency):
	allBalance = HitBtcApi.GetBalance(keys, quotedCurrency)
	notZeroBalance = []
	for balance in allBalance:
		if ((balance['available'] != '0') or (balance['reserved'] != '0')) and (balance['currency'] != quotedCurrency):
			notZeroBalance.append(balance)
	return notZeroBalance

def GetAllOrders(keys):
	return HitBtcApi.GetOrders(keys)

def GetTickers():
	AllTicker = HitBtcApi.GetTickers()
	Traded = []
	for Ticker in AllTicker:
		if ((Ticker['bid'] != None) and
		(Decimal(Ticker['bid']) + Decimal(Ticker['bid']) * (Config.StockFee * 2 + Config.Profit)) >= Decimal(Ticker['ask']) and
		(Ticker['symbol'].find(Config.QuotedCurrency) != -1)):
			ask = Decimal(Ticker['ask'])
			bid = Decimal(Ticker['bid'])
			volume = Decimal(Ticker['volume'])
			rank = ((ask - bid)/bid)*volume

			temp = json.loads(Config.Mask, object_hook=lambda d: Namespace(**d))
			temp.symbol = Ticker['symbol']
			temp.ask = ask
			temp.bid = bid
			temp.rank = rank
			temp.quantityIncrement = Decimal(HitBtcApi.GetInfoSumbols(temp.symbol)['quantityIncrement'])
			Traded.append(temp)

	Traded.sort(reverse=True, key=lambda t: t.rank)
	return Traded