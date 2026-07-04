import finnhub
import requests
import config

# إعداد عميل Finnhub
finnhub_client = finnhub.Client(api_key=config.FINNHUB_API_KEY)

def get_market_data(symbol):
    """
    جلب بيانات السعر وبيانات التاريخ لآخر 20 يوم
    """
    try:
        # جلب البيانات التاريخية لـ 25 يوم لضمان وجود 20 يوم تداول
        import time
        to_time = int(time.time())
        from_time = to_time - (25 * 24 * 60 * 60)
        
        res = finnhub_client.stock_candles(symbol, 'D', from_time, to_time)
        
        if res['s'] == 'ok':
            return {
                "current_price": res['c'][-1], # سعر الإغلاق الأخير
                "high": res['h'][-1],
                "low": res['l'][-1],
                "historical_lows": res['l'][-20:] # آخر 20 قاع
            }
    except Exception as e:
        print(f"خطأ في جلب بيانات {symbol}: {e}")
    return None

def send_telegram_msg(message):
    """
    إرسال التنبيه إلى تليجرام
    """
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": config.TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, params=params)
    except Exception as e:
        print(f"خطأ في إرسال رسالة تليجرام: {e}")
