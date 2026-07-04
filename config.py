# ==========================================
# AIF Pivot Scanner - Optimized Configuration
# ==========================================
import os
from dotenv import load_dotenv

load_dotenv()

# API KEYS
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Scanner Performance - Speed is critical for pivots
# قللنا الفاصل الزمني لزيادة سرعة الاستجابة اللحظية
SCAN_INTERVAL = 60 

# Penny Stock Filter
MIN_PRICE = 0.20
MAX_PRICE = 10.00
MIN_VOLUME = 500000        # رفعناه لضمان وجود سيولة حقيقية
MIN_DOLLAR_VOLUME = 1000000 # رفعناه لضمان سيولة مؤسساتية (Institutional footprint)
MIN_SCORE = 75

# Pivot & SMC Settings
LOOKBACK_DAYS = 20
PIVOT_RANGE = 0.02         # قللنا النطاق لـ 2% لاستهداف مناطق ارتكاز أكثر دقة
VOLUME_DRY_RATIO = 0.50    # رفعنا معايير جفاف السيولة لاكتشاف الانفجار السعري بشكل أفضل

# Alert Settings
ALERT_COOLDOWN = 300       # 5 دقائق لمنع تكرار التنبيهات لنفس السهم

# Timezone
TIMEZONE = "America/New_York"
