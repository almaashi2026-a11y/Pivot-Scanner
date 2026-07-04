# ==========================================
# AIF Pivot Scanner - Optimized Professional Config
# ==========================================
import os
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

# ==========================
# API KEYS
# ==========================
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ==========================
# Scanner Settings (Optimized for Speed)
# ==========================
# تقليص الفاصل الزمني لضمان التقاط الحركة لحظة حدوث الارتكاز
SCAN_INTERVAL = 60 

# ==========================
# Penny Stock & Institutional Filter
# ==========================
MIN_PRICE = 0.20
MAX_PRICE = 10.00

# رفع معايير السيولة لاستهداف الأسهم التي تتبعها "السيولة الذكية"
MIN_VOLUME = 500000        
MIN_DOLLAR_VOLUME = 1000000 
MIN_SCORE = 75

# ==========================
# Pivot & SMC Logic Settings
# ==========================
# تقليل النطاق لـ 2% يضمن لك دخولاً عند أقوى مناطق الارتكاز فقط
LOOKBACK_DAYS = 20
PIVOT_RANGE = 0.02         
VOLUME_DRY_RATIO = 0.50    # تم تضييق النطاق لاكتشاف الانفجار السعري بوضوح أكبر

# ==========================
# Alert Settings
# ==========================
# منع إزعاج التنبيهات المكررة لنفس السهم
ALERT_COOLDOWN = 300 

# ==========================
# Timezone
# ==========================
TIMEZONE = "America/New_York"
