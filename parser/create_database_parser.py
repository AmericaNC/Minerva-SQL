# parser/create_database_parser.py

class CreateDatabaseParser:
    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self):
        if len(self.tokens) < 3:
            raise SyntaxError("Sintaxis incompleta. Se esperaba: CREAR BASE nombre;")

        if self.tokens[0][0] != "CREATE" or self.tokens[1][0] != "DATABASE":
            raise SyntaxError("Se esperaba 'CREAR BASE <nombre>';")

        db_name = self.tokens[2][1]
        return {"type": "CREATE_DATABASE", "database": db_name}
