import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes


def load_private_key():
    """Load student_private.pem and return private key object."""
    with open("student_private.pem", "rb") as f:
        pem_data = f.read()

    private_key = serialization.load_pem_private_key(
        pem_data,
        password=None
    )
    return private_key


def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    """
    Decrypt base64-encoded encrypted seed using RSA/OAEP(SHA-256)
    """

    # 1. Base64 decode the ciphertext
    encrypted_bytes = base64.b64decode(encrypted_seed_b64)

    # 2. RSA/OAEP decrypt
    decrypted_bytes = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 3. Convert bytes → UTF-8 string
    hex_seed = decrypted_bytes.decode("utf-8")

    # 4. Validate hex seed (must be 64 hex chars)
    if len(hex_seed) != 64:
        raise ValueError("Invalid seed length (must be 64 hex characters).")

    valid_hex = "0123456789abcdef"
    if not all(c in valid_hex for c in hex_seed.lower()):
        raise ValueError("Seed contains non-hex characters.")

    return hex_seed


if __name__ == "__main__":
    # Load private key
    private_key = load_private_key()

    # Read encrypted seed
    with open("encrypted_seed.txt", "r") as f:
        encrypted_seed_b64 = f.read().strip()

    # Decrypt
    seed = decrypt_seed(encrypted_seed_b64, private_key)

    # Save seed to /data/seed.txt (as required for Docker)
    with open("data/seed.txt", "w") as f:
        f.write(seed)

    print("✔ Seed decrypted successfully!")
    print("✔ Saved to data/seed.txt")