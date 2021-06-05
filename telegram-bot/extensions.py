import requests
import json

import config as cnf


class ConvertionExceprion(Exception):
    pass

class CryptoConverter:

    ''' Обработка исключений функции get_values '''

    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionExceprion(f'Невозможно перевести одинкаовые валюты {base}')

        try:
            quote_ticker = cnf.KEYS[quote]
        except KeyError:
            raise ConvertionExceprion(f'Не удалось найти валюту {quote}')

        try:
            base_ticker = cnf.KEYS[base]
        except KeyError:
            raise ConvertionExceprion(f'Не удалось найти валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExceprion(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[cnf.KEYS[base]]

        return total_base*amount




if __name__ == '__main__':
    pass