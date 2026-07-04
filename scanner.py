# ==========================================
# AIF Pivot Scanner
# scanner.py
# ==========================================

import time
from datetime import datetime, timedelta

from finnhub_client import client
from market_filter import market_filter
from pivot_detector import pivot_detector
from scoring import score_calculator
from telegram_bot import telegram

# ==========================
# منع التكرار
# ==========================

last_alerts = {}

ALERT_COOLDOWN = 60 * 60  # ساعة


class PivotScanner:

    def __init__(self):
        self.symbols = []

    # ======================================
    # تحميل قائمة الأسهم
    # ======================================

    def load_symbols(self):

        print("Loading US Symbols...")

        data = client._request(
            "stock/symbol",
            {
                "exchange": "US"
            }
        )

        if not data:
            return []

        symbols = []

        for stock in data:

            symbol = stock.get("symbol", "")

            if symbol:
                symbols.append(symbol)

        print(f"Loaded {len(symbols)} Symbols")

        return symbols

    # ======================================
    # هل يسمح بإرسال التنبيه؟
    # ======================================

    def can_alert(self, symbol):

        now = time.time()

        if symbol not in last_alerts:
            last_alerts[symbol] = now
            return True

        if now - last_alerts[symbol] > ALERT_COOLDOWN:
            last_alerts[symbol] = now
            return True

        return False

    # ======================================
    # فحص سهم واحد
    # ======================================

    def scan_symbol(self, symbol):

        end_time = int(datetime.now().timestamp())

        start_time = int(
            (datetime.now() - timedelta(days=30)).timestamp()
        )

        candles = client.get_candles(
            symbol,
            "D",
            start_time,
            end_time
        )

        if not market_filter.is_valid_stock(candles):
            return

        closes = candles["c"]
        highs = candles["h"]
        lows = candles["l"]
        volumes = candles["v"]

        pivot, result = pivot_detector.detect_pivot(
            closes,
            highs,
            lows,
            volumes
        )

        if not pivot:
            return

        score = score_calculator.calculate(
            result,
            closes[-1],
            volumes[-1],
            sum(volumes[-20:]) / 20
        )

        if score < 75:
            return

        if not self.can_alert(symbol):
            return

        message = f"""
🚀 AIF Pivot Scanner

📈 {symbol}

⭐ Score : {score}/100

💲 Price : ${closes[-1]:.2f}

📊 Pivot Range : {result['pivot_range']}%

📉 Volume Dry : {result['volume_dry']}
"""

        telegram.send(message)
