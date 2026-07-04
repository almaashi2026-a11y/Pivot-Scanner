import time
import config
from scanner import analyze_opportunity
# افترض أن لديك دوال جاهزة للجلب والإرسال
from utils import get_market_data, send_telegram_msg 

def run():
    print("🚀 الماسح بدأ العمل بنظام الارتكاز والسيولة...")
    symbols = ["AAPL", "AMD", "NVDA"] # أضف قائمتك هنا
    
    while True:
        try:
            for symbol in symbols:
                data = get_market_data(symbol)
                if data:
                    alerts = analyze_opportunity(
                        data['current_price'], data['high'], data['low'], 
                        data['current_price'], data['historical_lows']
                    )
                    
                    if alerts:
                        msg = f"🔔 *تنبيه:* {symbol}\n" + "\n".join(alerts)
                        send_telegram_msg(msg)
            
            time.sleep(config.SCAN_INTERVAL)
            
        except Exception as e:
            print(f"حدث خطأ، إعادة المحاولة... {e}")
            time.sleep(60)

if __name__ == "__main__":
    run()
