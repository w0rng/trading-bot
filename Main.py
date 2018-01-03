import Logics
import Config
import GetInformations
import do
import time

maxPrice = 0
inf = GetInformations
keys = [Config.PublicKey, Config.SecretKey]

def main():
	while True:
		do.CancelOrders(keys, inf.GetAllOrders(keys))
		Config.Balance = inf.GetNotZeroBalances(keys, Config.QuotedCurrency)
		Config.MainBalance = inf.GetMainBalance(keys, Config.QuotedCurrency)

		print(Config.MainBalance)

		time.sleep(10)

if __name__ == '__main__':
	main()