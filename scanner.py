import config

def analyze_opportunity(current_price, high, low, close, historical_lows):
    # حساب الارتكاز (Pivot)
    pivot = (high + low + close) / 3
    r1 = (2 * pivot) - low
    s1 = (2 * pivot) - high
    
    alerts = []
    
    # فحص الارتكاز
    if abs(current_price - pivot) / pivot <= config.PIVOT_RANGE:
        alerts.append(f"🎯 ارتكاز: قريب من نقطة PIVOT ({pivot:.2f})")
    
    # فحص القاع القديم (السيولة)
    min_historical = min(historical_lows)
    if abs(current_price - min_historical) / min_historical <= 0.015:
        alerts.append(f"🌊 سيولة: السعر يختبر قاعاً قديماً ({min_historical:.2f})")

    return alerts if alerts else None
