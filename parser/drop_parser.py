class DropParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def match(self, expected_type):
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == expected_type:
            self.pos += 1
            return True
        return False

    def parse(self):
        if not self.match("DROP"):
            raise SyntaxError("Se esperaba 'DESHACER'")
        if not self.match("TABLE"):
            raise SyntaxError("Se esperaba 'TABLA'")
        if self.tokens[self.pos][0] != "IDENTIFIER":
            raise SyntaxError("Se esperaba el nombre de la tabla")

        table_name = self.tokens[self.pos][1]
        self.pos += 1

        return {"type": "DROP", "table": table_name}
