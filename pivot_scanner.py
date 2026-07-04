# =========================================================
# PivotScanner V1 - Institutional Batch Market Scanner
# Developer: AIF Pro System
# =========================================================

import time
import json
import logging
import requests
from datetime import datetime, timedelta

import config
from finnhub_client import FinnhubClient
from market_filter import MarketFilter
from pivot_detector import PivotDetector
from scoring import ScoreEngine

# =========================================================
# LOGGING SETUP
# =========================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("scanner.log"),
        logging.StreamHandler()
    ]
)

# =========================================================
# TELEGRAM ALERT
# =========================================================
class TelegramBot:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.url = f"https://api.telegram.org/bot{token}/sendMessage"

    def send(self, message: str):
        try:
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            requests.post(self.url, data=payload, timeout=10)
        except Exception as e:
            logging.error(f"Telegram Error: {e}")


# =========================================================
# STATE MANAGER (resume batch position)
# =========================================================
class StateManager:
    def __init__(self, file="state.json"):
        self.file = file
        self.state = self.load()

    def load(self):
        try:
            with open(self.file, "r") as f:
                return json.load(f)
        except:
            return {
                "last_index": 0,
                "last_alerts": {}
            }

    def save(self):
        with open(self.file, "w") as f:
            json.dump(self.state, f, indent=2)

    def get_index(self):
        return self.state.get("last_index", 0)

    def set_index(self, idx):
        self.state["last_index"] = idx
        self.save()

    def is_cooldown(self, symbol):
        last_alert = self.state["last_alerts"].get(symbol)
        if not last_alert:
            return False
        last_time = datetime.fromisoformat(last_alert)
        return datetime.utcnow() - last_time < timedelta(hours=1)

    def update_alert(self, symbol):
        self.state["last_alerts"][symbol] = datetime.utcnow().isoformat()
        self.save()


# =========================================================
# MAIN SCANNER
# =========================================================
class PivotScanner:
    def __init__(self):
        self.client = FinnhubClient()
        self.filter = MarketFilter()
        self.pivot = PivotDetector()
        self.score_engine = ScoreEngine()

        self.telegram = TelegramBot(config.TELEGRAM_TOKEN, config.TELEGRAM_CHAT_ID)
        self.state = StateManager()

        self.batch_size = 100
        self.symbols = self.load_symbols()

    # -----------------------------------------------------
    def load_symbols(self):
        try:
            with open("symbols.json", "r") as f:
                return json.load(f)
        except Exception:
            logging.error("symbols.json not found")
            return []

    # -----------------------------------------------------
    def process_symbol(self, symbol):
        try:
            if self.state.is_cooldown(symbol):
                return None

            data = self.client.get_quote(symbol)
            if not data:
                return None

            # فلترة السوق
            if not self.filter.passes(data):
                return None

            # اكتشاف pivot
            pivot_data = self.pivot.detect(symbol)
            if not pivot_data:
                return None

            # حساب السكور
            score = self.score_engine.calculate(symbol, data, pivot_data)

            if score < config.MIN_SCORE:
                return None

            return {
                "symbol": symbol,
                "score": score,
                "price": data["c"],
                "pivot": pivot_data
            }

        except Exception as e:
            logging.error(f"Error processing {symbol}: {e}")
            return None

    # -----------------------------------------------------
    def send_alert(self, result):
        symbol = result["symbol"]
        price = result["price"]
        score = result["score"]

        message = f"""
🚨 <b>Pivot Signal Detected</b>

📊 Symbol: {symbol}
💰 Price: {price}
⭐ Score: {score}

⚡ Institutional pivot detected
⏱ {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
"""

        self.telegram.send(message)
        self.state.update_alert(symbol)

    # -----------------------------------------------------
    def run_batch(self):
        start_index = self.state.get_index()
        end_index = start_index + self.batch_size

        batch = self.symbols[start_index:end_index]

        if not batch:
            logging.info("Restarting symbol cycle...")
            start_index = 0
            end_index = self.batch_size
            batch = self.symbols[start_index:end_index]

        logging.info(f"Processing batch {start_index} → {end_index}")

        for i, symbol in enumerate(batch, start=start_index):
            result = self.process_symbol(symbol)

            if result:
                logging.info(f"Signal: {result}")
                self.send_alert(result)

            self.state.set_index(i + 1)
            time.sleep(config.REQUEST_DELAY)

    # -----------------------------------------------------
    def run(self):
        logging.info("PivotScanner V1 Started 🚀")

        while True:
            try:
                self.run_batch()
                time.sleep(config.BATCH_DELAY)

            except Exception as e:
                logging.error(f"Main loop error: {e}")
                time.sleep(5)


# =========================================================
# ENTRY POINT
# =========================================================
if __name__ == "__main__":
    scanner = PivotScanner()
    scanner.run()
