# ==========================================
# AIF Pivot Scanner
# config.py
# ==========================================

import os
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

# ==========================
# API KEYS
# ==========================
FINNHUB_API_KEY = os.getenv("d934frpr01qpou39gg00d934frpr01qpou39gg0g")
TELEGRAM_BOT_TOKEN = os.getenv("8895817474:AAHxy3y7WfwNSFfYUY9qPNZmo4xCvlURB8o")
TELEGRAM_CHAT_ID = os.getenv("7990990947")

# ==========================
# Scanner Settings
# ==========================
SCAN_INTERVAL = 300      # 5 دقائق

# ==========================
# Penny Stock Filter
# ==========================
MIN_PRICE = 0.20
MAX_PRICE = 10.00

MIN_VOLUME = 300000

MIN_DOLLAR_VOLUME = 500000

MIN_SCORE = 75

# ==========================
# Pivot Settings
# ==========================
LOOKBACK_DAYS = 20

PIVOT_RANGE = 0.05       # 5%

VOLUME_DRY_RATIO = 0.70

# ==========================
# Alert Settings
# ==========================
ALERT_COOLDOWN = 60       # دقيقة

# ==========================
# Timezone
# ==========================
TIMEZONE = "America/New_York"
