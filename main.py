import time
import random
import config
import utils
import scanner

def run_scanner():
    print("🚀 الماسح الذكي بدأ العمل...")
    utils.send_telegram_msg("✅ الماسح الذكي نشط الآن ويقوم بفلترة السوق (0.20$ - 10$)!")

    # 1. جلب القائمة من السوق
    try:
        all_symbols = [s['symbol'] for s in utils.finnhub_client.stock_symbols('US') if s['type'] == 'Common Stock']
    except:
        all_symbols = ["AAPL", "TSLA", "AMD", "PLTR", "SOFI"] # احتياطي

    while True:
        # 2. اختيار 100 سهم عشوائياً
        random_symbols = random.sample(all_symbols, min(100, len(all_symbols)))
        
        for symbol in random_symbols:
            # 3. جلب السعر للفلترة
            try:
                quote = utils.finnhub_client.quote(symbol)
                price = quote.get('c', 0)
                
                # شرط السعر (0.20$ - 10$)
                if not (0.20 <= price <= 10.00):
                    continue
                
                # 4. جلب البيانات والتحليل
                data = utils.get_market_data(symbol)
                if not data:
                    continue
                
                alerts = scanner.analyze_opportunity(
                    data['current_price'], data['high'], data['low'], 
                    data['current_price'], data['historical_lows']
                )
                
                # 5. إرسال التنبيه إذا وجدنا فرصة
                if alerts:
                    msg = f"🔔 *فرصة في سهم {symbol}*\nالسعر الحالي: {price}$\n\n" + "\n".join(alerts)
                    utils.send_telegram_msg(msg)
                    
                time.sleep(0.5) # حماية للـ API
            except:
                continue
        
        print("⏳ انتهت دورة الفحص، ننتظر دقيقتين...")
        time.sleep(120)

if __name__ == "__main__":
    run_scanner()
