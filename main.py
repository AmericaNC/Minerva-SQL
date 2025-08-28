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
from parser.transaction_parse import TransactionParser
from parser.revoke_parser import RevokeParser
import json
import sys
import os
from pathlib import Path
from colorama import init, Fore,  Style

welcome_message = f""" 

___      ___   __    _____  ___    _______   _______  ___      ___  __        ________   ______    ___       
|"  \\    /"  | |" \\  (\\"   \\|"  \\  /"     "| /"      \\|"  \\    /"  |/""\\      /"       ) /    " \\  |"  |      
 \\   \\  //   | ||  | |.\\\\   \\    |(: ______)|:        |\\   \\  //  //    \\    (:   \\___/ // ____  \\ ||  |      
 /\\\\  \\/.    | |:  | |: \\.   \\\\  | \\/    |  |_____/   ) \\\\  \\/. .//' /\\  \\    \\___  \\  /  /    )  )|:  |       ╱|-`♡´- 
|: \\.        | |.  | |.  \\    \\. | // ___)_  //      /   \\.    ////  __'  \\    __/  \\\\(: (____/ //  \\  |___   (˚ˎ 。7  ִ
|.  \\    /:  | /\\  |\\|    \\    \\ |(:      "||:  __   \\    \\\\   //   /  \\\\  \\  /" \\   :)\         \\ ( \\_|:  \\   |、˜〵   
|___|\\__/|___|(__\\_|_)\\\\___|\\____\\) \\_______)|__|  \\___)    \\__/(___/    \\___)(_______/  \\\"____/\\__\\ \\_______) じしˍ,)ノ⁠♡
{Fore.CYAN}────────────────────────────────────────────────────────────────────────────────────────────────────────────────
{Fore.WHITE}🚀 {Fore.WHITE}MinervaSQL | {Fore.WHITE}Intérprete SQL en Español {Fore.YELLOW}v3.0{Fore.WHITE} | 
{Fore.CYAN}────────────────────────────────────────────────────────────────────────────────────────────────────────────────
{Fore.WHITE}  ¡Bienvenido a MinervaSQL! Usa el comando{Fore.GREEN} HELP {Fore.WHITE}para obtener ayuda epecifica en las instrucciones y
{Fore.WHITE}  SALIR para terminar la sesion.                                                                                                      
"""
print(welcome_message)

def resource_path(relative_path):
    """ Obtiene la ruta absoluta al recurso, sin importar si se ejecuta como script o como ejecutable """
    try:
        # PyInstaller crea una carpeta temporal y guarda el path ahí
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def cargar_ayuda():
    try:
        ruta = resource_path('help_docs.json')
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{Fore.RED}Error: Archivo de ayuda no encontrado{Style.RESET_ALL}")
        return {"comandos": {}, "permisos": {}}
    except json.JSONDecodeError:
        print(f"{Fore.RED}Error: Archivo de ayuda mal formado{Style.RESET_ALL}")
        return {"comandos": {}, "permisos": {}}

help_data = cargar_ayuda()
debug_mode = False
db = Database()
usuario_actual = "root"  
usuarios = UserManager("usuarios.json")
executor = Executor(db, usuarios) 
usuarios = UserManager()

# Llenar base de datos con algunos datos iniciales
db.tables["datos"] = [
    {"HR": 90, "TEMP": 36.5},
    {"HR": 110, "TEMP": 37.2},
    {"HR": 120, "TEMP": 38.0},
]

