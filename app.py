from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import base64
import pyotp

from decrypt_seed import decrypt_seed  # your working RSA function

app = FastAPI()

class SeedRequest(BaseModel):
    encrypted_seed: str

class VerifyRequest(BaseModel):
    code: str

def hex_to_base32(seed_hex: str) -> str:
    seed_bytes = bytes.fromhex(seed_hex)
    return base64.b32encode(seed_bytes).decode()

@app.get("/")
def root():
    return {"message": "Crypto microservice is running"}

@app.post("/decrypt-seed")
def decrypt_seed_endpoint(req: SeedRequest):
    try:
        seed_hex = decrypt_seed(req.encrypted_seed)

        # Save hex seed
        with open("/data/seed.txt", "w") as f:
            f.write(seed_hex)

        return {"status": "ok"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/generate-2fa")
def generate_2fa():
    try:
        with open("/data/seed.txt", "r") as f:
            seed_hex = f.read().strip()

        seed_b32 = hex_to_base32(seed_hex)
        totp = pyotp.TOTP(seed_b32)
        code = totp.now()

        return {"code": code}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/verify-2fa")
def verify_2fa(req: VerifyRequest):
    try:
        with open("/data/seed.txt", "r") as f:
            seed_hex = f.read().strip()

        seed_b32 = hex_to_base32(seed_hex)
        totp = pyotp.TOTP(seed_b32)

        if totp.verify(req.code):
            return {"status": "valid"}

        return {"status": "invalid"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/health")
def health():
    return {"status": "ok"}
