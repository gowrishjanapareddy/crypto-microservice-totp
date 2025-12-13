# scripts/log_2fa_cron.py
from datetime import datetime, timezone
from totp_utils import generate_totp_code
import os

SEED_FILE = "/data/seed.txt"

def main():
    if not os.path.exists(SEED_FILE):
        return  # seed not ready yet, silently skip

    try:
        code = generate_totp_code()
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
        print(f"{ts} 2FA={code}")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
