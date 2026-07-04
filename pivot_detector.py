# ==========================================
# AIF Pivot Scanner
# pivot_detector.py
# ==========================================

import numpy as np


class PivotDetector:

    def __init__(self):
        pass

    def detect_pivot(self, closes, highs, lows, volumes):

        # التأكد من وجود بيانات كافية
        if len(closes) < 20:
            return False, {}

        recent_high = max(highs[-10:])
        recent_low = min(lows[-10:])

        # نطاق الارتكاز
        pivot_range = (recent_high - recent_low) / recent_high

        # متوسط الأحجام
        recent_volume = np.mean(volumes[-5:])
        previous_volume = np.mean(volumes[-20:-5])

        volume_dry = recent_volume < previous_volume

        is_pivot = (
            pivot_range <= 0.05
            and volume_dry
        )

        result = {
            "pivot": is_pivot,
            "pivot_high": recent_high,
            "pivot_low": recent_low,
            "pivot_range": round(pivot_range * 100, 2),
            "volume_dry": volume_dry
        }

        return is_pivot, result


pivot_detector = PivotDetector()