while True:
    query = input(Fore.CYAN + "Consulta > " + Style.RESET_ALL)
    if query.lower() in ["salir", "exit"]:
        break
    if query.strip().upper() == "MODO DEPURACION":
        debug_mode = not debug_mode
        estado = "activado" if debug_mode else "desactivado"
        print(f"{Fore.YELLOW}🔍 Modo depuración {estado}{Style.RESET_ALL}")
        continue
    try:
        tokens = lexer(query)
        if debug_mode:
            print(f"\n{Fore.YELLOW}--------------------------------------------------")
            print(f"Procesando: '{query}'")
            print(f"--------------------------------------------------{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}[DEBUG LEX] Tokens generados:")
            print(json.dumps(tokens, indent=2, ensure_ascii=False))

        if tokens[0][1] == "SELECCIONA":
            parser = SelectParser(tokens)
            parsed_query = parser.parse()
            if debug_mode:
                print(f"{Fore.BLUE}[DEBUG PARSER] Árbol sintáctico:")
                print(json.dumps(parsed_query, indent=2, ensure_ascii=False))
            result = executor.execute(parsed_query)
            if debug_mode:
                print(f"{Fore.GREEN}[DEBUG EXEC] Resultado ejecución:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"Resultado: {result}")
        
        elif tokens[0][1] == "OTORGAR":
            parser = GrantParser(tokens)
            parsed_query = parser.parse()
            usuarios.otorgar_permiso(parsed_query["usuario"], parsed_query["permiso"])
            if debug_mode:
                print(f"{Fore.BLUE}[DEBUG PARSER] Árbol sintáctico:")
                print(json.dumps(parsed_query, indent=2, ensure_ascii=False))
            result = executor.execute_grant(parsed_query["permiso"], parsed_query["usuario"])
            if debug_mode:
                print(f"{Fore.GREEN}[DEBUG EXEC] Resultado ejecución:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(result)
        
        elif tokens[0][1] == "INSERTAR":
            parser = InsertParser(tokens)
            parsed_query = parser.parse()
            if debug_mode:
                print(f"{Fore.BLUE}[DEBUG PARSER] Árbol sintáctico:")
                print(json.dumps(parsed_query, indent=2, ensure_ascii=False))
            result = executor.execute_insert(parsed_query["table"], parsed_query["values"], parsed_query["columns"])
            if debug_mode:
                print(f"{Fore.GREEN}[DEBUG EXEC] Resultado ejecución:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"Resultado: {result}")
        
        elif tokens[0][0] == "USE":
            parser = UseDatabaseParser(tokens)
            parsed_query = parser.parse()
            if debug_mode:
                print(f"{Fore.BLUE}[DEBUG PARSER] Árbol sintáctico:")
                print(json.dumps(parsed_query, indent=2, ensure_ascii=False))
            result = executor.execute_use(parsed_query["database"])
            if debug_mode:
                print(f"{Fore.GREEN}[DEBUG EXEC] Resultado ejecución:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"Resultado: {result}")

        elif tokens[0][0] == "CREATE" and tokens[1][0] == "DATABASE":
            parser = CreateDatabaseParser(tokens)
            parsed_query = parser.parse()
            if debug_mode:
                print(f"{Fore.BLUE}[DEBUG PARSER] Árbol sintáctico:")
                print(json.dumps(parsed_query, indent=2, ensure_ascii=False))
            result = executor.execute_create_database(parsed_query["database"])
            if debug_mode:
                print(f"{Fore.GREEN}[DEBUG EXEC] Resultado ejecución:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"Resultado: {result}")
        
        elif tokens[0][0] == "CURRENT_USER":
            parsed_query = {"type": "CURRENT_USER"}
            if debug_mode:
                print(f"{Fore.BLUE}[DEBUG PARSER] Árbol sintáctico:")
                print(json.dumps(parsed_query, indent=2, ensure_ascii=False))
            result = executor.execute(parsed_query)
            if debug_mode:
                print(f"{Fore.GREEN}[DEBUG EXEC] Resultado ejecución:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(result)

        elif tokens[0][0] == "CURRENT_DATABASE":
            parsed_query = {"type": "CURRENT_DATABASE"}
            if debug_mode:
                print(f"{Fore.BLUE}[DEBUG PARSER] Árbol sintáctico:")
                print(json.dumps(parsed_query, indent=2, ensure_ascii=False))
            result = executor.execute(parsed_query)
            if debug_mode:
                print(f"{Fore.GREEN}[DEBUG EXEC] Resultado ejecución:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(result)

        elif tokens[0][0] == "CREATE" and tokens[1][0] == "USER":
            parser = CreateUserParser(tokens)
            parsed_query = parser.parse()
            usuarios.agregar_usuario(parsed_query["username"], parsed_query["password"])
            if debug_mode:
                print(f"{Fore.BLUE}[DEBUG PARSER] Árbol sintáctico:")
                print(json.dumps(parsed_query, indent=2, ensure_ascii=False))
            result = executor.execute_create_user(parsed_query["username"], parsed_query["password"])
            if debug_mode:
                print(f"{Fore.GREEN}[DEBUG EXEC] Resultado ejecución:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"Resultado: {result}")
  
       


        elif tokens[0][0] == "ELIMINAR" and tokens[1][0] == "USER":
            parser = EliminarUsuarioParser(tokens)
            parsed_query = parser.parse()
            if debug_mode:
                print(f"{Fore.BLUE}[DEBUG PARSER] Árbol sintáctico:")
                print(json.dumps(parsed_query, indent=2, ensure_ascii=False))
            result = executor.execute_eliminar_usuario(parsed_query["nombre"], usuario_actual)
            if debug_mode:
                print(f"{Fore.GREEN}[DEBUG EXEC] Resultado ejecución:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"Resultado: {result}")
        
      



        elif tokens[0][0] == "DROP" and tokens[1][0] == "USER":
            parser = DropUserParser(tokens)
            parsed_query = parser.parse()
            if debug_mode:
                print(f"{Fore.BLUE}[DEBUG PARSER] Árbol sintáctico:")
                print(json.dumps(parsed_query, indent=2, ensure_ascii=False))
            result = executor.execute_drop_user(parsed_query["username"])
            if debug_mode:
                print(f"{Fore.GREEN}[DEBUG EXEC] Resultado ejecución:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"Resultado: {result}")
                print(result)


        elif tokens[0][0] == "LOGIN":
            parser = LoginParser(tokens)
            parsed_query = parser.parse()
            if debug_mode:
                print(f"{Fore.BLUE}[DEBUG PARSER] Árbol sintáctico:")
                print(json.dumps(parsed_query, indent=2, ensure_ascii=False))
            result = executor.execute_login(parsed_query["username"], parsed_query["password"])
            if debug_mode:
                print(f"{Fore.GREEN}[DEBUG EXEC] Resultado ejecución:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"Resultado: {result}")
 

        elif tokens[0][1] == "MOSTRAR" and tokens[1][1] == "BASES":
            result = executor.execute_show_databases()
            from parser.show_parser import ShowDatabasesParser
            parser = ShowDatabasesParser(tokens)
            parsed_query = parser.parse()
            if debug_mode:
                print(f"{Fore.BLUE}[DEBUG PARSER] Árbol sintáctico:")
                print(json.dumps(parsed_query, indent=2, ensure_ascii=False))
            result = executor.execute_show_databases()
            if debug_mode:
                print(f"{Fore.GREEN}[DEBUG EXEC] Resultado ejecución:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print("Bases de datos disponibles:")
                print("\n".join(f"  • {db}" for db in result))

        elif tokens[0][1] == "MOSTRAR" and tokens[1][1] == "TABLAS":
           from parser.show_tables_parser import ShowTablesParser
           parser = ShowTablesParser(tokens)
           parsed_query = parser.parse()
           if debug_mode:
                print(f"{Fore.BLUE}[DEBUG PARSER] Árbol sintáctico:")
                print(json.dumps(parsed_query, indent=2, ensure_ascii=False))
           result = executor.execute_show_tables()
           if result:
            print("Tablas:")
            for i, item in enumerate(result, 1):
                print(f"{i}. {item}")
           else:
            print("No hay tablas en la base de datos actual.")
            if debug_mode:
                print(f"{Fore.GREEN}[DEBUG EXEC] Resultado ejecución:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"Resultado: {result}")

        elif tokens[0][1] == "MOSTRAR" and tokens[1][1] == "TABLAS" and tokens[2][1] == "EN":
           from parser.show_tables_in_parser import ShowTablesInParser
           parser = ShowTablesInParser(tokens)
           parsed_query = parser.parse()
           if debug_mode:
                print(f"{Fore.BLUE}[DEBUG PARSER] Árbol sintáctico:")
                print(json.dumps(parsed_query, indent=2, ensure_ascii=False))

           result = executor.execute_show_tables_in(parsed_query["database"])
           if result:
            print(f"Tablas en '{parsed_query['database']}':", ", ".join(result))
           else:
            print(f"No hay tablas en '{parsed_query['database']}'")
            if debug_mode:
                print(f"{Fore.GREEN}[DEBUG EXEC] Resultado ejecución:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"Resultado: {result}")

        elif tokens[0][1] == "MOSTRAR" and tokens[1][1] == "USUARIOS":
            from parser.show_users_parser import ShowUsersParser
            parser = ShowUsersParser(tokens)
            parsed_query = parser.parse()
            if debug_mode:
                print(f"{Fore.BLUE}[DEBUG PARSER] Árbol sintáctico:")
                print(json.dumps(parsed_query, indent=2, ensure_ascii=False))
            result = executor.execute_show_users()
            if debug_mode:
                print(f"{Fore.GREEN}[DEBUG EXEC] Resultado ejecución:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(result)

        elif tokens[0][1] == "ACTUALIZAR":
            parser = UpdateParser(tokens)
            parsed_query = parser.parse()
            if debug_mode:
                print(f"{Fore.BLUE}[DEBUG PARSER] Árbol sintáctico:")
                print(json.dumps(parsed_query, indent=2, ensure_ascii=False))
            result = executor.execute_update(parsed_query["table"], parsed_query["column"], parsed_query["value"], parsed_query["where"])
            if debug_mode:
                print(f"{Fore.GREEN}[DEBUG EXEC] Resultado ejecución:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"Resultado: {result}")

        
        elif tokens[0][1] == "BORRAR":
            if len(tokens) > 1 and tokens[1][0] == "USER":  # <--- esto es clave
                from parser.eliminar_usuario_parser import EliminarUsuarioParser
                parser = EliminarUsuarioParser(tokens)
                parsed_query = parser.parse()
                if debug_mode:
                    print(f"{Fore.BLUE}[DEBUG PARSER] Árbol sintáctico:")
                    print(json.dumps(parsed_query, indent=2, ensure_ascii=False))
                result = executor.execute_eliminar_usuario(parsed_query["nombre"])
                if debug_mode:
                    print(f"{Fore.GREEN}[DEBUG EXEC] Resultado ejecución:")
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                else:
                    print(f"Resultado: {result}")
                print(result)
            else:
                parser = DeleteParser(tokens)
                parsed_query = parser.parse()
                if debug_mode:
                    print(f"{Fore.BLUE}[DEBUG PARSER] Árbol sintáctico:")
                    print(json.dumps(parsed_query, indent=2, ensure_ascii=False))
                result = executor.execute_delete(parsed_query["table"], parsed_query["where"])
                if debug_mode:
                    print(f"{Fore.GREEN}[DEBUG EXEC] Resultado ejecución:")
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                else:
                    print(f"Resultado: {result}")
   
        elif tokens[0][1] == "DESHACER":
            from parser.drop_parser import DropParser  # o como lo estés organizando
            parser = DropParser(tokens)
            parsed_query = parser.parse()
            result = executor.execute_drop_table(parsed_query["table"])
            if debug_mode:
                print(f"{Fore.GREEN}[DEBUG EXEC] Resultado ejecución:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"Resultado: {result}")


        elif tokens[0][1] == "CREAR":
            parser = CreateTableParser(tokens)
            parsed_query = parser.parse()
            if debug_mode:
                print(f"{Fore.BLUE}[DEBUG PARSER] Árbol sintáctico:")
                print(json.dumps(parsed_query, indent=2, ensure_ascii=False))
            result = executor.execute_create(parsed_query["table"], parsed_query["columns"])
            print(f"Resultado: {result}")

        elif tokens[0][1] == "CONTAR":
            parser = CountParser(tokens)
            parsed_query = parser.parse()
            if debug_mode:
                print(f"{Fore.BLUE}[DEBUG PARSER] Árbol sintáctico:")
                print(json.dumps(parsed_query, indent=2, ensure_ascii=False))
            result = executor.execute_count(parsed_query["table"], parsed_query["where"])
            print(f"Resultado: {result}")
        
        elif tokens[0][1] == "REVOCAR":
            parser = RevokeParser(tokens)
            parsed_query = parser.parse()
            result = executor.execute_revoke(parsed_query["permiso"], parsed_query["usuario"])
            if debug_mode:
                print(f"{Fore.BLUE}[DEBUG PARSER] Árbol sintáctico:")
                print(json.dumps(parsed_query, indent=2, ensure_ascii=False))
                print(f"{Fore.GREEN}[DEBUG EXEC] Resultado ejecución:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(result)

        elif tokens[0][1] in ["BEGIN", "COMMIT", "ROLLBACK"]:
            parser = TransactionParser(tokens)
            parsed_query = parser.parse()
            if parsed_query["type"] == "BEGIN":
                result = executor.begin()
            elif parsed_query["type"] == "COMMIT":
                result = executor.commit()
            elif parsed_query["type"] == "ROLLBACK":
                result = executor.rollback()
            print(result)

        elif tokens[0][1] == "HELP":
            if len(tokens) == 1:
        # Mostrar lista de comandos disponibles
                print(f"\n{Fore.YELLOW}Comandos disponibles:{Style.RESET_ALL}")
                for cmd in help_data["comandos"]:
                    print(f"  {Fore.CYAN}{cmd.ljust(12)}{Style.RESET_ALL} - {help_data['comandos'][cmd]['descripcion']}")
                    # Nueva línea para mostrar permisos
                print(f"\n{Fore.YELLOW}Permisos disponibles:{Style.RESET_ALL}")
                for permiso, desc in help_data["permisos"].items():
                    print(f"  {Fore.MAGENTA}{permiso.ljust(12)}{Style.RESET_ALL} - {desc}")
        
                print(f"\n  Usa el comando {Fore.CYAN}MODO DEPURACION {Style.RESET_ALL} para depurar paso por paso cada instrucción. Consulta su funcionamiento con HELP MODO_DEPURACION\n")
                print(f"\n  Usa {Fore.GREEN}HELP [comando]{Style.RESET_ALL} para detalles específicos.\n")
            else:
                
        # Mostrar ayuda específica
                cmd = tokens[1][1]
                if cmd in help_data["comandos"]:
                    info = help_data["comandos"][cmd]
                    print(f"\n{Fore.YELLOW}AYUDA PARA {cmd}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}Descripción:{Style.RESET_ALL} {info['descripcion']}")
                    print(f"{Fore.CYAN}Sintaxis:{Style.RESET_ALL}    {info['sintaxis']}")
                    print(f"{Fore.CYAN}Ejemplo:{Style.RESET_ALL}     {info['ejemplo']}\n")

                elif cmd == "PERMISOS":
                    print(f"\n{Fore.YELLOW}PERMISOS DISPONIBLES:{Style.RESET_ALL}")
                    for permiso, desc in help_data["permisos"].items():
                        print(f"  {Fore.MAGENTA}{permiso.ljust(15)}{Style.RESET_ALL} - {desc}")
                    print()
                else:
                    print(f"{Fore.RED}Error: Comando '{cmd}' no reconocido{Style.RESET_ALL}")

        elif tokens[0][0] == "DELETE" and tokens[1][0] == "DATABASE":
            from parser.drop_database_parser import DropDatabaseParser
            parser = DropDatabaseParser(tokens)
            parsed_query = parser.parse()
            result = executor.execute_drop_database(parsed_query["name"])
            if debug_mode:
                print(f"{Fore.GREEN}[DEBUG EXEC] Resultado ejecución:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"Resultado: {result}")

        else:
            raise SyntaxError("Comando no reconocido")

    except Exception as e:
        print("Error:", e)
