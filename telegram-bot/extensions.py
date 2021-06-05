from datetime import datetime

import requests
import json
import lxml.html

from collections import defaultdict

class ConvertionExceprion(Exception):
    pass

class UserInfo:

    ''' Информация о пользователя '''

    def __init__(self):
        self.f = "RUB"
        self.t = "USD"

class UserDB:

    ''' База даных для пользователий '''

    def __init__(self):
        self.db = defaultdict(UserInfo)

    def change_from(self, user_id, val):
        self.db[user_id].f = val

    def change_too(self, user_id, val):
        self.db[user_id].t = val

    def get_pair(self, user_id):
        user = self.db[user_id]
        return user.f, user.t

class CryptoConverter:

    ''' Обработка исключений функции get_values '''

    @staticmethod
    def convert(values):
        if len(values) != 3:
            raise ConvertionExceprion('Слишком много параметров')
        quote, base, amount = values

        if quote == base:
            raise ConvertionExceprion(f'Невозможно перевести одинкаовые валюты {base}')

        quote_ticker = quote
        base_ticker = base

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExceprion(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total = float(json.loads(r.content)[base_ticker])*amount

        return round(total, 3)

class VGPrice:

    @staticmethod
    def get_vg_price():
        html = requests.get('https://quote.rbc.ru/ticker/306109').content
        tree = lxml.html.document_fromstring(html)
        vg = tree.xpath(
            '/html/body/div[7]/div[4]/div[2]/div[1]/div[3]/div/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/span[1]/text()'
                        )[1].replace(',', '.')
        current_datetime = datetime.now().date()
        lifting_percentage = tree.xpath(
            '/html/body/div[7]/div[4]/div[2]/div[1]/div[3]/div/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/span[2]/text()'
        )
        lifting_percentage = '\n'.join(lifting_percentage).replace(' ', '').split()
        lifting_percentage = ''.join(lifting_percentage)
        text = f'Цена Virgin Galactic на {current_datetime} состовляет - {vg} USD {lifting_percentage}'
        return text


if __name__ == '__main__':
    pass
