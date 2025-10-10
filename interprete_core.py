import sys
import json
import os
from lexer import lexer
from parser.select_parser import SelectParser
from parser.eliminar_usuario_parser import EliminarUsuarioParser
from parser.show_parser import ShowDatabasesParser
from parser.grant_parser import GrantParser
from parser.update_parser import UpdateParser
from parser.insert_parser import InsertParser
from parser.delete_parser import DeleteParser
from parser.create_parser import CreateTableParser
from parser.create_user_parser import CreateUserParser
from parser.login_parser import LoginParser
from parser.create_database_parser import CreateDatabaseParser
from parser.count_parser import CountParser
from parser.use_parser import UseDatabaseParser
from user_manager import UserManager
from parser.drop_parser import DropParser
from executor import Executor
from database import Database

# --- Nuevas importaciones de main.py ---
from parser.show_tables_parser import ShowTablesParser
from parser.show_tables_in_parser import ShowTablesInParser
from parser.show_users_parser import ShowUsersParser
from parser.drop_database_parser import DropDatabaseParser
from parser.transaction_parse import TransactionParser
from parser.revoke_parser import RevokeParser
from parser.show_trigger import ShowTriggersParser

# --- Funciones de ayuda para el comando HELP ---
def resource_path(relative_path):
    """ Obtiene la ruta absoluta al recurso, sin importar si se ejecuta como script o como ejecutable """
    try:
        # PyInstaller crea una carpeta temporal y guarda el path ahí
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def cargar_ayuda():
    """ Carga la documentación de ayuda desde un archivo JSON. """
    try:
        ruta = resource_path('help_docs.json')
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        # Si falla, retorna una estructura vacía para no bloquear el programa.
        return {"comandos": {}, "permisos": {}}

# --- INICIALIZACIÓN (Se ejecuta una sola vez) ---
db = Database()
usuarios = UserManager("usuarios.json")
executor = Executor(db, usuarios)
help_data = cargar_ayuda() # Cargar los datos de ayuda al iniciar
debug_mode = False 
base_global = None# <--- AÑADIDO: Variable global para el modo depuración

# Llenar base de datos con algunos datos iniciales (opcional)
db.tables["datos"] = [
    {"HR": 90, "TEMP": 36.5},
    {"HR": 110, "TEMP": 37.2},
    {"HR": 120, "TEMP": 38.0},
]
# --------------------------------------------------------------------------

