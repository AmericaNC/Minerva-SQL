class Executor:
    def __init__(self, db):
        self.db = db

    def execute(self, parsed_query):
        if parsed_query["type"] == "SELECT":
            return self.db.select(parsed_query["table"], parsed_query["columns"], parsed_query["where"])
        elif parsed_query["type"] == "INSERT":
            return self.execute_insert(parsed_query["table"], parsed_query["values"])
        elif parsed_query["type"] == "CURRENT_USER":
            return self.execute_current_user()
        elif parsed_query["type"] == "CURRENT_DATABASE":
            return self.execute_current_database()

    
    def execute_current_database(self):
        return f"Base de datos actual: {self.db.current_db}"

    def execute_create_user(self, username, password):
        return self.db.create_user(username, password)

    def execute_login(self, username, password):
        if username in self.db.users and self.db.users[username] == password:
            self.db.current_user = username
            return f"Sesión iniciada como '{username}'."
        else:
            raise ValueError("Usuario o contraseña incorrectos.")

    
    def execute_eliminar_usuario(self, username):
        self.check_permission("eliminar_usuario")
        if username not in self.db.users:
            return f"El usuario '{username}' no existe."
        del self.db.users[username]
        return f"Usuario '{username}' eliminado."
    
    def execute_show_databases(self):
        self.check_permission("ver_bases")
        return list(self.db.databases.keys())
    
    def execute_grant(self, permiso, usuario):
        self.check_permission("otorgar")
        if usuario not in self.db.users:
            raise ValueError(f"El usuario '{usuario}' no existe.")
        if usuario not in self.db.permissions:
            self.db.permissions[usuario] = set()
        self.db.permissions[usuario].add(permiso)
        return f"Permiso '{permiso}' otorgado al usuario '{usuario}'."

    
    def execute_show_tables(self):
        self.check_permission("ver_tablas")
        current_db = self.db.current_db
        return list(self.db.databases[current_db].keys())
    
    def execute_show_tables_in(self, db_name):
        self.check_permission("ver_tablas")
        if db_name not in self.db.databases:
          raise ValueError(f"La base de datos '{db_name}' no existe.")
        return list(self.db.databases[db_name].keys())

    def execute_insert(self, table_name, values, columns):
        self.check_permission("insertar")
        return self.db.insert(table_name, values, columns)
    
    def execute_use(self, db_name):
       self.check_permission("usar_base")
       if db_name not in self.db.databases:
        raise ValueError(f"La base de datos '{db_name}' no existe.")
       self.db.current_db = db_name
       return f"Usando base de datos: {db_name}"

    def execute_show_users(self):
       self.check_permission("ver_usuarios")
       if not self.db.users:
        return "No hay usuarios registrados."
       return "Usuarios: " + ", ".join(self.db.users.keys())
    
    def check_permission(self, permiso):
        if self.db.current_user is None:
            raise PermissionError("Debes iniciar sesión primero.")
        user = self.db.current_user
        if user not in self.db.permissions or permiso not in self.db.permissions[user]:
            raise PermissionError(f"Permiso '{permiso}' requerido.")


    def execute_create_database(self, name):
        self.check_permission("crear_base")
        if name in self.db.databases:
            return f"La base de datos '{name}' ya existe."
        self.db.databases[name] = {}
        return f"Base de datos '{name}' creada exitosamente."

    def execute_update(self, table_name, column, value, where_clause):
        self.check_permission("actualizar")
        #print(f"\n🔍 Ejecutando UPDATE en '{table_name}' - SET {column} = {value} DONDE {where_clause}")
        resultado = self.db.update(table_name, column, value, where_clause)
        #print(f"🛠 Resultado de UPDATE: {resultado}")
        return resultado
    
    def execute_current_user(self):
        user = self.db.current_user
        return f"Usuario actual: {user}" if user else "No hay sesión activa."

    def execute_count(self, table_name, where_clause):
        self.check_permission("contar")
        return self.db.count(table_name, where_clause)
    
    def execute_delete(self, table_name, where_clause):
        self.check_permission("eliminar")
        deleted_rows = self.db.delete(table_name, where_clause)
        return f"Filas eliminadas: {deleted_rows}"
    
    def execute_create(self, table_name, columns):
        self.check_permission("crear_tabla")
        db = self.db.databases[self.db.current_db]
        if table_name in db:
          raise ValueError(f"La tabla '{table_name}' ya existe.")
        db[table_name] = {"columns": columns, "rows": []}
        return f"Tabla '{table_name}' creada con columnas {columns}."

    def execute_drop(self, table_name):
        self.check_permission("eliminar_tabla")
        if table_name in self.db.tables:
            del self.db.tables[table_name]
            return f"Tabla '{table_name}' eliminada."
        else:
            return f"La tabla '{table_name}' no existe."

