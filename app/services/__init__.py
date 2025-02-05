import base64
from app.utils.crypt import (encrypt, check_encrypt)

def encrypt_password(password: str) -> str:
    encrypted_password = encrypt(password)
    print(encrypted_password)
    return encrypted_password.decode("utf-8")

def check_password(password: str, encrypted_password: str) -> bool: 
    return check_encrypt(password.encode("utf-8"), encrypted_password.encode("utf-8"))