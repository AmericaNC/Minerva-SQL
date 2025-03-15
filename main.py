from lexer import lexer
from parser.select_parser import SelectParser
from parser.update_parser import UpdateParser
from parser.insert_parser import InsertParser
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
        
        # Detectar si es un SELECT o un INSERT
        if tokens[0][1] == "SELECCIONA":
            parser = SelectParser(tokens)
            parsed_query = parser.parse()
        elif tokens[0][1] == "INSERTAR":
            parser = InsertParser(tokens)
            parsed_query = parser.parse()
        elif  tokens[0][1] == "ACTUALIZAR":
            parser = UpdateParser(tokens)  # Aquí agregamos el parser para UPDATE
            parsed_query = parser.parse()
            result = executor.execute_update(parsed_query["table"], parsed_query["column"], parsed_query["value"], parsed_query["where"])
            print(result)
        else:
            raise SyntaxError("Comando no reconocido")

        result = executor.execute(parsed_query)
        print(result)
    except Exception as e:
        print("Error:", e)
