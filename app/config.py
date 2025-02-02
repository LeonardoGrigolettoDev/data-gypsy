import os
class Config:
    def __init__(self):
        self.db_host=os.getenv('POSTGRES_HOST')
        self.db_port=os.getenv('POSTGRES_PORT')
        self.db_name=os.getenv('POSTGRES_DBNAME')
        self.db_user=os.getenv('POSTGRES_USER')
        self.db_password=os.getenv('POSTGRES_PASSWORD')
        self.str_encrypt=os.getenv('ENCRYPT')
