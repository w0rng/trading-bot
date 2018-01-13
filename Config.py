from decimal import Decimal

PublicKey = "***REMOVED***"
SecretKey = "***REMOVED***"

QuotedCurrency = 'USD' #Котируемая валюта
Quantity = 4 #Колисчество валютных пар для торговли
Profit = Decimal(0.03) #необходимая прибыль в % с 1 сделки (0.01 = 1%)
StockFee = Decimal(0.001) #комиссия биржи (0.01 = 1%)
Period = 60 #Периуд за который брать информацию о валюте (1 = 1мин)
Sleep = 120 #время ожидания бота (1 = 1 сек)
MinRank = Decimal(2000) #минимальный ранг торгуемых валют
MinDegree = 15 #минимальный градус наклона рынка, при котором можно покупать валюту
MaxDegree = 45 #максимальный градус рынка, при котором можно покупать валюту
MinPrice = Decimal(0.01) #Минимальная цена за 1 валюту

#DON'T TOUCH!
Balance = {}
MaxPrice = Decimal(0)
MainBalance = Decimal(0)
TradedCurrency = {}