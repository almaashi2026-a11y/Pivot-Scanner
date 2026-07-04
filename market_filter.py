# ==========================================
# AIF Pivot Scanner
# market_filter.py
# ==========================================

from config import (
    MIN_PRICE,
    MAX_PRICE,
    MIN_VOLUME,
    MIN_DOLLAR_VOLUME
)


class MarketFilter:

    def __init__(self):
        pass

    def is_valid_stock(self, candles):

        # التأكد من وجود بيانات
        if not candles:
            return False

        if candles.get("s") != "ok":
            return False

        closes = candles.get("c", [])
        volumes = candles.get("v", [])

        if len(closes) == 0 or len(volumes) == 0:
            return False

        price = closes[-1]
        volume = volumes[-1]

        # فلتر السعر
        if price < MIN_PRICE or price > MAX_PRICE:
            return False

        # فلتر الحجم
        if volume < MIN_VOLUME:
            return False

        # فلتر قيمة التداول
        dollar_volume = price * volume

        if dollar_volume < MIN_DOLLAR_VOLUME:
            return False

        return True


market_filter = MarketFilter()
