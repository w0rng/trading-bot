import math
import json
from System.Technical import convert_float_to_decimal


@convert_float_to_decimal
def get_config(config_name):
    file = open('Configs/%s.conf' % config_name)
    config = json.load(file)
    file.close()
    return config


def get_balance(get_balance, quoted_currency):
    accounts = get_balance(quoted_currency)
    other_balance = {}
    main_balance = 0
    for balance in accounts:
        if balance['currency'] == quoted_currency:
            main_balance = balance['available']
        elif balance['reserved'] or balance['available']:
            other_balance.update(
                {
                    balance['currency']:
                        (balance['reserved'], balance['available'])
                })
    return main_balance, other_balance


def check_price_currency(ask, bid, config):
    if not (ask and bid):
        return False
    ask_price = ask - ask*config['StockFee']
    bid_price = bid + bid*config['StockFee']
    profit = (ask_price-bid_price) / bid_price * 100
    return (profit >= config['Profit']) and (bid >= config['MinPrice'])


def generate_info_symbol(symbol, ask, bid, volume, api, config, max_price):
    rank = (ask-bid) / bid*volume
    if rank >= config["MinRank"]:
        quantity_increment = api.GetInfoSumbols(symbol)['quantityIncrement']
        if quantity_increment <= (max_price / bid):
            return {
                'ask': ask,
                'bid': bid,
                'rank': rank,
                'quantityIncrement': quantity_increment
            }


def get_tickers(api, config, max_price):
    all_ticker = api.GetTickers()
    traded = {}
    for Ticker in all_ticker:
        if (Ticker['bid'] is None) or \
                (config['QuotedCurrency'] not in Ticker['symbol']):
            continue
        symbol = Ticker['symbol']
        ask = Ticker['ask']
        bid = Ticker['bid']
        if check_price_currency(ask, bid, config):
            traded[symbol] = generate_info_symbol(
                symbol,
                ask,
                bid,
                Ticker['volume'],
                api,
                config,
                max_price
            )
    return traded


def buy_currency(traded_currency, max_price, create_orders):
    for key in list(traded_currency):
        currency = traded_currency[key]
        quantity = \
            math.trunc(
                max_price /
                currency['bid'] /
                currency['quantityIncrement']) * \
            currency['quantityIncrement']
        create_orders(key, "buy", quantity, currency['bid'])
    return {}


def sell_currency(traded_currency, create_orders):
    for key in list(traded_currency):
        currency = traded_currency[key]
        print(currency)
        create_orders(key, "sell", currency['quantity'], currency['ask'])
    return {}
