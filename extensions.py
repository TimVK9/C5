import requests
import json
from config import keys


class APIException(Exception):
    pass


class Convert:
    @staticmethod
    def get_price(base, quote, amount):

        if base == quote:
            raise APIException('Невозможно конвертировать!')

        try:
            value_ticker = keys[base]
        except KeyError:
            raise APIException(f'Невозможно обработать валюту - {base}')

        try:
            value_conv_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Невозможно обработать валюту - {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Невозможно обработать колличество - {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={value_ticker}&tsyms={value_conv_ticker}')
        j = float(json.loads(r.content)[keys[quote]]) * float(amount)

        return j
