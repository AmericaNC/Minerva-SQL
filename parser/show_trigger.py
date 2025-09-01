class ShowTriggersParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        if self.tokens[self.pos][1] != "MOSTRAR":
            raise SyntaxError("Se esperaba 'MOSTRAR'")
        self.pos += 1
        if self.tokens[self.pos][1] != "TRIGGERS":
            raise SyntaxError("Se esperaba 'TRIGGERS'")
        self.pos += 1

        table_name = None
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == "DE":
            self.pos += 1
            table_name = self.tokens[self.pos][1]
            self.pos += 1

        self.consume("SEMICOLON")
        return {"type": "SHOW_TRIGGERS", "table": table_name}

    def consume(self, expected_type):
        if self.tokens[self.pos][0] != expected_type:
            raise SyntaxError(f"Se esperaba {expected_type}")
        self.pos += 1
