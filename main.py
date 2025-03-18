from lexer import lexer
from parser.select_parser import SelectParser
from parser.update_parser import UpdateParser
from parser.insert_parser import InsertParser
from parser.delete_parser import DeleteParser
from parser.create_parser import CreateTableParser
from parser.drop_parser import DropParser
from executor import Executor
from database import Database

db = Database()
executor = Executor(db)

# Llenar base de datos con algunos datos iniciales
db.tables["datos"] = [
    {"HR": 90, "TEMP": 36.5},
    {"HR": 110, "TEMP": 37.2},
    {"HR": 120, "TEMP": 38.0},
]

while True:
    query = input("Consulta > ")
    if query.lower() in ["salir", "exit"]:
        break
    try:
        tokens = lexer(query)
        
        # Detectar si es un SELECT
        if tokens[0][1] == "SELECCIONA":
            parser = SelectParser(tokens)
            parsed_query = parser.parse()
            result = executor.execute(parsed_query)  # Ejecutar el SELECT
            print(f"Resultado: {result}")  # Mostrar el resultado final

        elif tokens[0][1] == "INSERTAR":
            parser = InsertParser(tokens)
            parsed_query = parser.parse()
            result = executor.execute_insert(parsed_query["table"], parsed_query["values"], parsed_query["columns"])
            print(f"Resultado: {result}")

        elif tokens[0][1] == "ACTUALIZAR":
            parser = UpdateParser(tokens)
            parsed_query = parser.parse()
            result = executor.execute_update(parsed_query["table"], parsed_query["column"], parsed_query["value"], parsed_query["where"])
            print(f"Resultado: {result}")
        
        elif tokens[0][1] == "ELIMINAR":
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

        else:
            raise SyntaxError("Comando no reconocido")

    except Exception as e:
        print("Error:", e)
