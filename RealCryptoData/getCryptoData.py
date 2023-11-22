import requests
import json

class CryptoData:
    url = "https://api.coinlore.net/api/tickers/?start=0&limit=500"

    @classmethod
    def get_cryptocurrencies(cls):
        response = requests.get(cls.url)
        data = json.loads(response.text)
        cryptoData = data['data']
        return cryptoData
