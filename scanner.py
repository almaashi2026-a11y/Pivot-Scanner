import config

def calculate_pivots(high, low, close):
    pivot = (high + low + close) / 3
    return {
        "pivot": pivot,
        "r1": (2 * pivot) - low,
        "s1": (2 * pivot) - high
    }

def analyze_opportunity(current_price, high, low, close, historical_lows):
    levels = calculate_pivots(high, low, close)
    alerts = []
    
    # 1. الارتكاز الكلاسيكي
    for key, value in levels.items():
        if abs(current_price - value) / value <= config.PIVOT_RANGE:
            alerts.append(f"🎯 ارتكاز: {key.upper()} عند {value:.2f}")

    # 2. فحص السيولة (القاع القديم)
    min_historical = min(historical_lows)
    if abs(current_price - min_historical) / min_historical <= 0.015:
        alerts.append(f"🌊 سيولة: السعر يختبر قاعاً قديماً عند {min_historical:.2f}")

    return alerts if alerts else None
