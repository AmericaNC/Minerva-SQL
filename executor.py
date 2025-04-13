#  ___      ___   __    _____  ___    _______  
# |"  \    /"  | |" \  (\"   \|"  \  /"     "| 
#  \   \  //   | ||  | |.\\   \    |(: ______) 
#  /\\  \/.    | |:  | |: \.   \\  | \/    |   
# |: \.        | |.  | |.  \    \. | // ___)_  
# |.  \    /:  | /\  |\|    \    \ |(:      "| 
# |___|\__/|___|(__\_|_)\___|\____\) \_______)
# 
# MinervaSQL - Intérprete SQL en Español v1.0

from colorama import Fore, Style
from user_manager import UserManager;
import os

class Executor:
    def __init__(self, db, usuarios: UserManager):
        self.db = db
        self.usuarios = usuarios

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
        result = f"Base de datos actual: {self.db.current_db}"
        return Fore.GREEN + result + Style.RESET_ALL
    
    def execute_drop_database(self, db_name):
        self.check_permission("eliminar")
        if db_name == self.db.current_db:
            return "No se puede eliminar la base de datos actualmente en uso."
        try:
            self.db.drop_database(db_name)
            return f"Base de datos '{db_name}' eliminada correctamente."
        except Exception as e:
            return f"Error al eliminar base de datos: {str(e)}"

    def execute_create_user(self, username, password):
        self.check_permission("crear_usuario")
        self.usuarios.agregar_usuario(username, password)
        return f"Usuario '{username}' creado."


    def execute_login(self, username, password):
        if self.usuarios.verificar_credenciales(username, password):
            self.db.current_user = username
            result = f"Sesión iniciada como '{username}'."
            return Fore.GREEN + result + Style.RESET_ALL
        else:
            raise ValueError("Usuario o contraseña incorrectos.")

    def execute_eliminar_usuario(self, nombre):
        usuario_actual = self.db.current_user  # Obtener el usuario actual
        permisos = self.usuarios.obtener_permisos(usuario_actual)
        if "eliminar_usuario" not in permisos:
            return "Error: Permiso 'eliminar_usuario' requerido."
        if nombre == "root":
            return "Error: No se puede eliminar el usuario root."
        if nombre == usuario_actual:
            return "Error: No puedes eliminar tu propio usuario mientras estás conectado."
        if nombre not in self.usuarios.usuarios:
            return f"Error: El usuario '{nombre}' no existe."
        del self.usuarios.usuarios[nombre]
        self.usuarios.guardar_usuarios()
        return f"Usuario '{nombre}' eliminado correctamente."

    def execute_show_databases(self):
        self.check_permission("ver_bases")
        dbs = self.db.list_databases()
        return dbs  # ← Devuelve la lista real, no el string formateado

    def execute_grant(self, permiso, usuario):
        self.check_permission("otorgar")
        self.usuarios.otorgar_permiso(usuario, permiso)  # ← ya persiste en el archivo
        return f"Permiso '{permiso}' otorgado al usuario '{usuario}'."

    def execute_show_tables(self):
        self.check_permission("ver_tablas")
        current_db = self.db.current_db
        self.db.databases[current_db] = self.db.load_tables(current_db)  # << Esta línea es clave
        return list(self.db.databases[current_db].keys())

    
    def execute_show_tables_in(self, db_name):
        self.check_permission("ver_tablas")
        if db_name not in self.db.databases:
          raise ValueError(f"La base de datos '{db_name}' no existe.")
        return list(self.db.databases[db_name].keys())

    def execute_insert(self, table_name, values, columns):
        self.check_permission("insertar")
        if table_name not in self.db.tables:
            raise ValueError(f"Tabla '{table_name}' no existe")
        entry = dict(zip(columns, values))
        self.db.tables[table_name].append(entry)
        self.db.save_table(table_name)  # 💾 Guardar automáticamente
        return f"Insertado en {table_name}: {entry}"

    def execute_use(self, db_name):
       self.check_permission("usar_base")
       if db_name not in self.db.databases:
        raise ValueError(f"La base de datos '{db_name}' no existe.")
       self.db.current_db = db_name
       self.db.tables = self.db.load_tables(db_name)
       result = f"Usando base de datos: {db_name}"
       return Fore.GREEN + result + Style.RESET_ALL

    def execute_show_users(self):
        self.check_permission("ver_usuarios")
        lista = []
        for nombre, info in self.usuarios.usuarios.items():
            permisos = info.get("permisos", [])
            permisos_str = ", ".join(permisos) if permisos else "Sin permisos"
            lista.append(f"- {nombre} (Permisos: {permisos_str})")
        return "Usuarios registrados:\n" + "\n".join(lista) if lista else "No hay usuarios registrados."


    def check_permission(self, permiso):
        permisos = self.usuarios.obtener_permisos(self.db.current_user)
        if permiso not in permisos:
            raise PermissionError(f"Permiso '{permiso}' requerido.")


    def execute_create_database(self, name):
        self.check_permission("crear_base")
        if name in self.db.databases:
            result = f"La base de datos '{name}' ya existe."
            return Fore.RED + result + Style.RESET_ALL
        self.db.databases[name] = {}
        db_folder = self.db.databases_path / name
        db_folder.mkdir(exist_ok=True)
        result = f"Base de datos '{name}' creada exitosamente."
        return Fore.GREEN + result + Style.RESET_ALL

    def execute_update(self, table_name, column, value, where_clause):
        self.check_permission("actualizar")
        resultado = self.db.update(table_name, column, value, where_clause)
        self.db.save_table(table_name)  # 💾 Guardar cambios
        return f"Filas actualizadas: {resultado}"

    def execute_current_user(self):
        user = self.db.current_user
        return f"Usuario actual: {user}" if user else "No hay sesión activa."

    def execute_count(self, table_name, where_clause):
        self.check_permission("contar")
        return self.db.count(table_name, where_clause)
    
    def execute_delete(self, table_name, where_clause):
        self.check_permission("eliminar")
        deleted_rows = self.db.delete(table_name, where_clause)
        self.db.save_table(table_name)  # 💾 Guardar cambios
        result = f"Filas eliminadas: {deleted_rows}"
        return Fore.GREEN + result + Style.RESET_ALL
    
    def execute_create(self, table_name, columns):
        self.check_permission("crear_tabla")
        if table_name in self.db.tables:
            raise ValueError(f"La tabla '{table_name}' ya existe.")
        self.db.tables[table_name] = []
        self.db.save_table(table_name)  # 💾 Guardar la nueva tabla
        result = f"Tabla '{table_name}' creada con columnas {columns}."
        return Fore.GREEN + result + Style.RESET_ALL

    def execute_drop_table(self, table_name):
        self.check_permission("eliminar")
        success = self.db.drop_table(table_name)
        return f"Tabla '{table_name}' eliminada." if success else f"No se pudo eliminar la tabla '{table_name}'."


    def execute_drop(self, table_name):
        self.check_permission("eliminar_tabla")
        if table_name in self.db.tables:
            del self.db.tables[table_name]
            db_folder = self.db.databases_path / self.db.current_db
            file_path = db_folder / f"{table_name}.json"
            if file_path.exists():
                file_path.unlink()  # 🗑️ Borrar archivo
                result = f"Tabla '{table_name}' eliminada."
            return Fore.GREEN + result + Style.RESET_ALL
        else:
            result = f"La tabla '{table_name}' no existe."
            return Fore.GREEN + result + Style.RESET_ALL


