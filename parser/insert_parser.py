class InsertParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def consume(self, expected_type):
        token_type, token_value = self.tokens[self.position]
        if token_type == expected_type:
            self.position += 1
            return token_value
        else:
            raise SyntaxError(f"Se esperaba {expected_type}, pero se encontró {token_type}")

    def parse(self):
        self.consume("INSERT")
        self.consume("INTO")
        table_name = self.consume("IDENTIFIER")
        self.consume("VALUES")
        self.consume("PARIZQ")
        values = []
        while True:
            values.append(self.consume("NUMBER"))
            if self.tokens[self.position][0] == "COMMA":
                self.consume("COMMA")
            else:
                break
        self.consume("PARDER")
        self.consume("SEMICOLON")
        return {"type": "INSERT", "table": table_name, "values": values}
