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
from parser.drop_parser import DropParser
from executor import Executor
from database import Database
from colorama import init, Fore,  Style

welcome_message = f"""

 ___      ___   __    _____  ___    _______   _______  ___      ___  __        ________   ______    ___       
|"  \    /"  | |" \  (\"   \|"  \  /"     "| /"      \|"  \    /"  |/""\      /"       ) /    " \  |"  |      
 \   \  //   | ||  | |.\\   \    |(: ______)|:        |\   \  //  //    \    (:   \___/ // ____  \ ||  |      
 /\\  \/.    | |:  | |: \.   \\  | \/    |  |_____/   ) \\  \/. .//' /\  \    \___  \  /  /    )  )|:  |       ╱|、
|: \.        | |.  | |.  \    \. | // ___)_  //      /   \.    ////  __'  \    __/  \\(: (____/ //  \  |___ (˚. 。7 
|.  \    /:  | /\  |\|    \    \ |(:      "||:  __   \    \\   //   /  \\  \  /" \   :)\         \ ( \_|:  \ |、˜〵  
|___|\__/|___|(__\_|_)\___|\____\) \_______)|__|  \___)    \__/(___/    \___)(_______/  \"____/\__\ \_______)じしˍ,)ノ     

{Fore.CYAN}────────────────────────────────────────────────────────────────────────────────────────────────────────────────
{Fore.WHITE}🚀 {Fore.WHITE}MinervaSQL | {Fore.WHITE}Intérprete SQL en Español {Fore.YELLOW}v1.0{Fore.WHITE} | 
{Fore.CYAN}────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 
{Fore.WHITE}                                                                                                         
"""
print(welcome_message)

db = Database()
executor = Executor(db)

# Llenar base de datos con algunos datos iniciales
db.tables["datos"] = [
    {"HR": 90, "TEMP": 36.5},
    {"HR": 110, "TEMP": 37.2},
    {"HR": 120, "TEMP": 38.0},
]

