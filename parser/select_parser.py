class SelectParser:
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
        self.consume("SELECT")
        columns = []
        while True:
            columns.append(self.consume("IDENTIFIER"))
            if self.tokens[self.position][0] == "COMMA":
                self.consume("COMMA")
            else:
                break
        self.consume("FROM")
        table_name = self.consume("IDENTIFIER")
        where_clause = None
        if self.tokens[self.position][0] == "WHERE":
            self.consume("WHERE")
            column = self.consume("IDENTIFIER")
            operator = self.consume(self.tokens[self.position][0])
            value = self.consume("NUMBER")
            where_clause = (column, operator, value)
        self.consume("SEMICOLON")
        return {"type": "SELECT", "columns": columns, "table": table_name, "where": where_clause}
