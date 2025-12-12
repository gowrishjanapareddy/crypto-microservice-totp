import json
import requests

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

def request_seed(student_id: str, github_repo_url: str, api_url: str = API_URL):
    """
    Request encrypted seed from instructor API
    """

    # 1. Read student public key
    with open("student_public.pem", "r") as f:
        public_key_pem = f.read()

    # 2. Prepare payload
    payload = {
        "student_id": student_id,
        "github_repo_url": github_repo_url,
        "public_key": public_key_pem
    }

    # 3. Send POST request
    response = requests.post(
        api_url,
        json=payload,
        timeout=10
    )

    # Handle error responses
    if response.status_code != 200:
        print("❌ Error calling instructor API:", response.text)
        return None

    data = response.json()

    if data.get("status") != "success":
        print("❌ API returned error:", data)
        return None

    encrypted_seed = data.get("encrypted_seed")

    # 4. Save encrypted seed to a local file (DO NOT COMMIT)
    with open("encrypted_seed.txt", "w") as f:
        f.write(encrypted_seed)

    print("✔ Encrypted seed saved to encrypted_seed.txt")
    return encrypted_seed


if __name__ == "__main__":
    # CHANGE THIS to your actual student ID
    student_id = "23P31A0537"

    github_repo_url = "https://github.com/gowrishjanapareddy/crypto-microservice-totp"

    request_seed(student_id, github_repo_url)