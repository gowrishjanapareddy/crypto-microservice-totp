import os
import base64
import pyotp

SEED_FILE = "/data/seed.txt"

def load_seed_hex():
    if not os.path.exists(SEED_FILE):
        return None
    with open(SEED_FILE, "r") as f:
        return f.read().strip()

def generate_totp_code():
    seed_hex = load_seed_hex()
    if not seed_hex:
        raise Exception("Seed not found")

    # Convert hex → bytes → base32
    seed_bytes = bytes.fromhex(seed_hex)
    base32_seed = base64.b32encode(seed_bytes).decode("utf-8")

    totp = pyotp.TOTP(base32_seed)
    return totp.now()
