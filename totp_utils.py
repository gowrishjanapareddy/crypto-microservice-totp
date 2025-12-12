import pyotp
import base64

def hex_to_base32(hex_seed: str) -> str:
    """
    Convert 64-char hex seed into Base32 string (no padding).
    """
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode().replace("=", "")
    return base32_seed


def generate_totp_code(hex_seed: str) -> str:
    """
    Generate current TOTP code (6 digits).
    """
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)
    return totp.now()


def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Verify a TOTP code within ±valid_window intervals (default ±30 sec).
    """
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)
    return totp.verify(code, valid_window=valid_window)