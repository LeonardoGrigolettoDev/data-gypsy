from app.models import Model
from  app.services import (check_password, encrypt_password)

def auth_user(email: str, password: str):
    table = Model("users")
    found = table.read(filters={'email': email})
    if not found:
        return False 
    pwd = found['password']
    auth = check_password(password, pwd)
    print(f"Senha armazenada no banco: {found['password']}")
    print(auth)
    if not auth:
        return auth
    
    return {**found, "password": None}


def create_user(user: dict):
    table = Model("users")
    print(user['password'])
    encrypted = encrypt_password(user['password'])
    user = {**user, 'password': encrypted}
    return table.insert(user)
