import Config
import GetInformations
import do
import time

inf = GetInformations
keys = [Config.PublicKey, Config.SecretKey]

def main():
	print("RUN")
	while True:
		do.SortedOrders(keys, inf.GetAllOrders(keys)) #Удаляем ордера на покупку, удаляем из массива не купленную валюту
		do.SellCurrencys(keys)
		Config.MainBalance, Config.Balance = inf.GetBalance(keys, Config.QuotedCurrency) # получаем баланс
		if len(Config.Balance) < Config.Quantity:
			Config.MaxPrice = Config.MainBalance / (Config.Quantity - len(Config.Balance)) #расчет максимальной цены за валюту
			print("MAX PRICE",Config.MaxPrice)
			Config.TradedCurrency = GetInformations.GetTickers() #Получение всех валют на покупку
			do.RemoveBadCurrencys() #удаление валют, не подходящих под условия отбора
			do.RemoveBadMarkets() #удаление валют с падающим рынком
			do.BuyCurrencys(keys) #покупаем
			print(time.strftime('%H:%M'), "MAIN BALANCE: ", Config.MainBalance)
		time.sleep(Config.Sleep)

if __name__ == '__main__':
	main()