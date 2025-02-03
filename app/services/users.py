from app.models import Model
from app.utils.encrypt import (encrypt, check_encrypt)


def auth_user(email: str, password: str):
    table = Model("users")
    has_user = table.read(filters={'email': email})
    if not len(has_user):
        return has_user 
    has_user = has_user[0]
    auth = check_encrypt(password, has_user['password'])
    if not auth:
        return auth
    
    return {**has_user, "password": None}


def create_user(user: dict):
    table = Model("users")
    encrypted, salt = encrypt(user['password'])
    user = {**user, 'password': encrypted, 'salt': salt}
    return table.insert(user)
