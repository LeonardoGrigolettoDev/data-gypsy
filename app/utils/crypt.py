import bcrypt

def encrypt(string: str) -> bytes:
    salt = bcrypt.gensalt()
    encrypted = bcrypt.hashpw(string.encode('utf-8'), salt)
    return encrypted



def check_encrypt(compare: bytes, encrypt: bytes) -> bool:
    return bcrypt.checkpw(compare, encrypt)
