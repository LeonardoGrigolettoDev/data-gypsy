def connect_to_external_db():
    pass

# import psycopg2

# def create_database(db_name, user, password, host, port):
#     try:
#         # Conectar ao banco principal
#         connection = psycopg2.connect(
#             dbname="postgres", user=user, password=password, host=host, port=port
#         )
#         connection.autocommit = True
#         cursor = connection.cursor()

#         # Criar banco de dados dinamicamente
#         cursor.execute(f"CREATE DATABASE {db_name}")
#         print(f"Banco de dados '{db_name}' criado com sucesso!")

#     except Exception as e:
#         print(f"Erro ao criar banco de dados: {e}")
#     finally:
#         if connection:
#             cursor.close()
#             connection.close()

# # Chamar a função
# create_database("meu_banco_dinamico", "usuario", "senha", "localhost", "5432")