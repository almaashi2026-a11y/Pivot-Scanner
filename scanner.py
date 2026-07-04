def calculate_pivots(high, low, close):
    """
    حساب نقاط الارتكاز الكلاسيكية
    Pivot = (High + Low + Close) / 3
    """
    pivot = (high + low + close) / 3
    r1 = (2 * pivot) - low
    r2 = pivot + (high - low)
    s1 = (2 * pivot) - high
    s2 = pivot - (high - low)
    
    return {
        "pivot": pivot,
        "r1": r1,
        "r2": r2,
        "s1": s1,
        "s2": s2
    }

def check_pivot_alert(current_price, high, low, close):
    """
    التحقق من اقتراب السعر من نقطة الارتكاز بناءً على نطاق 2% (PIVOT_RANGE)
    """
    levels = calculate_pivots(high, low, close)
    
    # التحقق هل السعر الحالي قريب من أي مستوى (دعم أو مقاومة)
    for key, value in levels.items():
        # حساب نسبة الاختلاف
        diff = abs(current_price - value) / value
        
        # إذا كان السعر ضمن نطاق 2% من أي مستوى ارتكاز
        if diff <= 0.02: 
            return True, f"السعر اقترب من {key.upper()}: {value:.2f}"
            
    return False, None
