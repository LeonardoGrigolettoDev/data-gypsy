from app.models import Model
from app.utils.encrypt import encrypt


def create_user(user: dict):
    table = Model("users")
    encrypted = encrypt(user['password'])
    user = {**user, 'password': encrypted}
    return table.insert(user)
