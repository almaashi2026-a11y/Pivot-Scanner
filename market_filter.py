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

    def is_valid_stock(self, quote):

        if not quote:
            return False

        price = quote.get("c", 0)
        volume = quote.get("v", 0)

        # السعر
        if price < MIN_PRICE:
            return False

        if price > MAX_PRICE:
            return False

        # الحجم
        if volume < MIN_VOLUME:
            return False

        # قيمة التداول
        dollar_volume = price * volume

        if dollar_volume < MIN_DOLLAR_VOLUME:
            return False

        return True


market_filter = MarketFilter()
