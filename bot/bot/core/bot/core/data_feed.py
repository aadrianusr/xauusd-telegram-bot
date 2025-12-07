import requests

from bot.config import OANDA_API_KEY, OANDA_ACCOUNT_ID, FOREX_COM_API_KEY, PAIR


class DataFeed:
    def __init__(self):
        self.oanda_url = f"https://api-fxpractice.oanda.com/v3/instruments/{PAIR}/candles"
        self.forexcom_url = "https://ciapi.cityindex.com/tradingapi/market/"

    # -----------------------------
    # Ambil data dari OANDA
    # -----------------------------
    def get_oanda(self, timeframe="M1", count=100):
        headers = {
            "Authorization": f"Bearer {OANDA_API_KEY}"
        }

        params = {
            "granularity": timeframe,
            "count": count
        }

        try:
            r = requests.get(self.oanda_url, headers=headers, params=params, timeout=5)
            data = r.json()
            return data
        except:
            return None

    # -----------------------------
    # Ambil data dari FOREX.com
    # -----------------------------
    def get_forexcom(self):
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        try:
            r = requests.get(self.forexcom_url + "507", headers=headers, timeout=5)
            return r.json()
        except:
            return None

    # -----------------------------
    # Fallback otomatis
    # -----------------------------
    def get_price(self, timeframe="M1"):
        oanda = self.get_oanda(timeframe=timeframe)
        if oanda:
            return oanda

        forex = self.get_forexcom()
        if forex:
            return forex

        return None
