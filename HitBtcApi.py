import requests

session = requests.session()

def GetBalance(keys, quotedCurrency):
	session.auth = (keys[0], keys[1])
	return session.get('https://api.hitbtc.com/api/2/trading/balance').json()

def GetOrders(keys):
	session.auth = (keys[0], keys[1])
	return session.get('https://api.hitbtc.com/api/2/order').json()

def CancelOrders(keys, clientOrderId):
	session.auth = (keys[0], keys[1])
	session.delete('https://api.hitbtc.com/api/2/order/'+clientOrderId)