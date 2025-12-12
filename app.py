from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import base64
import time

from cryptography.hazmat.primitives import serialization
from decrypt_seed import decrypt_seed
from totp_utils import generate_totp_code, verify_totp_code


app = FastAPI()

SEED_PATH = "data/seed.txt"
PRIVATE_KEY_PATH = "student_private.pem"


# ----------- Request Models -----------

class DecryptRequest(BaseModel):
    encrypted_seed: str


class VerifyRequest(BaseModel):
    code: str


# ----------- Helpers -----------

def load_private_key():
    """Load student private key from PEM file."""
    if not os.path.exists(PRIVATE_KEY_PATH):
        raise Exception("Private key not found")

    with open(PRIVATE_KEY_PATH, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)


def read_seed():
    """Load decrypted seed from data/seed.txt."""
    if not os.path.exists(SEED_PATH):
        return None
    with open(SEED_PATH, "r") as f:
        return f.read().strip()


# ----------- Endpoints -----------

@app.post("/decrypt-seed")
def decrypt_seed_endpoint(req: DecryptRequest):
    try:
        private_key = load_private_key()

        # Base64 decode
        encrypted_bytes = base64.b64decode(req.encrypted_seed)

        # Decrypt using your function
        hex_seed = decrypt_seed(req.encrypted_seed, private_key)

        # Validate hex seed
        if len(hex_seed) != 64 or any(c not in "0123456789abcdef" for c in hex_seed):
            raise Exception("Invalid decrypted seed format")

        # Save to /data/seed.txt
        os.makedirs("data", exist_ok=True)
        with open(SEED_PATH, "w") as f:
            f.write(hex_seed)

        return {"status": "ok"}

    except Exception as e:
        return {"error": f"Decryption failed: {str(e)}"}


@app.get("/generate-2fa")
def generate_2fa():
    seed = read_seed()
    if not seed:
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    # Generate code
    code = generate_totp_code(seed)

    # Remaining seconds in this TOTP period
    now = int(time.time())
    valid_for = 30 - (now % 30)

    return {
        "code": code,
        "valid_for": valid_for
    }


@app.post("/verify-2fa")
def verify_2fa(req: VerifyRequest):
    if not req.code:
        raise HTTPException(status_code=400, detail="Missing code")

    seed = read_seed()
    if not seed:
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    is_valid = verify_totp_code(seed, req.code, valid_window=1)

    return {"valid": is_valid}
