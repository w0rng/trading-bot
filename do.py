import HitBtcApi
import Config

def CancelOrders(keys, orders):
	for order in orders:
		if order['side'] == 'buy':
			HitBtcApi.CancelOrders(keys, order['clientOrderId'])

def SortCurrencyTraded(Traded):
	a = Traded
	a = sorted(a,reverse=True, key=lambda t: t[3])

	i = 0
	while i < len(a):
		if (a[i][3] < 0.5) or (float(HitBtcApi.GetInfoSumbols(a[i][0])['quantityIncrement']) > Config.MaxPrice / float(a[i][1])) or (a[i][0].find(Config.QuotedCurrency) == -1):
			del a[i]
		else:
			i += 1
	print(a)