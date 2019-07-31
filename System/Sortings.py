import math
import time
from datetime import datetime
from decimal import Decimal
from itertools import islice

import numpy as np


def RemoveBuyOrder(order, CancelOrders):
    CancelOrders(order['clientOrderId'])
    if order['status'] is 'new':
        return False
    elif order['status'] is 'partiallyFilled':
        return order['cumQuantity']


def CheckStopLoss(order, price, api, StopLoss):
    stopLoss = order['price'] - order['price']*StopLoss
    if price <= stopLoss:
        api.CancelOrders(order['clientOrderId'])
        api.CreateOrders(order['symbol'], "sell", order['quantity'], price)


def CheckStopTime(order, price, api, StopTime):
    timeOrderTemp = time.strptime(order['createdAt'], "%Y-%m-%dT%H:%M:%S.%fZ")
    timeOrder = time.mktime(timeOrderTemp)
    nowTime = time.time()
    if(timeOrder - nowTime <= StopTime):
        api.CancelOrders(order['clientOrderId'])
        api.CreateOrders(order['symbol'], "sell", order['quantity'], price)


def ScalingOfCoordinates(x, y):
    k = max(x) / max(y)
    y = [y[i]*k for i in range(len(y))]
    k = min(y)
    y = [y[i] - k for i in range(len(y))]
    k = max(y) / max(x)
    x = [x[i] * k for i in range(len(x))]

    return (x, y)


def GetPricePeaks(x, y, fit_fn, funct):
    Y = funct(y)
    r = fit_fn(x)[y.index(Y)] - Y
    r -= r * 0.1
    return Decimal(fit_fn(x)[len(x) - 1] - r)


def GetInformationMarket(symbol, GetCandles, Period):
    try:
        candles = GetCandles(symbol, Period)

        x = range(len(candles))
        y = [float((candle['open']+candle['close'])/2) for candle in candles]
        x, y = ScalingOfCoordinates(x, y)

        fit = np.polyfit(x, y, 1)
        fit_fn = np.poly1d(fit)
        degree = math.degrees(math.atan(fit_fn[1]))

        minPrice = GetPricePeaks(x, y, fit_fn, min)
        maxPrice = GetPricePeaks(x, y, fit_fn, max)

        return (degree, minPrice, maxPrice)
    except:
        return None


def SortedOrders(TradedCurrency, api, config):
    orders = api.GetOrders()
    for order in orders:
        if config["QuotedCurrency"] in order['symbol']:
            if order['side'] is 'buy':
                newPrice = RemoveBuyOrder(order, api.CancelOrders)
                if newPrice:
                    TradedCurrency[order['symbol']]['quantity'] = newPrice
                else:
                    TradedCurrency.pop(order)
            elif order['side'] is 'sell':
                price = api.GetTicker(order['symbol'])['ask']
                if config["StopLoss"]:
                    CheckStopLoss(order, price, api, config['StopLoss'])
                if config["StopTime"]:
                    CheckStopTime(order, price, api, config['StopTime'])
    return TradedCurrency


def RemoveBadCurrencys(TradedCurrency, Balance, config):
    for key in list(TradedCurrency):
        if key.replace(config["QuotedCurrency"], "") in Balance:
            TradedCurrency.pop(key)
        elif not TradedCurrency[key]:
            TradedCurrency.pop(key)
    return TradedCurrency


def RemoveBadMarkets(TradedCurrency, config, api):
    for key in list(TradedCurrency):
        informations = GetInformationMarket(
            key,
            api.GetCandles,
            config['Period']
        )

        if informations is None:
            TradedCurrency.pop(key)
            continue

        degree, minPrice, maxPrice = informations
        currency = TradedCurrency[key]

        if (degree < config["MinDegree"]) or (degree > config["MaxDegree"]):
            TradedCurrency.pop(key)
        elif (currency['ask'] < minPrice) or (currency['ask'] > maxPrice):
            TradedCurrency.pop(key)

    return TradedCurrency


def Chopping(TradedCurrency, Balance, Quantity):
    TradedCurrency = dict(
        sorted(TradedCurrency.items(), key=lambda t: t[1]['rank']))
    n = Quantity - len(Balance)
    if TradedCurrency:
        return TradedCurrency.items()[:n]
    else:
        return {}
