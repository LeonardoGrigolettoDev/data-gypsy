import bcrypt

def encrypt(string: str) -> str:
    # Gera o salt e aplica o hash
    salt = bcrypt.gensalt()
    encrypted = bcrypt.hashpw(string.encode('utf-8'), salt)
    return encrypted.decode('utf-8'), salt.decode('utf-8')

def check_encrypt(string: str, encrypt: str) -> bool:
    return bcrypt.checkpw(string.encode('utf-8'), encrypt.encode('utf-8'))