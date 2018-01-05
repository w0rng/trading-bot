import Config
import GetInformations
import do
import time

maxPrice = 0
inf = GetInformations
keys = [Config.PublicKey, Config.SecretKey]

def main():
	while True:
		do.SortedOrders(keys, inf.GetAllOrders(keys)) #Удаляем ордера на покупку, добавляем в лист ордера на продажу
		Config.Balance = inf.GetNotZeroBalances(keys, Config.QuotedCurrency) #получение баланса всех валют, кроме котируемой
		if len(Config.Balance) < Config.Quantity: 
			Config.MainBalance = inf.GetMainBalance(keys, Config.QuotedCurrency) #получение баланса котируемой валюты
			Config.MaxPrice = Config.MainBalance / (Config.Quantity - len(Config.Orders)) #расчет максимальной цены за валюту
			Config.TradedCurrency = GetInformations.GetTickers() #Получение всех валют на покупку
			do.SortCurrencyTraded() #Поиск валют для покупки
			do.RemoveBadTradedCurrency() #удаление валют с падющим рынком
			#do.RemovalAvailableCurrencies()

		time.sleep(Config.sleep)

if __name__ == '__main__':
	main()