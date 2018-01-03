import HitBtcApi

def CancelOrders(keys, orders):
	for order in orders:
		if order['side'] == 'buy':
			HitBtcApi.CancelOrders(keys, order['clientOrderId'])