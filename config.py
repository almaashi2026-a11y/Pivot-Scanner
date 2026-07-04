import os
from dotenv import load_dotenv

load_dotenv()

# API KEYS
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Scanner Settings
SCAN_INTERVAL = 60 # ثانية
LOOKBACK_DAYS = 20
PIVOT_RANGE = 0.02 # 2%
VOLUME_DRY_RATIO = 0.50

# Filter Settings
MIN_PRICE = 0.20
MAX_PRICE = 10.00
MIN_DOLLAR_VOLUME = 1000000 
