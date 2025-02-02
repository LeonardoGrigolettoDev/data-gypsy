from app.config import Config
config = Config()
dsn = f"dbname={config.db_name} user={config.db_user} password={config.db_password} host={config.db_host} port={config.db_port}"
