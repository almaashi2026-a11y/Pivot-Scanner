def check_pivot_and_liquidity(current_price, high, low, close, historical_lows):
    """
    تحليل مزدوج: 
    1. نقاط الارتكاز الكلاسيكية.
    2. الارتداد من قيعان قديمة (مناطق سيولة).
    """
    levels = calculate_pivots(high, low, close)
    alerts = []
    
    # 1. التحقق من نقاط الارتكاز الكلاسيكية
    for key, value in levels.items():
        if abs(current_price - value) / value <= 0.02:
            alerts.append(f"🎯 ارتكاز: اقترب من {key.upper()} عند {value:.2f}")

    # 2. التحقق من الارتداد من القيعان القديمة (مناطق السيولة)
    # historical_lows يجب أن تكون قائمة تحتوي على أدنى أسعار للأيام الـ 20 الماضية
    min_historical = min(historical_lows)
    if abs(current_price - min_historical) / min_historical <= 0.015: # هامش 1.5% للقيعان
        alerts.append(f"🌊 سيولة: السعر يختبر قاعاً قديماً عند {min_historical:.2f} (فرصة ارتداد)")

    if alerts:
        return True, "\n".join(alerts)
    
    return False, None
