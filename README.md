# crypto-microservice-totp

This project implements a **secure cryptographic microservice** that:

- Decrypts an RSA-encrypted seed using a **student private key**
- Generates **TOTP (2FA) codes** using RFC-compliant logic
- Verifies submitted 2FA codes
- Logs TOTP codes every minute using **cron**
- Runs fully inside **Docker**

⚠️ **Security Notice**  
The cryptographic keys included in this repository are **ONLY for this assignment**.  
Do **NOT** reuse them for any real or production system.

---

## 📌 Features

- RSA decryption (OAEP + SHA-256)
- TOTP generation (RFC 6238)
- FastAPI REST endpoints
- Persistent seed storage
- Cron-based TOTP logging (UTC)
- Dockerized deployment

---

## 📂 Project Structure

```text
crypto-microservice-totp/
├── app.py                     # FastAPI application
├── decrypt_seed.py             # RSA seed decryption logic
├── totp_utils.py               # TOTP generation utility
├── scripts/
│   └── log_2fa_cron.py         # Cron job script
├── cron/
│   └── 2fa-cron                # Cron configuration
├── data/                       # Persisted decrypted seed
├── student_private.pem         # REQUIRED (public for assignment)
├── student_public.pem          # REQUIRED
├── instructor_public.pem       # REQUIRED
├── encrypted_seed.txt          # Provided encrypted seed (NOT committed)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
├── .gitattributes
└── README.md

```
## 🚀 API Endpoints

### Health Check

GET /health

Response:
{"status":"ok"}

---

### Decrypt Seed

POST /decrypt-seed

Request:
{
  "encrypted_seed": "BASE64_STRING"
}

Response:
{"status":"ok"}

The decrypted seed is stored at:
/data/seed.txt

---

### Generate 2FA Code

GET /generate-2fa

Response:
{
  "code": "123456"
}

---

### Verify 2FA Code

POST /verify-2fa

Request:
{
  "code": "123456"
}

Valid response:
{"status":"valid"}

Invalid response:
{"status":"invalid"}

---

## ⏱ Cron Job (TOTP Logger)

- Runs every minute
- Generates a fresh TOTP code
- Logs output to:

/cron/last_code.txt

Example output:
2025-12-13T15:39:01 2FA=922851

---

## 🐳 Docker Usage

Build the image:
docker-compose build

Start the service:
docker-compose up -d

---

## 🧪 Local Testing

1) Decrypt Seed
curl -X POST http://localhost:8080/decrypt-seed \
-H "Content-Type: application/json" \
-d "{\"encrypted_seed\": \"$(cat encrypted_seed.txt)\"}"

2) Generate TOTP
curl http://localhost:8080/generate-2fa

3) Verify Valid Code
CODE=$(curl -s http://localhost:8080/generate-2fa | jq -r '.code')

curl -X POST http://localhost:8080/verify-2fa \
-H "Content-Type: application/json" \
-d "{\"code\": \"$CODE\"}"

4) Verify Invalid Code
curl -X POST http://localhost:8080/verify-2fa \
-H "Content-Type: application/json" \
-d '{"code":"000000"}'

5) Check Cron Output
sleep 70
docker exec crypto-microservice-totp cat /cron/last_code.txt

---

## 🔐 Cryptographic Details

RSA Decryption:
- Algorithm: RSA
- Padding: OAEP
- Hash: SHA-256

TOTP:
- Standard: RFC 6238
- Digits: 6
- Time step: 30 seconds
- Timezone: UTC

---

## 📎 Submission Notes

- student_private.pem is intentionally committed
- Keys are public only for assignment evaluation
- Encrypted seed is never committed
- Cron logs prove time-based correctness

---

## ✅ Assignment Checklist

- RSA seed decryption
- TOTP generation
- TOTP verification
- Cron logging
- Dockerized
- UTC time
- Persistent seed
- Verified locally

---

## 👨‍🎓 Author

Student Name: YOUR NAME  
Assignment: PKI + TOTP Crypto Microservice

---

## ⚠️ Disclaimer

This repository contains cryptographic material ONLY for educational evaluation.
Do NOT reuse keys or logic in production systems.
