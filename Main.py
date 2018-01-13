from decimal import Decimal
import Config
import GetInformations
import do
import time

keys = [Config.PublicKey, Config.SecretKey]

def main():
	print("RUN")
	while True:
		do.SortedOrders(keys)
		do.SellCurrencys(keys)
		GetInformations.GetBalance(keys)
		if len(Config.Balance) < Config.Quantity:
			Config.MaxPrice = Decimal(Config.MainBalance / (Config.Quantity - len(Config.Balance)))
			GetInformations.GetTickers()
			do.RemoveBadCurrencys()
			do.RemoveBadMarkets()
			do.Chopping()
			do.BuyCurrencys(keys)
			print(time.strftime('%H:%M'), "MAIN BALANCE: ", Config.MainBalance)

		time.sleep(Config.Sleep)

if __name__ == '__main__':
	main()