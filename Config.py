PublicKey = "***REMOVED***"
SecretKey = "***REMOVED***"

QuotedCurrency = 'USD' #Котируемая валюта
Quantity = 5 #Колисчество валютных пар для торговли
Profit = 0.01 #необходимый навар (0.01 = 1%)
StockFee = 0.01 #комиссия биржи (0.01 = 1%)
Period = 60 #время для расчетов (1 = 1 мин)
Sleep = 10 #время ожидания бота (1 = 1 сек)
MinRank = 1000 #минимальный ранг торгуемых валют

#Private setings
Balance = [] #Баланс
MainBalance = 0 #Баланс котируемой валюты
MaxPrice = 0 #Максимальная цена
TradedCurrency = [] #Валюты для торговли
Orders = [] #Ордера ??
Mask = '{"symbol": "text", "ask": 0, "bid": 0, "rank": 0, "quantityIncrement": 0}' #Объект валюты на продажу