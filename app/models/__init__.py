from app.db.postgres import execute_query


class Model:
    def __init__(self, table: str):
        self.table = table

    def insert(self, data: dict):
        columns = ", ".join(data.keys())
        values = ", ".join([f"'{v}'" for v in data.values()])
        query = f"INSERT INTO {self.table} ({columns}) VALUES ({values}) RETURNING *;"
        res = execute_query(query)
        return res
   
