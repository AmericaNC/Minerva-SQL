class UpdateParser:
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
        #print(f"🔍 Tokens en UpdateParser: {self.tokens}")  # Para ver qué estamos recibiendo

        self.consume("ACTUALIZAR")  # Ahora buscamos 'ACTUALIZAR'
        table_name = self.consume("IDENTIFIER")
        self.consume("SET")
        column = self.consume("IDENTIFIER")
        self.consume("EQ")

        # Aceptar tanto NUMBER como FLOAT
        value_token = self.tokens[self.position]
        if value_token[0] in ["NUMBER", "FLOAT"]:
            value = self.consume(value_token[0])  # Usamos el tipo adecuado
        else:
            raise SyntaxError(
                f"Se esperaba NUMBER o FLOAT, pero se encontró {value_token[0]}"
            )

        self.consume("DONDE")
        where_column = self.consume("IDENTIFIER")
        operator = self.consume("EQ")  # Extender a "LT" o "GT" si es necesario

        # Aceptar tanto NUMBER como FLOAT para el valor en WHERE
        where_value_token = self.tokens[self.position]
        if where_value_token[0] in ["NUMBER", "FLOAT"]:
            where_value = self.consume(where_value_token[0])
        else:
            raise SyntaxError(
                f"Se esperaba NUMBER o FLOAT, pero se encontró {where_value_token[0]}"
            )

        self.consume("SEMICOLON")

        print(
            "🚀 Actualizado correctamente!"
           # f"🔍 Parsed UPDATE: table={table_name}, column={column}, value={value}, where={where_column} {operator} {where_value}"
        )

        return {
            "type": "UPDATE",
            "table": table_name,
            "column": column,
            "value": float(value) if "." in value else int(value),  # Convertir correctamente
            "where": (
                where_column,
                operator,
                float(where_value) if "." in where_value else int(where_value),
            ),
        }

