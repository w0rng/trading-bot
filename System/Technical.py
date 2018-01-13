from decimal import Decimal, getcontext

typeNumbers = (float, int, Decimal)


def _NumberCheck(str):
    try:
        if type(str) in typeNumbers:
            return True
        if '.' in str:
            str = str.replace('.', '', 1)
        str = str.lstrip('-')
        return str.isdigit()
    except:
        return None


def _Convert(d):
    for key in d:
        if _NumberCheck(d[key]):
            value = Decimal(d[key])
            value = value.quantize(Decimal('1.00000'))
            d[key] = value.normalize()
    return d


def ConvertFloatToDecimal(func):
    def warp(*args):
        temp = func(*args)
        if type(temp) is dict:
            return _Convert(temp)
        else:
            for index in range(len(temp)):
                temp[index] = _Convert(temp[index])
        return temp
    return warp