def procesar_consulta(query):
    """
    Esta función recibe una consulta como string, la procesa y devuelve
    el resultado también como un string.
    """
    global debug_mode # Indicar que vamos a modificar la variable global
    global usuario_global
    global base_global

    if query.strip().upper() == "MODO DEPURACION":
        debug_mode = not debug_mode
        estado = "activado" if debug_mode else "desactivado"
        return f"🔍 Modo depuración {estado}."
    
    if not query.strip():
        return "Por favor, ingresa un comando."
    
    if query.lower().strip() in ["salir", "exit"]:
        return "Sesión terminada."

    try:
        tokens = lexer(query)
        # <--- AÑADIDO: Lógica para acumular información de depuración
        debug_info = ""
        if debug_mode:
            debug_info += f"--- [DEBUG LEX] TOKENS ---\n{json.dumps(tokens, indent=2, ensure_ascii=False)}\n\n"

        if not tokens:
            return "Error: No se pudo procesar el comando. Revisa la sintaxis."
        
        # --- LÓGICA DEL INTÉRPRETE (Unificada) ---
        
        comando_principal = tokens[0][1] if len(tokens) > 0 else ''
        
        if comando_principal == "SELECCIONA":
            parser = SelectParser(tokens)
            parsed_query = parser.parse()
            if debug_mode:
                debug_info += f"--- [DEBUG PARSER] ÁRBOL SINTÁCTICO ---\n{json.dumps(parsed_query, indent=2, ensure_ascii=False)}\n\n"
            result = executor.execute(parsed_query)
            return f"{debug_info}Resultado: {result}"

        elif comando_principal == "OTORGAR":
            parser = GrantParser(tokens)
            parsed_query = parser.parse()
            if debug_mode:
                debug_info += f"--- [DEBUG PARSER] ÁRBOL SINTÁCTICO ---\n{json.dumps(parsed_query, indent=2, ensure_ascii=False)}\n\n"
            result = executor.execute_grant(parsed_query["permiso"], parsed_query["usuario"])
            return f"{debug_info}{result}"

        elif comando_principal == "INSERTAR":
            parser = InsertParser(tokens)
            parsed_query = parser.parse()
            if debug_mode:
                debug_info += f"--- [DEBUG PARSER] ÁRBOL SINTÁCTICO ---\n{json.dumps(parsed_query, indent=2, ensure_ascii=False)}\n\n"
            result = executor.execute_insert(parsed_query["table"], parsed_query["values"], parsed_query["columns"])
            return f"{debug_info}Resultado: {result}"

        # Bloque corregido (Aproximadamente línea 100)
        # Bloque USE corregido para una sincronización robusta
        elif tokens[0][0] == "USE":
            parser = UseDatabaseParser(tokens)
            parsed_query = parser.parse()

            if debug_mode:
                debug_info += f"--- [DEBUG PARSER] ÁRBOL SINTÁCTICO ---\n{json.dumps(parsed_query, indent=2, ensure_ascii=False)}\n\n"

    # 1. Ejecutamos el comando
            result = executor.execute_use(parsed_query["database"])

    # 2. Sincronizamos base_global si NO detectamos un mensaje de error.
    #    Esto es más robusto que buscar un mensaje de éxito exacto.
            if "Error" not in result and "no existe" not in result and "fallida" not in result:
        # Si no hay error visible, asumimos éxito y actualizamos el estado global.
                global base_global
                base_global = parsed_query["database"]

            return f"{debug_info}Resultado: {result}"

        elif tokens[0][0] == "CREATE" and len(tokens) > 1 and tokens[1][0] == "DATABASE":
            parser = CreateDatabaseParser(tokens)
            parsed_query = parser.parse()
            if debug_mode:
                debug_info += f"--- [DEBUG PARSER] ÁRBOL SINTÁCTICO ---\n{json.dumps(parsed_query, indent=2, ensure_ascii=False)}\n\n"
            result = executor.execute_create_database(parsed_query["database"])
            return f"{debug_info}Resultado: {result}"
        
        elif tokens[0][0] == "CREATE" and len(tokens) > 1 and tokens[1][0] == "USER":
            parser = CreateUserParser(tokens)
            parsed_query = parser.parse()
            if debug_mode:
                debug_info += f"--- [DEBUG PARSER] ÁRBOL SINTÁCTICO ---\n{json.dumps(parsed_query, indent=2, ensure_ascii=False)}\n\n"
            result = executor.execute_create_user(parsed_query["username"], parsed_query["password"])
            return f"{debug_info}Resultado: {result}"

        elif tokens[0][0] == "CREATE": # Asumimos CREATE TABLE por defecto
            parser = CreateTableParser(tokens)
            parsed_query = parser.parse()
            if debug_mode:
                debug_info += f"--- [DEBUG PARSER] ÁRBOL SINTÁCTICO ---\n{json.dumps(parsed_query, indent=2, ensure_ascii=False)}\n\n"
            result = executor.execute_create(parsed_query["table"], parsed_query["columns"])
            return f"{debug_info}Resultado: {result}"

        elif (tokens[0][0] == "ELIMINAR" or tokens[0][0] == "BORRAR") and len(tokens) > 1 and tokens[1][0] == "USER":
            parser = EliminarUsuarioParser(tokens)
            parsed_query = parser.parse()
            if debug_mode:
                debug_info += f"--- [DEBUG PARSER] ÁRBOL SINTÁCTICO ---\n{json.dumps(parsed_query, indent=2, ensure_ascii=False)}\n\n"
            # NOTA: `usuario_actual` no está definido en este contexto. Se usa 'root' como fallback.
            # Para una implementación completa, esta función debería recibir el usuario que ejecuta la acción.
            result = executor.execute_eliminar_usuario(parsed_query["nombre"], "root") 
            return f"{debug_info}Resultado: {result}"
        
        elif comando_principal == "MOSTRAR" and len(tokens) > 1 and tokens[1][1] == "BASES":
            result = executor.execute_show_databases()
            output = "Bases de datos disponibles:\n"
            output += "\n".join(f"  • {db_name}" for db_name in result)
            return f"{debug_info}{output}"
            
        elif comando_principal == "MOSTRAR" and len(tokens) > 3 and tokens[1][1] == "TABLAS" and tokens[2][1] == "EN":
             parser = ShowTablesInParser(tokens)
             parsed_query = parser.parse()
             if debug_mode:
                 debug_info += f"--- [DEBUG PARSER] ÁRBOL SINTÁCTICO ---\n{json.dumps(parsed_query, indent=2, ensure_ascii=False)}\n\n"
             result = executor.execute_show_tables_in(parsed_query["database"])
             if result:
                 return f"{debug_info}Tablas en '{parsed_query['database']}': {', '.join(result)}"
             else:
                 return f"{debug_info}No hay tablas en la base de datos '{parsed_query['database']}' o no existe."

        elif comando_principal == "MOSTRAR" and len(tokens) > 1 and tokens[1][1] == "TABLAS":
            result = executor.execute_show_tables()
            if result:
                output = "Tablas:\n"
                output += "\n".join(f"  • {table_name}" for table_name in result)
                return f"{debug_info}{output}"
            else:
                return f"{debug_info}No hay tablas en la base de datos actual."

        elif comando_principal == "MOSTRAR" and len(tokens) > 1 and tokens[1][1] == "USUARIOS":
            result = executor.execute_show_users()
            return f"{debug_info}{str(result)}"

        elif comando_principal == "MOSTRAR" and len(tokens) > 1 and tokens[1][1] == "TRIGGERS":
            parser = ShowTriggersParser(tokens)
            parsed_query = parser.parse()
            if debug_mode:
                debug_info += f"--- [DEBUG PARSER] ÁRBOL SINTÁCTICO ---\n{json.dumps(parsed_query, indent=2, ensure_ascii=False)}\n\n"
            result = executor.execute_show_triggers(parsed_query.get("table"))
            return f"{debug_info}Resultado: {result}"

        elif comando_principal == "ACTUALIZAR":
            parser = UpdateParser(tokens)
            parsed_query = parser.parse()
            if debug_mode:
                debug_info += f"--- [DEBUG PARSER] ÁRBOL SINTÁCTICO ---\n{json.dumps(parsed_query, indent=2, ensure_ascii=False)}\n\n"
            result = executor.execute_update(parsed_query["table"], parsed_query["column"], parsed_query["value"], parsed_query["where"])
            return f"{debug_info}Resultado: {result}"

        elif comando_principal == "BORRAR":
    # 1. Distinguir BORRAR USER
            if len(tokens) > 1 and tokens[1][0] == "USER":
                from parser.eliminar_usuario_parser import EliminarUsuarioParser # Importación necesaria si no está al inicio
                parser = EliminarUsuarioParser(tokens)
                parsed_query = parser.parse()
        
                if debug_mode:
                    debug_info += f"--- [DEBUG PARSER] ÁRBOL SINTÁCTICO ---\n{json.dumps(parsed_query, indent=2, ensure_ascii=False)}\n\n"
            
        # Ejecuta la eliminación de usuario
        # Nota: Asegúrate de que 'root' o 'usuario_global' se maneje correctamente
                result = executor.execute_eliminar_usuario(parsed_query["nombre"], "root") 
                return f"{debug_info}Resultado: {result}"
        
    # 2. BORRAR DE (Borrar registros)
            else:
        # Asume que esta es la sentencia para borrar registros (DELETE FROM)
                parser = DeleteParser(tokens)
                parsed_query = parser.parse()

            if debug_mode:
                debug_info += f"--- [DEBUG PARSER] ÁRBOL SINTÁCTICO ---\n{json.dumps(parsed_query, indent=2, ensure_ascii=False)}\n\n"
        
        # 🚨 CAMBIO CLAVE: Usamos el método genérico 'execute' 
        # que debe manejar la lógica de DELETE FROM internamente en la clase Executor.
            result = executor.execute(parsed_query) 
        
            return f"{debug_info}Resultado: {result}"
        
        elif comando_principal == "CONTAR":
            parser = CountParser(tokens)
            parsed_query = parser.parse()
            if debug_mode:
                debug_info += f"--- [DEBUG PARSER] ÁRBOL SINTÁCTICO ---\n{json.dumps(parsed_query, indent=2, ensure_ascii=False)}\n\n"
            result = executor.execute_count(parsed_query["table"], parsed_query["where"])
            return f"{debug_info}Resultado: {result}"

        # Bloque LOGIN (Aproximadamente línea 165)
        elif comando_principal == "LOGIN":
            parser = LoginParser(tokens)
            parsed_query = parser.parse()
    # ...
            result = executor.execute_login(parsed_query["username"], parsed_query["password"])
    
            if "Sesión iniciada" in result:
        # AHORA SÍ: Sincroniza el usuario logueado con la variable global
                usuario_global = parsed_query["username"] 
                return f"{debug_info}Sesión iniciada como '{usuario_global}'."
            else:
                return f"{debug_info}Resultado: {result}"
        
        # --- Nuevas funciones de main.py ---
        
        elif comando_principal == "DESHACER": # DROP TABLE
            parser = DropParser(tokens)
            parsed_query = parser.parse()
            if debug_mode:
                debug_info += f"--- [DEBUG PARSER] ÁRBOL SINTÁCTICO ---\n{json.dumps(parsed_query, indent=2, ensure_ascii=False)}\n\n"
            result = executor.execute_drop_table(parsed_query["table"])
            return f"{debug_info}Resultado: {result}"

        elif tokens[0][0] == "DELETE" and len(tokens) > 1 and tokens[1][0] == "DATABASE": # DROP DATABASE
            parser = DropDatabaseParser(tokens)
            parsed_query = parser.parse()
            if debug_mode:
                debug_info += f"--- [DEBUG PARSER] ÁRBOL SINTÁCTICO ---\n{json.dumps(parsed_query, indent=2, ensure_ascii=False)}\n\n"
            result = executor.execute_drop_database(parsed_query["name"])
            return f"{debug_info}Resultado: {result}"

        elif comando_principal == "REVOCAR":
            parser = RevokeParser(tokens)
            parsed_query = parser.parse()
            if debug_mode:
                debug_info += f"--- [DEBUG PARSER] ÁRBOL SINTÁCTICO ---\n{json.dumps(parsed_query, indent=2, ensure_ascii=False)}\n\n"
            result = executor.execute_revoke(parsed_query["permiso"], parsed_query["usuario"])
            return f"{debug_info}{result}"

        elif comando_principal in ["BEGIN", "COMMIT", "ROLLBACK"]:
            parser = TransactionParser(tokens)
            parsed_query = parser.parse()
            if debug_mode:
                debug_info += f"--- [DEBUG PARSER] ÁRBOL SINTÁCTICO ---\n{json.dumps(parsed_query, indent=2, ensure_ascii=False)}\n\n"
            if parsed_query["type"] == "BEGIN":
                result = executor.begin()
            elif parsed_query["type"] == "COMMIT":
                result = executor.commit()
            elif parsed_query["type"] == "ROLLBACK":
                result = executor.rollback()
            return f"{debug_info}{result}"
        
        elif comando_principal == "USUARIO_ACTUAL":
            return f"{debug_info}Usuario actual: {usuario_global}"

      # Bloque BASE_ACTUAL (corregido)
        elif comando_principal == "BASE_ACTUAL": # Ahora usa el valor correcto
            if base_global:
                return f"{debug_info}Base de datos actual: {base_global}"
            else:
                return f"{debug_info}No hay una base de datos seleccionada actualmente."

        elif comando_principal == "AYUDA":
             # El comando AYUDA no necesita parser, la info de tokens es suficiente
             output = ""
             if len(tokens) == 1:
                 output += "Comandos disponibles:\n"
                 for cmd, data in help_data.get("comandos", {}).items():
                     output += f"  • {cmd.ljust(15)} - {data['descripcion']}\n"
                 output += "\nPermisos disponibles:\n"
                 for permiso, desc in help_data.get("permisos", {}).items():
                     output += f"  • {permiso.ljust(15)} - {desc}\n"
                 output += "\nUsa AYUDA [comando] para detalles específicos."
                 return f"{debug_info}{output}"
             else:
                 cmd_ayuda = tokens[1][1]
                 info = help_data.get("comandos", {}).get(cmd_ayuda)
                 if info:
                     output += f"--- AYUDA PARA {cmd_ayuda} ---\n"
                     output += f"Descripción: {info['descripcion']}\n"
                     output += f"Sintaxis:    {info['sintaxis']}\n"
                     output += f"Ejemplo:     {info['ejemplo']}\n"
                     return f"{debug_info}{output}"
                 else:
                     return f"{debug_info}Error: Comando '{cmd_ayuda}' no encontrado en la ayuda."
        
        else:
            return "Error: Comando no reconocido o sintaxis incorrecta."

    except Exception as e:
        return f"Error de ejecución: {e}"