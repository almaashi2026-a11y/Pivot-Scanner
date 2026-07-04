# ==========================================
# AIF Pivot Scanner
# app.py
# ==========================================

import time
from scanner import PivotScanner
from config import SCAN_INTERVAL


def main():

    scanner = PivotScanner()

    print("=" * 50)
    print("🚀 AIF Pivot Scanner Started")
    print(f"⏰ Scan Every {SCAN_INTERVAL} Seconds")
    print("=" * 50)

    while True:

        try:

            print("\nStarting New Scan...")
            scanner.run()

        except Exception as e:

            print(f"Scanner Error: {e}")

        time.sleep(SCAN_INTERVAL)


if __name__ == "__main__":
    main()
