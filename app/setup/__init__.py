from app.setup.postgres import (create_permissions_table, create_users_table)


def setup_tables():
    create_permissions_table()
    create_users_table()
