from decimal import Decimal

typeNumbers = (float, int, Decimal)


def _number_check(num):
    try:
        if type(num) in typeNumbers:
            return True
        if '.' in num:
            num = num.replace('.', '', 1)
        num = num.lstrip('-')
        return num.isdigit()
    except:
        return None


def _convert(d):
    for key in d:
        if _number_check(d[key]):
            value = Decimal(d[key])
            value = value.quantize(Decimal('1.00000'))
            d[key] = value.normalize()
    return d


def convert_float_to_decimal(func):
    def warp(*args):
        temp = func(*args)
        if type(temp) is dict:
            return _convert(temp)
        else:
            for index in range(len(temp)):
                temp[index] = _convert(temp[index])
        return temp
    return warp
