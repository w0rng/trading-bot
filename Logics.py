import numpy
import talib

BEAR_PERC = 95
BULL_PERC = 30

def should_buy(Candles):
    data = Candles
    quotes = {}
    quotes['close']=numpy.asarray([float(item['close']) for item in data])
    macd, macdsignal, macdhist = talib.MACD(quotes['close'], fastperiod=12, slowperiod=26, signalperiod=9)

    idx = numpy.argwhere(numpy.diff(numpy.sign(macd - macdsignal)) != 0).reshape(-1) + 0

    inters = []

    for offset, elem in enumerate(macd):
        if offset in idx:
            inters.append(elem)
        else:
            inters.append(numpy.nan)

    hist_data = []
    max_v = 0

    for offset, elem in enumerate(macdhist):
        activity_time = False
        curr_v = macd[offset] - macdsignal[offset]
        if abs(curr_v) > abs(max_v):
            max_v = curr_v
        perc = curr_v/max_v
        
        if((macd[offset] > macdsignal[offset] and perc*100 > BULL_PERC) # восходящий тренд
        | (macd[offset] < macdsignal[offset] and perc*100 < 100-BEAR_PERC)):
            v = 1
            activity_time = True
        else:
            v = 0
            
        if offset in idx & (not numpy.isnan(elem)):
            # тренд изменился
            max_v = curr_v = 0 # обнуляем пик спреда между линиями
        hist_data.append(v*1000)
 
    return activity_time