# parser/show_tables_parser.py
class ShowTablesParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        if self.tokens[self.pos][1] != "MOSTRAR":
            raise SyntaxError("Se esperaba 'MOSTRAR'")
        self.pos += 1
        if self.tokens[self.pos][1] != "TABLAS":
            raise SyntaxError("Se esperaba 'TABLAS'")
        return {"action": "show_tables"}
