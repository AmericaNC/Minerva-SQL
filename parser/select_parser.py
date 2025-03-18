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
        self.consume("SELECCIONA")  # Se espera la palabra clave SELECT
        columns = []
        
        # Leer las columnas seleccionadas
        while self.tokens[self.position][0] == "IDENTIFIER":
            columns.append(self.consume("IDENTIFIER"))
            if self.tokens[self.position][0] == "COMMA":
                self.consume("COMMA")
        
        self.consume("DESDE")  # Consumir la palabra 'DESDE'
        table_name = self.consume("IDENTIFIER")  # Obtener el nombre de la tabla

        # Verificar si hay una cláusula WHERE
        where_clause = None
        if self.position < len(self.tokens) and self.tokens[self.position][0] == "DONDE":
            self.consume("DONDE")
            where_column = self.consume("IDENTIFIER")
            operator = self.consume("EQ")  # Cambiar a ">","<" si es necesario
            where_value = self.consume("NUMBER")  # Asegúrate de que sea un número o flotante
            where_clause = (where_column, operator, where_value)

        self.consume("SEMICOLON")  # Esperar el punto y coma al final

        return {
            "type": "SELECT",
            "columns": columns,
            "table": table_name,
            "where": where_clause,
        }
