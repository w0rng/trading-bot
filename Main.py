import Config
import GetInformations
import do
import time

maxPrice = 0
inf = GetInformations
keys = [Config.PublicKey, Config.SecretKey]

def main():
	print("RUN")
	while True:
		try:
			do.SortedOrders(keys, inf.GetAllOrders(keys)) #Удаляем ордера на покупку, удаляем из массива не купленную валюту
			do.SellCurrencys(keys)
			Config.Balance = inf.GetNotZeroBalances(keys, Config.QuotedCurrency) #получение баланса всех валют, кроме котируемой
			if len(Config.Balance) < Config.Quantity: 
				Config.MainBalance = inf.GetMainBalance(keys, Config.QuotedCurrency) #получение баланса котируемой валюты
				Config.MaxPrice = Config.MainBalance / (Config.Quantity - len(Config.Balance)) #расчет максимальной цены за валюту
				Config.TradedCurrency = GetInformations.GetTickers() #Получение всех валют на покупку
				do.RemoveBadTradedCurrency() #удаление валют, не подходящих под условия отбора
				do.RemoveCurencyFallingMarket() #удаление валют с падающим рынком
				do.BuyCurrencys(keys) #покупаем
				print(time.strftime('%H:%M'), "MAIN BALANCE: ", Config.MainBalance)

			time.sleep(Config.Sleep)
		except:
			print("ERROR main")
			time.sleep(Config.Sleep*5)

if __name__ == '__main__':
	main()