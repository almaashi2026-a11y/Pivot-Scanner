import os

# المفاتيح الأساسية
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# تعريف كافة المتغيرات التي يطلبها الكود لتجنب أخطاء الاستيراد
MIN_VOLUME = 50000 
MIN_PRICE = 0.20
MAX_PRICE = 10.00
PIVOT_RANGE = 0.015
