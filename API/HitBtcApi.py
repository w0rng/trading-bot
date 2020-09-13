import requests
import datetime
from System.Technical import convert_float_to_decimal


class HitBtcAPI:
    def __init__(self, publicKey, secretKey):
        self.session = requests.session()
        self.UrlAPI = "https://api.hitbtc.com/api/2/%s"
        self.session.auth = (publicKey, secretKey)

    @convert_float_to_decimal
    def GetBalance(self, quotedCurrency):
        return self.session.get(self.UrlAPI % 'trading/balance').json()

    @convert_float_to_decimal
    def GetOrders(self):
        return self.session.get(self.UrlAPI % 'order').json()

    @convert_float_to_decimal
    def CancelOrders(self, clientOrderId):
        return self.session.delete(
            self.UrlAPI % 'order/%s' % clientOrderId).json()

    @convert_float_to_decimal
    def CreateOrders(self, symbol, side, quantity, price):
        print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
              side, quantity, symbol, price)

        orderData = {
            'symbol': symbol,
            'side': side,
            'quantity': quantity,
            'price': price
        }
        return self.session.post(self.UrlAPI % 'order', data=orderData).json()

    @convert_float_to_decimal
    def GetTickers(self):
        return self.session.get(self.UrlAPI % 'public/ticker').json()

    @convert_float_to_decimal
    def GetTicker(self, symbol):
        return self.session.get(self.UrlAPI % 'public/ticker/'+symbol).json()

    @convert_float_to_decimal
    def GetInfoSumbols(self, symbol):
        return self.session.get(
            self.UrlAPI % 'public/symbol/%s' % symbol).json()

    @convert_float_to_decimal
    def GetCandles(self, symbol, limit):
        limit = float(limit)
        return self.session.get(
            self.UrlAPI %
            'public/candles/%s?limit=%s&period=M1' %
            (symbol, limit)).json()
