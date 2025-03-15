class Executor:
    def __init__(self, db):
        self.db = db

    def execute(self, parsed_query):
        if parsed_query["type"] == "SELECT":
            return self.db.select(parsed_query["table"], parsed_query["columns"], parsed_query["where"])
        elif parsed_query["type"] == "INSERT":
            return self.execute_insert(parsed_query["table"], parsed_query["values"])

    def execute_insert(self, table_name, values):
        self.db.insert(table_name, values)
        return f"Datos insertados en la tabla '{table_name}': {values}"

    def execute_update(self, table_name, column, value, where_clause):
        #print(f"\n🔍 Ejecutando UPDATE en '{table_name}' - SET {column} = {value} DONDE {where_clause}")
        resultado = self.db.update(table_name, column, value, where_clause)
        #print(f"🛠 Resultado de UPDATE: {resultado}")
        return resultado


