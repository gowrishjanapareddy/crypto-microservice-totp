import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def sign_message(commit_hash: str, private_key):
    """
    Sign commit hash using RSA-PSS with SHA-256
    """
    return private_key.sign(
        commit_hash.encode("utf-8"),  # ASCII bytes
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

def encrypt_with_public_key(data: bytes, public_key):
    """
    Encrypt signature using RSA/OAEP-SHA256
    """
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def main():
    # 1. Get commit hash from user
    commit_hash = input("Enter your commit hash: ").strip()
    if len(commit_hash) != 40:
        raise ValueError("Commit hash must be 40 characters long")

    # 2. Load student private key
    with open("student_private.pem", "rb") as f:
        student_private_key = serialization.load_pem_private_key(
            f.read(),
            password=None
        )

    # 3. Sign commit hash
    signature = sign_message(commit_hash, student_private_key)

    # 4. Load instructor public key
    with open("instructor_public.pem", "rb") as f:
        instructor_public_key = serialization.load_pem_public_key(f.read())

    # 5. Encrypt signature
    encrypted_signature = encrypt_with_public_key(signature, instructor_public_key)

    # 6. Base64 encode
    encoded = base64.b64encode(encrypted_signature).decode("utf-8")

    print("\n============================")
    print(" FINAL OUTPUT FOR SUBMISSION")
    print("============================")
    print("Commit Hash:")
    print(commit_hash)
    print("\nEncrypted Signature (single line):")
    print(encoded)
    print("============================")

if __name__ == "__main__":
    main()