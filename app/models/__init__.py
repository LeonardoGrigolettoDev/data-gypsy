from app.db.postgres import execute_query


class Model:
    def __init__(self, table: str):
        self.table = table

    def build_filter_clause(self, filters: dict):
        """Gera a cláusula WHERE dinamicamente com base nos filtros, suportando operadores."""
        if not filters:
            return ""

        conditions = []
        for col, condition in filters.items():
            if isinstance(condition, list) and len(condition) == 2:
                operator, value = condition

                match operator.lower():
                    case "between":
                        conditions.append(f"{col} BETWEEN '{
                                          value[0]}' AND '{value[1]}'")
                    case "in":
                        values_str = ", ".join(f"'{v}'" for v in value)
                        conditions.append(f"{col} IN ({values_str})")
                    case "like":
                        conditions.append(f"{col} LIKE '{value}'")
                    case ">":
                        conditions.append(f"{col} > '{value}'")
                    case "<":
                        conditions.append(f"{col} < '{value}'")
                    case ">=":
                        conditions.append(f"{col} >= '{value}'")
                    case "<=":
                        conditions.append(f"{col} <= '{value}'")
                    case "=":
                        conditions.append(f"{col} = '{value}'")
                    case "!=":
                        conditions.append(f"{col} != '{value}'")
                    case _:
                        raise ValueError(
                            f"Operador '{operator}' não suportado.")
            else:
                conditions.append(f"{col} = '{condition}'")

        return " WHERE " + " AND ".join(conditions)

    def insert(self, data: dict):
        columns = ", ".join(data.keys())
        values = ", ".join([f"'{v}'" for v in data.values()])
        query = f"INSERT INTO {self.table} ({columns}) VALUES ({
            values}) RETURNING *;"
        return execute_query(query)

    def update(self, data: dict, id: str = None, filters: dict = None):
        set_clause = ", ".join(
            [f"{col} = '{val}'" for col, val in data.items()])
        where_clause = f" WHERE id = '{
            id}'" if id else self.build_filter_clause(filters)

        if not where_clause:
            return {"error": "É necessário um ID ou filtros para atualizar registros"}

        query = f"UPDATE {self.table} SET {
            set_clause}{where_clause} RETURNING *;"
        return execute_query(query)

    def delete(self, id: str = None, filters: dict = None):
        where_clause = f" WHERE id = '{
            id}'" if id else self.build_filter_clause(filters)

        if not where_clause:
            return {"error": "É necessário um ID ou filtros para deletar registros"}

        query = f"DELETE FROM {self.table}{where_clause} RETURNING *;"
        return execute_query(query)

    def read(self, id: str = None, filters: dict = None):
        where_clause = f" WHERE id = '{
            id}'" if id else self.build_filter_clause(filters)
        query = f"SELECT * FROM {self.table}{where_clause};"
        return execute_query(query)
