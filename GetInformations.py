import HitBtcApi

def GetMainBalance(keys, quotedCurrency):
	balances = HitBtcApi.GetBalance(keys, quotedCurrency)
	for balance in balances:
		if balance['currency'] == quotedCurrency:
			return balance

def GetNotZeroBalances(keys, quotedCurrency):
	allBalance = HitBtcApi.GetBalance(keys, quotedCurrency)
	notZeroBalance = []
	for balance in allBalance:
		if (balance['available'] != '0') and (balance['currency'] != quotedCurrency):
			notZeroBalance.append(balance)
	return notZeroBalance

def GetAllOrders(keys):
	return HitBtcApi.GetOrders(keys)