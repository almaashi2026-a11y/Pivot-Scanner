import finnhub
import requests
import config
import time

finnhub_client = finnhub.Client(api_key=config.FINNHUB_API_KEY)

def get_market_data(symbol):
    try:
        # جلب بيانات آخر 20 يوم
        to_time = int(time.time())
        from_time = to_time - (30 * 24 * 60 * 60)
        
        res = finnhub_client.stock_candles(symbol, 'D', from_time, to_time)
        
        if res['s'] == 'ok':
            # نستخدم القوائم مباشرة بدون pandas
            closes = res['c']
            highs = res['h']
            lows = res['l']
            
            return {
                "current_price": closes[-1],
                "high": highs[-1],
                "low": lows[-1],
                "historical_lows": lows[-21:-1] # آخر 20 قاع
            }
    except Exception as e:
        print(f"خطأ في جلب بيانات {symbol}: {e}")
    return None

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {"chat_id": config.TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, params=params)
