#!/usr/bin/env python3

import os
from datetime import datetime, timezone
from totp_utils import generate_totp_code

SEED_PATH = "/data/seed.txt"

def read_seed():
    try:
        with open(SEED_PATH, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("Seed file not found")
        return None

def main():
    seed = read_seed()
    if not seed:
        print("No seed available for cron job")
        return

    code = generate_totp_code(seed)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    print(f"{timestamp} - 2FA Code: {code}")

if __name__ == "__main__":
    main()
