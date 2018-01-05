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
			do.RemoveBadTradedCurrency() #удаление валют с падющим рынком
			do.RemoveCurencyFallingMarket() #Поиск валют для покупки

			t = Config.TradedCurrency
			for currency in t:
				print(currency.symbol, currency.rank)
		print('______')
		time.sleep(Config.Sleep)

if __name__ == '__main__':
	main()