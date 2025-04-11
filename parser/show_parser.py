# parser/show_parser.py
class ShowDatabasesParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        if self.tokens[self.pos][1] != "MOSTRAR":
            raise SyntaxError("Se esperaba 'MOSTRAR'")
        self.pos += 1
        if self.tokens[self.pos][1] != "BASES":
            raise SyntaxError("Se esperaba 'BASES'")
        return {"action": "show_databases"}
