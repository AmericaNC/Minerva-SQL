class DeleteParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def match(self, expected_type):
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == expected_type:
            self.pos += 1
            return True
        return False

    def parse(self):
        if not self.match("DELETE"):
            raise SyntaxError("Se esperaba 'ELIMINAR'")
        if not self.match("FROM"):
            raise SyntaxError("Se esperaba 'DE'")
        if self.tokens[self.pos][0] != "IDENTIFIER":
            raise SyntaxError("Se esperaba el nombre de la tabla")
        
        table_name = self.tokens[self.pos][1]
        self.pos += 1

        where_clause = None
        if self.match("DONDE"):
            if self.pos + 2 >= len(self.tokens):
                raise SyntaxError("Condición WHERE incompleta")
            column = self.tokens[self.pos][1]
            operator = self.tokens[self.pos + 1][0]
            value = self.tokens[self.pos + 2][1]
            self.pos += 3
            where_clause = (column, operator, int(value) if value.isdigit() else float(value) if "." in value else value)

        return {
            "type": "DELETE",
            "table": table_name,
            "where": where_clause
        }
