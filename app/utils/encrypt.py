import bcrypt

def encrypt(string: str) -> str:
    # Gera o salt e aplica o hash
    salt = bcrypt.gensalt()
    encrypted = bcrypt.hashpw(string.encode('utf-8'), salt)
    return encrypted.decode('utf-8')