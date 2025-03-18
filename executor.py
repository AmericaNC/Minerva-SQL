class Executor:
    def __init__(self, db):
        self.db = db

    def execute(self, parsed_query):
        if parsed_query["type"] == "SELECT":
            return self.db.select(parsed_query["table"], parsed_query["columns"], parsed_query["where"])
        elif parsed_query["type"] == "INSERT":
            return self.execute_insert(parsed_query["table"], parsed_query["values"])

    def execute_insert(self, table_name, values, columns):
        return self.db.insert(table_name, values, columns)

    def execute_update(self, table_name, column, value, where_clause):
        #print(f"\n🔍 Ejecutando UPDATE en '{table_name}' - SET {column} = {value} DONDE {where_clause}")
        resultado = self.db.update(table_name, column, value, where_clause)
        #print(f"🛠 Resultado de UPDATE: {resultado}")
        return resultado
    
    def execute_count(self, table_name, where_clause):
        return self.db.count(table_name, where_clause)
    
    def execute_delete(self, table_name, where_clause):
        deleted_rows = self.db.delete(table_name, where_clause)
        return f"Filas eliminadas: {deleted_rows}"
    
    def execute_create(self, table_name, columns):
        return self.db.create_table(table_name, columns)
    
    def execute_drop(self, table_name):
        if table_name in self.db.tables:
            del self.db.tables[table_name]
            return f"Tabla '{table_name}' eliminada."
        else:
            return f"La tabla '{table_name}' no existe."

