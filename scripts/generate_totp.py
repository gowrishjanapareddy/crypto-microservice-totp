import base64
import pyotp
from datetime import datetime

def generate_totp_from_seed(seed_hex: str) -> str:
    # Convert hex → bytes
    seed_bytes = bytes.fromhex(seed_hex)

    # Convert bytes → Base32
    seed_b32 = base64.b32encode(seed_bytes).decode()

    # Create TOTP generator
    totp = pyotp.TOTP(seed_b32)

    return totp.now()

if __name__ == "__main__":
    try:
        with open("/data/seed.txt", "r") as f:
            seed_hex = f.read().strip()

        code = generate_totp_from_seed(seed_hex)

        # Write cron output
        with open("/cron/output.txt", "a") as log:
            log.write(f"{datetime.utcnow()} - 2FA Code: {code}\n")

        print("Generated TOTP:", code)

    except Exception as e:
        print("Error:", e)