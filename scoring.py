# ==========================================
# AIF Pivot Scanner
# scoring.py
# ==========================================

class ScoreCalculator:

    def __init__(self):
        pass

    def calculate(
        self,
        pivot_data,
        price,
        volume,
        avg_volume
    ):

        score = 0

        # =============================
        # قوة الارتكاز (35 نقطة)
        # =============================
        if pivot_data["pivot"]:
            score += 35

        # =============================
        # جفاف الفوليوم (20 نقطة)
        # =============================
        if pivot_data["volume_dry"]:
            score += 20

        # =============================
        # قرب الاختراق (20 نقطة)
        # =============================
        if pivot_data["pivot_range"] <= 3:
            score += 20
        elif pivot_data["pivot_range"] <= 5:
            score += 10

        # =============================
        # السيولة (15 نقطة)
        # =============================
        if volume >= 1000000:
            score += 15
        elif volume >= 500000:
            score += 10
        elif volume >= 300000:
            score += 5

        # =============================
        # زيادة الحجم (10 نقاط)
        # =============================
        if avg_volume > 0:
            ratio = volume / avg_volume

            if ratio >= 3:
                score += 10
            elif ratio >= 2:
                score += 7
            elif ratio >= 1.5:
                score += 5

        return min(score, 100)


score_calculator = ScoreCalculator()
