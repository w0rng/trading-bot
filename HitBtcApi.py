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

def CreateOrders(keys, symbol, side, quantity, price):
    session.auth = (keys[0], keys[1])
    orderData = {'symbol': symbol, 'side': side, 'quantity': quantity, 'price': price}
    return session.post('https://api.hitbtc.com/api/2/order', data = orderData).json()

def GetTickers():
	return session.get('https://api.hitbtc.com/api/2/public/ticker').json()

def GetInfoSumbols(symbol):
	return session.get('https://api.hitbtc.com/api/2/public/symbol/'+symbol).json()

def GetCandles(symbol, limit):
	return session.get('https://api.hitbtc.com/api/2/public/candles/'+symbol+'?limit='+str(limit)+'&period=M1').json()