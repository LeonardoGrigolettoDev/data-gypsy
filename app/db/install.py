import psycopg2
from app.db import PostgreSQL

def create_postgres_internal_tables():
    db = PostgreSQL()
    schemas = [('tabUser',{
    'id': 'SERIAL PRIMARY KEY',     
    'name': 'VARCHAR(100)',          
    'email': 'VARCHAR(150) UNIQUE', 
    'created_at': 'TIMESTAMP'       
    })]
    for table_name, schema in schemas:
        db.create_table(table_name, schema)
        
