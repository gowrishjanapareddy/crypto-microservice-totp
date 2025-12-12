from totp_utils import generate_totp_code, verify_totp_code

seed_hex = "f555496efc8bd51d8f6525d7f6f7eab10019a28614f9148af927d145e9945f00"

code = generate_totp_code(seed_hex)
print("TOTP Code:", code)

print("Verify:", verify_totp_code(seed_hex, code))