while True:
    query = input(Fore.BLUE + "Consulta > " + Style.RESET_ALL)
    if query.lower() in ["salir", "exit"]:
        break
    try:
        tokens = lexer(query)
        #print("Tokens:", tokens)        
        # Detectar si es un SELECT
        if tokens[0][1] == "SELECCIONA":
            parser = SelectParser(tokens)
            parsed_query = parser.parse()
            result = executor.execute(parsed_query)  # Ejecutar el SELECT
            print(f"Resultado: {result}")  # Mostrar el resultado final
        
        elif tokens[0][1] == "OTORGAR":
            parser = GrantParser(tokens)
            parsed_query = parser.parse()
            result = executor.execute_grant(parsed_query["permiso"], parsed_query["usuario"])
            print(result)
        

        elif tokens[0][1] == "INSERTAR":
            parser = InsertParser(tokens)
            parsed_query = parser.parse()
            result = executor.execute_insert(parsed_query["table"], parsed_query["values"], parsed_query["columns"])
            print(f"Resultado: {result}")
        
        elif tokens[0][0] == "USE":
            parser = UseDatabaseParser(tokens)
            parsed_query = parser.parse()
            result = executor.execute_use(parsed_query["database"])
            print(result)

        elif tokens[0][0] == "CREATE" and tokens[1][0] == "DATABASE":
            parser = CreateDatabaseParser(tokens)
            parsed_query = parser.parse()
            result = executor.execute_create_database(parsed_query["database"])
            print(result)
        
        elif tokens[0][0] == "CURRENT_USER":
            parsed_query = {"type": "CURRENT_USER"}
            result = executor.execute(parsed_query)
            print(result)

        elif tokens[0][0] == "CURRENT_DATABASE":
            parsed_query = {"type": "CURRENT_DATABASE"}
            result = executor.execute(parsed_query)
            print(result)

        elif tokens[0][0] == "CREATE" and tokens[1][0] == "USER":
            parser = CreateUserParser(tokens)
            parsed_query = parser.parse()
            result = executor.execute_create_user(parsed_query["username"], parsed_query["password"])
            print(result)

        elif tokens[0][0] == "ELIMINAR" and tokens[1][0] == "USUARIO":
            parser = EliminarUsuarioParser(tokens)
            parsed_query = parser.parse()
            result = executor.execute_eliminar_usuario(parsed_query["nombre"])
            print(result)


        elif tokens[0][0] == "DROP" and tokens[1][0] == "USER":
            parser = DropUserParser(tokens)
            parsed_query = parser.parse()
            result = executor.execute_drop_user(parsed_query["username"])
            print(result)


        elif tokens[0][0] == "LOGIN":
            parser = LoginParser(tokens)
            parsed_query = parser.parse()
            result = executor.execute_login(parsed_query["username"], parsed_query["password"])
            print(result)

        elif tokens[0][1] == "MOSTRAR" and tokens[1][1] == "BASES":
            from parser.show_parser import ShowDatabasesParser
            parser = ShowDatabasesParser(tokens)
            parsed_query = parser.parse()
            result = executor.execute_show_databases()
            print("Bases de datos disponibles:", ", ".join(result))

        elif tokens[0][1] == "MOSTRAR" and tokens[1][1] == "TABLAS":
           from parser.show_tables_parser import ShowTablesParser
           parser = ShowTablesParser(tokens)
           parsed_query = parser.parse()
           result = executor.execute_show_tables()
           if result:
            print("Tablas disponibles:", ", ".join(result))
           else:
            print("No hay tablas en la base de datos actual.")

        elif tokens[0][1] == "MOSTRAR" and tokens[1][1] == "TABLAS" and tokens[2][1] == "EN":
           from parser.show_tables_in_parser import ShowTablesInParser
           parser = ShowTablesInParser(tokens)
           parsed_query = parser.parse()
           result = executor.execute_show_tables_in(parsed_query["database"])
           if result:
            print(f"Tablas en '{parsed_query['database']}':", ", ".join(result))
           else:
            print(f"No hay tablas en '{parsed_query['database']}'")
        
        elif tokens[0][1] == "MOSTRAR" and tokens[1][1] == "USUARIOS":
            from parser.show_users_parser import ShowUsersParser
            parser = ShowUsersParser(tokens)
            parsed_query = parser.parse()
            result = executor.execute_show_users()
            print(result)

        elif tokens[0][1] == "ACTUALIZAR":
            parser = UpdateParser(tokens)
            parsed_query = parser.parse()
            result = executor.execute_update(parsed_query["table"], parsed_query["column"], parsed_query["value"], parsed_query["where"])
            print(f"Resultado: {result}")
        
        elif tokens[0][1] == "ELIMINAR":
            if len(tokens) > 1 and tokens[1][0] == "USER":  # <--- esto es clave
                from parser.eliminar_usuario_parser import EliminarUsuarioParser
                parser = EliminarUsuarioParser(tokens)
                parsed_query = parser.parse()
                result = executor.execute_eliminar_usuario(parsed_query["nombre"])
                print(result)
            else:
                parser = DeleteParser(tokens)
                parsed_query = parser.parse()
                result = executor.execute_delete(parsed_query["table"], parsed_query["where"])
            print(f"Resultado: {result}")

        
        elif tokens[0][1] == "DESHACER":
            parser = DropParser(tokens)
            parsed_query = parser.parse()
            result = executor.execute_drop(parsed_query["table"])
            print(f"Resultado: {result}")
        
        elif tokens[0][1] == "CREAR":
            parser = CreateTableParser(tokens)
            parsed_query = parser.parse()
            result = executor.execute_create(parsed_query["table"], parsed_query["columns"])
            print(f"Resultado: {result}")

        elif tokens[0][1] == "CONTAR":
            parser = CountParser(tokens)
            parsed_query = parser.parse()
            result = executor.execute_count(parsed_query["table"], parsed_query["where"])
            print(f"Resultado: {result}")

        else:
            raise SyntaxError("Comando no reconocido")

    except Exception as e:
        print("Error:", e)
