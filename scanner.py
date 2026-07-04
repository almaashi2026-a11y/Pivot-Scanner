import time
import config # لاستيراد الإعدادات التي عدلناها
# افترض أن لديك دالة إرسال التليجرام موجودة مسبقاً
from telegram_bot import send_telegram_msg 
from finnhub_client import get_market_data # دالة جلب البيانات التي كتبناها

def calculate_pivots(high, low, close):
    pivot = (high + low + close) / 3
    return {
        "pivot": pivot,
        "r1": (2 * pivot) - low,
        "s1": (2 * pivot) - high
    }

def check_pivot_and_liquidity(current_price, high, low, close, historical_lows):
    levels = calculate_pivots(high, low, close)
    alerts = []
    
    # 1. التحقق من الارتكاز الكلاسيكي (ضمن نطاق 2%)
    for key, value in levels.items():
        if abs(current_price - value) / value <= config.PIVOT_RANGE:
            alerts.append(f"🎯 ارتكاز: {key.upper()} عند {value:.2f}")

    # 2. التحقق من القيعان القديمة (مناطق السيولة)
    min_historical = min(historical_lows)
    if abs(current_price - min_historical) / min_historical <= 0.015:
        alerts.append(f"🌊 سيولة: السعر يختبر قاعاً قديماً عند {min_historical:.2f}")

    return alerts

def run_scanner(symbols):
    print("--- بدأ الماسح في العمل ---")
    while True:
        for symbol in symbols:
            data = get_market_data(symbol)
            if data:
                alerts = check_pivot_and_liquidity(
                    data['current_price'],
                    data['high'],
                    data['low'],
                    data['current_price'],
                    data['historical_lows']
                )
                
                if alerts:
                    msg = f"🔔 *تنبيه للسهم:* {symbol}\n" + "\n".join(alerts)
                    send_telegram_msg(msg)
                    print(f"تم إرسال تنبيه للسهم: {symbol}")
        
        # الانتظار حسب الفاصل الزمني في config.py
        time.sleep(config.SCAN_INTERVAL)

# تشغيل الماسح
if __name__ == "__main__":
    symbols_to_scan = ["AAPL", "AMD", "NVDA"] # أضف قائمتك هنا
    run_scanner(symbols_to_scan)
