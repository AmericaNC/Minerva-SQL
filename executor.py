class Executor:
    def __init__(self, db):
        self.db = db

    def execute(self, parsed_query):
        if parsed_query["type"] == "SELECT":
            return self.db.select(parsed_query["table"], parsed_query["columns"], parsed_query["where"])
        elif parsed_query["type"] == "INSERT":
            return self.execute_insert(parsed_query["table"], parsed_query["values"])

    def execute_create_user(self, username, password):
        return self.db.create_user(username, password)

    def execute_login(self, username, password):
        return self.db.login(username, password)
    
    def execute_eliminar_usuario(self, username):
        if username not in self.db.users:
            return f"El usuario '{username}' no existe."
        del self.db.users[username]
        return f"Usuario '{username}' eliminado."
    
    def execute_show_databases(self):
        return list(self.db.databases.keys())
    
    def execute_show_tables(self):
        current_db = self.db.current_db
        return list(self.db.databases[current_db].keys())


    def execute_insert(self, table_name, values, columns):
        return self.db.insert(table_name, values, columns)
    
    def execute_use(self, db_name):
        return self.db.use_database(db_name)
    
    def execute_create_database(self, name):
        if name in self.db.databases:
            return f"La base de datos '{name}' ya existe."
        self.db.databases[name] = {}
        return f"Base de datos '{name}' creada exitosamente."

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

