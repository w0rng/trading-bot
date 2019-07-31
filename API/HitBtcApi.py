import requests
from System.Technical import ConvertFloatToDecimal


class HitBtcAPI:
    def __init__(self, publicKey, secretKey):
        self.session = requests.session()
        self.UrlAPI = "https://api.hitbtc.com/api/2/%s"
        self.session.auth = (publicKey, secretKey)

    @ConvertFloatToDecimal
    def GetBalance(self, quotedCurrency):
        return self.session.get(self.UrlAPI % 'trading/balance').json()

    @ConvertFloatToDecimal
    def GetOrders(self):
        return self.session.get(self.UrlAPI % 'order').json()

    @ConvertFloatToDecimal
    def CancelOrders(self, clientOrderId):
        return self.session.delete(
            self.UrlAPI % 'order/%s' % clientOrderId).json()

    @ConvertFloatToDecimal
    def CreateOrders(self, symbol, side, quantity, price):
        print(side, quantity, symbol, price)

        orderData = {
            'symbol': symbol,
            'side': side,
            'quantity': quantity,
            'price': price
        }
        return self.session.post(self.UrlAPI % 'order', data=orderData).json()

    @ConvertFloatToDecimal
    def GetTickers(self):
        return self.session.get(self.UrlAPI % 'public/ticker').json()

    @ConvertFloatToDecimal
    def GetTicker(self, symbol):
        return self.session.get(self.UrlAPI % 'public/ticker/'+symbol).json()

    @ConvertFloatToDecimal
    def GetInfoSumbols(self, symbol):
        return self.session.get(
            self.UrlAPI % 'public/symbol/%s' % symbol).json()

    @ConvertFloatToDecimal
    def GetCandles(self, symbol, limit):
        limit = float(limit)
        return self.session.get(
            self.UrlAPI %
            'public/candles/%s?limit=%s&period=M1' %
            (symbol, limit)).json()
