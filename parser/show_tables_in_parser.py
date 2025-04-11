# parser/show_tables_in_parser.py
class ShowTablesInParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        if self.tokens[self.pos][1] != "MOSTRAR":
            raise SyntaxError("Se esperaba 'MOSTRAR'")
        self.pos += 1
        if self.tokens[self.pos][1] != "TABLAS":
            raise SyntaxError("Se esperaba 'TABLAS'")
        self.pos += 1
        if self.tokens[self.pos][1] != "EN":
            raise SyntaxError("Se esperaba 'EN'")
        self.pos += 1
        if self.tokens[self.pos][0] != "IDENTIFIER":
            raise SyntaxError("Se esperaba el nombre de la base de datos")
        database_name = self.tokens[self.pos][1]
        return {"action": "show_tables_in", "database": database_name}
