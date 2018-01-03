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
		#do.CancelOrders(keys, inf.GetAllOrders(keys))
		#Config.Balance = inf.GetNotZeroBalances(keys, Config.QuotedCurrency)
		Config.MainBalance = inf.GetMainBalance(keys, Config.QuotedCurrency)
		Config.MaxPrice = Config.MainBalance / Config.Quantity

		print(Config.MaxPrice)

		Config.TradedCurrency = do.SortCurrencyTraded(GetInformations.GetTickers())

		time.sleep(10)

if __name__ == '__main__':
	main()