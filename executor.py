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
        self.en_transaccion = False
        self.cambios_pendientes = []

    def begin(self):
        if self.en_transaccion:
            return "Ya hay una transacción activa."
        self.en_transaccion = True
        self.cambios_pendientes = []
        return "Transacción iniciada."

    def commit(self):
        if not self.en_transaccion:
            return "No hay transacción activa."
        for accion, args in self.cambios_pendientes:
            accion(*args)  # Ejecuta el insert real
        self.en_transaccion = False
        self.cambios_pendientes.clear()
        return "Transacción confirmada (COMMIT)."


    def rollback(self):
        if not self.en_transaccion:
            return "No hay transacción activa."
    
        self.cambios_pendientes.clear()
        self.en_transaccion = False
        return "Transacción cancelada (ROLLBACK)."


    def execute(self, parsed_query):
        if parsed_query["type"] == "SELECT":
            try:
            # Pasa la dirección de ordenamiento a la función select
                return self.db.select(
                    parsed_query["table"],
                    parsed_query["columns"],
                    parsed_query.get("where"),
                    parsed_query.get("order_by"),
                    parsed_query.get("order_direction") # <--- Línea agregada
                )
            except Exception as e:
                return f"Error: {e}"

        elif parsed_query["type"] == "INSERT":
            return self.execute_insert(parsed_query["table"], parsed_query["values"])
        elif parsed_query["type"] == "CURRENT_USER":
            return self.execute_current_user()
        elif parsed_query["type"] == "CURRENT_DATABASE":
            return self.execute_current_database()
        elif parsed_query["type"] == "CREATE_TRIGGER":
            return self.execute_create_trigger(
                parsed_query["trigger_name"],
                parsed_query["table"],
                parsed_query["event"],
                parsed_query["timing"]
            )


    def execute_show_triggers(self, table_name=None):
        triggers = self.db.triggers
        if table_name:
            table_triggers = triggers.get(table_name, {})
            if not table_triggers:
                return f"No hay triggers en la tabla '{table_name}'."
            result = [f"Evento '{event}': {[func.__name__ for func in funcs]}" 
                    for event, funcs in table_triggers.items()]
            return "\n".join(result)
        else:
            all_triggers = []
            for table, events in triggers.items():
                for event, funcs in events.items():
                    all_triggers.append(f"Tabla '{table}', Evento '{event}': {[func.__name__ for func in funcs]}")
            return "\n".join(all_triggers) if all_triggers else "No hay triggers registrados."

    def execute_create_trigger(self, trigger_name, table_name, event, timing="DESPUES"):
        """
        trigger_name: nombre del trigger
        table_name: tabla sobre la que actúa
        event: INSERT, UPDATE, DELETE
        timing: ANTES o DESPUES (opcional)
        """
        self.check_permission("crear_trigger")

    # Definir trigger simple que solo imprime el registro
        def trigger_func(row):
            print(f"[TRIGGER {trigger_name}] Evento {event} en {table_name}: {row}")

        self.db.add_trigger(table_name, event, trigger_func)
        return f"Trigger '{trigger_name}' agregado a la tabla '{table_name}' para {timing} {event}."


    def execute_current_database(self):
        result = f"Base de datos actual: {self.db.current_db}"
        return Fore.GREEN + result + Style.RESET_ALL
  
    def execute_drop_database(self, db_name):
        self.check_permission("eliminar")
        if db_name == self.db.current_db:
            return "No se puede eliminar la base de datos actualmente en uso."
        def accion(nombre):
            self.db.drop_database(nombre)

        if self.en_transaccion:
        # Guardar en la lista de cambios pendientes
            self.cambios_pendientes.append((accion, (db_name,)))
            return f"DROP DATABASE '{db_name}' registrado en transacción."
        else:
            try:
                self.db.drop_database(db_name)
                return f"Base de datos '{db_name}' eliminada correctamente."
            except Exception as e:
                return f"Error al eliminar base de datos: {str(e)}"

    def execute_create_user(self, username, password):
        self.check_permission("crear_usuario")
        def accion(u, p):
            self.usuarios.agregar_usuario(u, p)
        if self.en_transaccion:
        # Guardar en la lista de cambios pendientes
            self.cambios_pendientes.append((accion, (username, password)))
            return f"CREATE USER '{username}' registrado en transacción."
        else:
        # Ejecución inmediata
            self.usuarios.agregar_usuario(username, password)
            return f"Usuario '{username}' creado."

    #def execute_create_user(self, username, password):
    #    self.check_permission("crear_usuario")
    #    def accion_crear_usuario(u, p):
    #        self.usuarios.agregar_usuario(u, p)
    #        print(f"Usuario '{u}' creado exitosamente.")
    #        self.create_default_user_trigger(u)

    #    if self.en_transaccion:
    #        self.cambios_pendientes.append((accion_crear_usuario, (username, password)))
    #        return f"CREATE USER '{username}' registrado en transacción."
    #    else:
    #        accion_crear_usuario(username, password)
    #        return f"Usuario '{username}' creado, y trigger asociado inicializado."

    def create_default_user_trigger(self, username):
        """
        Función que crea un trigger predefinido para el nuevo usuario.
        """
        def user_login_message():
            print(f"¡Bienvenido! El usuario '{username}' acaba de iniciar sesión. 👋")
        print(f"Trigger para el usuario '{username}' creado y activado.")

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
        return dbs  

    def execute_grant(self, permiso, usuario):
        self.check_permission("otorgar")
        def accion(p, u):
            self.usuarios.otorgar_permiso(u, p)
        if self.en_transaccion:
            self.cambios_pendientes.append((accion, (permiso, usuario)))
            return f"GRANT '{permiso}' a '{usuario}' registrado en transacción."
        else:
            self.usuarios.otorgar_permiso(usuario, permiso)
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
    
    def execute_insert(self, tabla, valores, columnas=None):
        self.check_permission("insertar")
        def accion(table_name, values, cols):
            self.db.insert(table_name, values, cols) 
        if self.en_transaccion:
            self.cambios_pendientes.append((accion, (tabla, valores.copy(), columnas.copy() if columnas else None)))
            return f"INSERT en {tabla} registrado en transacción."
        else:
            return self.db.insert(tabla, valores, columnas)

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
    
    def execute_revoke(self, permiso, usuario):
        self.check_permission("otorgar")
        def accion(p, u):
            self.usuarios.revocar_permiso(u, p)
        if self.en_transaccion:
            self.cambios_pendientes.append((accion, (permiso, usuario)))
            return f"REVOKE '{permiso}' de '{usuario}' registrado en transacción."
        else:
            if not self.usuarios.revocar_permiso(usuario, permiso):
                return f"El usuario '{usuario}' no tenía el permiso '{permiso}'."
            return f"Permiso '{permiso}' revocado al usuario '{usuario}'."

    def check_permission(self, permiso):
        permisos = self.usuarios.obtener_permisos(self.db.current_user)
        if permiso not in permisos:
            raise PermissionError(f"Permiso '{permiso}' requerido.")

    def execute_create_database(self, name):
        self.check_permission("crear_base")

    # Acción diferida para COMMIT
        def accion(nombre):
            if nombre in self.db.databases:
                raise RuntimeError(f"La base de datos '{nombre}' ya existe.")  # si ya existe al commit, error
            self.db.databases[nombre] = {}
            db_folder = self.db.databases_path / nombre
            db_folder.mkdir(exist_ok=True)

        if self.en_transaccion:
            self.cambios_pendientes.append((accion, (name,)))
            return f"CREATE DATABASE '{name}' registrado en transacción."
        else:
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

    # Acción diferida para COMMIT
        def accion(tn, col, val, wc):
            resultado = self.db.update(tn, col, val, wc)
            self.db.save_table(tn)  # 💾 Guardar en disco
            return resultado

        if self.en_transaccion:
            self.cambios_pendientes.append((accion, (table_name, column, value, where_clause)))
            return f"UPDATE en '{table_name}' registrado en transacción."
        else:
            resultado = self.db.update(table_name, column, value, where_clause)
            self.db.save_table(table_name)  # 💾 Guardar en disco
            return f"Filas actualizadas: {resultado}"

    def execute_current_user(self):
        user = self.db.current_user
        return f"Usuario actual: {user}" if user else "No hay sesión activa."

    def execute_count(self, table_name, where_clause):
        self.check_permission("contar")
        return self.db.count(table_name, where_clause)
   
    
    def execute_create(self, table_name, columns):
        self.check_permission("crear_tabla")

    # Acción diferida para COMMIT
        def accion(tn, cols):
            if tn in self.db.tables:
                raise ValueError(f"La tabla '{tn}' ya existe.")
            self.db.tables[tn] = []
            self.db.save_table(tn)  # 💾 Guardar en disco
            return f"Tabla '{tn}' creada con columnas {cols}."

        if self.en_transaccion:
            self.cambios_pendientes.append((accion, (table_name, columns)))
            return f"CREATE TABLE '{table_name}' registrado en transacción."
        else:
            if table_name in self.db.tables:
                raise ValueError(f"La tabla '{table_name}' ya existe.")
            self.db.tables[table_name] = []
            self.db.save_table(table_name)  # 💾 Guardar en disco
            result = f"Tabla '{table_name}' creada con columnas {columns}."
            return Fore.GREEN + result + Style.RESET_ALL

    def execute_mostrar_tablas(self):
        db_name = self.db.current_db
        tablas = list(self.db.tables.keys())
        return f"Tablas en la base '{db_name}': {tablas}"

    def execute_describe(self, table_name):
        if table_name not in self.db.tables:
            return f"Error: La tabla '{table_name}' no existe."
    
        table_columns = list(self.db.tables[table_name][0].keys()) if self.db.tables[table_name] else []
        num_rows = len(self.db.tables[table_name])
    
    # Resultado visual
        result = f"Tabla '{table_name}':\nColumnas: {table_columns}\nFilas: {num_rows}"
        return result

    def execute_drop_table(self, table_name):
        self.check_permission("eliminar")

    # Acción diferida para COMMIT
        def accion(tn):
            success = self.db.drop_table(tn)
            return f"Tabla '{tn}' eliminada." if success else f"No se pudo eliminar la tabla '{tn}'."

        if self.en_transaccion:
            self.cambios_pendientes.append((accion, (table_name,)))
            return f"DROP TABLE '{table_name}' registrado en transacción."
        else:
            success = self.db.drop_table(table_name)
            return f"Tabla '{table_name}' eliminada." if success else f"No se pudo eliminar la tabla '{table_name}'."



