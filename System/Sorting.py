import math
import time
from decimal import Decimal

import numpy as np


def remove_buy_order(order, cancel_orders):
    cancel_orders(order['clientOrderId'])
    if order['status'] == 'new':
        return False
    elif order['status'] == 'partiallyFilled':
        return order['cumQuantity']


def check_stop_loss(order, price, api, stop_loss):
    if price <= (order['price'] - order['price'] * stop_loss):
        api.CancelOrders(order['clientOrderId'])
        api.CreateOrders(order['symbol'], "sell", order['quantity'], price)


def check_stop_time(order, price, api, stop_time):
    time_order_temp = time.strptime(
        order['createdAt'], "%Y-%m-%dT%H:%M:%S.%fZ")
    time_order = time.mktime(time_order_temp)
    now_time = time.time()
    if time_order - now_time <= stop_time:
        api.CancelOrders(order['clientOrderId'])
        api.CreateOrders(order['symbol'], "sell", order['quantity'], price)


def scaling_of_coordinates(x, y):
    k = max(x) / max(y)
    y = [y[i] * k for i in range(len(y))]
    k = min(y)
    y = [y[i] - k for i in range(len(y))]
    k = max(y) / max(x)
    x = [x[i] * k for i in range(len(x))]

    return x, y


def get_price_peaks(x, y, fit_fn, func):
    f = func(y)
    r = fit_fn(x)[y.index(f)] - f
    r -= r * 0.1
    return Decimal(fit_fn(x)[len(x) - 1] - r)


def get_information_market(symbol, get_candles, period):
    try:
        candles = get_candles(symbol, period)

        x = range(len(candles))
        y = [float((candle['open'] + candle['close']) / 2)
             for candle in candles]
        x, y = scaling_of_coordinates(x, y)

        fit = np.polyfit(x, y, 1)
        fit_fn = np.poly1d(fit)
        degree = math.degrees(math.atan(fit_fn[1]))

        min_price = get_price_peaks(x, y, fit_fn, min)
        max_price = get_price_peaks(x, y, fit_fn, max)

        return degree, min_price, max_price
    except:
        return None


def sorted_orders(traded_currency, api, config):
    orders = api.GetOrders()
    for order in orders:
        if config["QuotedCurrency"] in order['symbol']:
            if order['side'] == 'buy':
                if new_price := remove_buy_order(order, api.CancelOrders):
                    traded_currency[order['symbol']]['quantity'] = new_price
                else:
                    traded_currency.pop(order['symbol'])
            elif order['side'] == 'sell':
                price = api.GetTicker(order['symbol'])['ask']
                if config["StopLoss"]:
                    check_stop_loss(order, price, api, config['StopLoss'])
                if config["StopTime"]:
                    check_stop_time(order, price, api, config['StopTime'])
    return traded_currency


def remove_bad_currency(traded_currency, balance, config):
    for key in list(traded_currency):
        if key.replace(config["QuotedCurrency"], "") in balance:
            traded_currency.pop(key)
        elif not traded_currency[key]:
            traded_currency.pop(key)
    return traded_currency


def remove_bad_markets(traded_currency, config, api):
    for key in list(traded_currency):
        information = get_information_market(
            key,
            api.GetCandles,
            config['Period']
        )

        if information is None:
            traded_currency.pop(key)
            continue

        degree, min_price, max_price = information
        # currency = TradedCurrency[key]

        if (degree < config["MinDegree"]) or (degree > config["MaxDegree"]):
            traded_currency.pop(key)
        # elif (currency['ask'] < min_price) or (currency['ask'] > max_price):
        #    TradedCurrency.pop(key)

    return traded_currency


def chopping(traded_currency, balance, quantity):
    traded_currency = dict(
        sorted(traded_currency.items(), key=lambda t: t[1]['rank']))
    n = int(quantity - len(balance))
    if traded_currency:
        return {key: traded_currency[key]
                for key in list(traded_currency.keys())[:n]}
    else:
        return {}
