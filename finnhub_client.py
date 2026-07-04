# ==========================================
# AIF Pivot Scanner
# finnhub_client.py
# ==========================================

import requests
import time
from config import FINNHUB_API_KEY

BASE_URL = "https://finnhub.io/api/v1"


class FinnhubClient:

    def __init__(self):
        self.api_key = FINNHUB_API_KEY

    def _request(self, endpoint, params=None):

        if params is None:
            params = {}

        params["token"] = self.api_key

        url = f"{BASE_URL}/{endpoint}"

        try:

            response = requests.get(url, params=params, timeout=15)

            if response.status_code == 200:
                return response.json()

            elif response.status_code == 429:
                print("⚠️ Rate Limit... waiting")
                time.sleep(3)
                return None

            else:
                print(f"HTTP Error : {response.status_code}")
                return None

        except Exception as e:
            print("Connection Error:", e)
            return None

    # ============================
    # Quote
    # ============================

    def get_quote(self, symbol):

        return self._request(
            "quote",
            {
                "symbol": symbol
            }
        )

    # ============================
    # Company Profile
    # ============================

    def get_company(self, symbol):

        return self._request(
            "stock/profile2",
            {
                "symbol": symbol
            }
        )

    # ============================
    # Candles
    # ============================

    def get_candles(
        self,
        symbol,
        resolution,
        start,
        end
    ):

        return self._request(
            "stock/candle",
            {
                "symbol": symbol,
                "resolution": resolution,
                "from": start,
                "to": end
            }
        )


client = FinnhubClient()
