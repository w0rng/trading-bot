import Logics
import Config
import GetInformations
import do
import time

inf = GetInformations
keys = [Config.PublicKey, Config.SecretKey]
def main():
	while True:
		orders = inf.GetAllOrders(keys)
		print(orders)
		do.CancelOrders(keys, orders)
		#balance = inf.GetNotZeroBalances([Config.PublicKey, Config.SecretKey], Config.QuotedCurrency)
		time.sleep(10)

if __name__ == '__main__':
	main()