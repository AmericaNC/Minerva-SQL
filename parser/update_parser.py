#  ___      ___   __    _____  ___    _______  
# |"  \    /"  | |" \  (\"   \|"  \  /"     "| 
#  \   \  //   | ||  | |.\\   \    |(: ______) 
#  /\\  \/.    | |:  | |: \.   \\  | \/    |   
# |: \.        | |.  | |.  \    \. | // ___)_  
# |.  \    /:  | /\  |\|    \    \ |(:      "| 
# |___|\__/|___|(__\_|_)\___|\____\) \_______)
# 
# MinervaSQL - Intérprete SQL en Español v1.0

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
        self.consume("ACTUALIZAR")  # Ahora buscamos 'ACTUALIZAR'
        table_name = self.consume("IDENTIFIER")
        self.consume("SET")
        column = self.consume("IDENTIFIER")
        self.consume("EQ")

     # Aceptar NUMBER, FLOAT o STRING
        value_token = self.tokens[self.position]
        if value_token[0] == "STRING":
            value = self.consume("STRING")[1:-1]  # Eliminar comillas
        elif value_token[0] == "FLOAT":
            value = float(self.consume("FLOAT"))
        elif value_token[0] == "NUMBER":
            value = int(self.consume("NUMBER"))
        else:
            raise SyntaxError(f"Se esperaba NUMBER, FLOAT o STRING, pero se encontró {value_token[0]}")


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
        )

        return {
            "type": "UPDATE",
            "table": table_name,
            "column": column,
            "value": (
            float(value) if isinstance(value, str) and '.' in value else
            int(value) if isinstance(value, str) and value.isdigit() else
            value  # ya es un string válido como 'ADN'
            ),  # Convertir correctamente
            "where": (
                where_column,
                operator,
                float(where_value) if "." in where_value else int(where_value),
            ),
        }

