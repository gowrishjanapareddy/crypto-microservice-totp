# totp_utils.py
import base64
import pyotp

SEED_FILE = "/data/seed.txt"

def generate_totp_code() -> str:
    with open(SEED_FILE, "r") as f:
        seed_hex = f.read().strip()

    seed_bytes = bytes.fromhex(seed_hex)
    base32_seed = base64.b32encode(seed_bytes).decode("utf-8")

    totp = pyotp.TOTP(base32_seed)
    return totp.now()
