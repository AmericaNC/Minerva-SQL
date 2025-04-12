class DropParser:
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
        self.consume("DROP")
        self.consume("TABLE")
        table_name = self.consume("IDENTIFIER")
        self.consume("SEMICOLON")
        return {"type": "DROP", "table": table_name}
