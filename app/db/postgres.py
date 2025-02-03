from app.db import dsn
import psycopg2


def connect_db():
    try:
        conn = psycopg2.connect(dsn)
        cur = conn.cursor()
        return conn, cur
    except Exception as e:
        print(f"Error on connect to postgres db: {e}")
        return None, None


def execute_query(query, params=None):
    conn, cur = connect_db()
    if not conn:
        return {"error": "Could not connect to postgres"}
    try:
        query = query.strip().lower()
        # Verifica o tipo da consulta usando a primeira palavra (tipo de query)
        match query.split()[0]:
            case "select":
                cur.execute(query, params)
                result = cur.fetchall()
                # Obtém os nomes das colunas
                columns = [desc[0] for desc in cur.description]

                # Transforma os resultados em dicionários { "coluna": valor }
                data = [dict(zip(columns, row)) for row in result]

                return data if data else []

            case "insert":
                cur.execute(query, params)
                conn.commit()
                result = cur.fetchone()
                return result

            case "update":
                cur.execute(query, params)
                conn.commit()
                return {"message": f"{cur.rowcount} linha(s) atualizada(s)"}

            case "delete":
                cur.execute(query, params)
                conn.commit()
                return {"message": f"{cur.rowcount} linha(s) excluída(s)"}

            case "create":
                cur.execute(query, params)
                conn.commit()
                return {"message": "Tabela criada com sucesso"}

            case "drop":
                cur.execute(query, params)
                conn.commit()
                return {"message": "Tabela removida com sucesso"}

            case "alter":
                cur.execute(query, params)
                conn.commit()
                return {"message": "Tabela alterada com sucesso"}

            case _:
                return {"error": "Tipo de consulta não reconhecido"}

    except Exception as e:
        conn.rollback()  # Faz rollback em caso de erro
        return e

    finally:
        cur.close()
        conn.close()


def create_table(table_name: str, schema: dict):
    try:
        cols_sql = ", ".join([f"{col} {type}" for col, type in schema.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({cols_sql});"
        execute_query(query)
    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
        return e
