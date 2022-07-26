import requests
import json
from config import keys


class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, basec: str, amount: str):
        if quote == basec:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {basec}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            basec_ticker = keys[basec]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {basec}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://api.exchangeratesapi.io/latest?base={quote_ticker}')
        total_base = json.loads(r.content)['rates'][basec_ticker]

        return total_base