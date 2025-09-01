#  ___      ___   __    _____  ___    _______  
# |"  \    /"  | |" \  (\"   \|"  \  /"     "| 
#  \   \  //   | ||  | |.\\   \    |(: ______) 
#  /\\  \/.    | |:  | |: \.   \\  | \/    |   
# |: \.        | |.  | |.  \    \. | // ___)_  
# |.  \    /:  | /\  |\|    \    \ |(:      "| 
# |___|\__/|___|(__\_|_)\___|\____\) \_______)
# 
# MinervaSQL - Intérprete SQL en Español v1.0

#  ___      ___   __    _____  ___    _______  
# |"  \    /"  | |" \  (\"   \|"  \  /"     "| 
#  \   \  //   | ||  | |.\\   \    |(: ______) 
#  /\\  \/.    | |:  | |: \.   \\  | \/    |   
# |: \.        | |.  | |.  \    \. | // ___)_  
# |.  \    /:  | /\  |\|    \    \ |(:      "| 
# |___|\__/|___|(__\_|_)\___|\____\) \_______)
# 
# MinervaSQL - Intérprete SQL en Español v1.0

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
        self.consume("SELECCIONA")
        columns = []
        if self.tokens[self.position][0] == "ASTERISK":
            self.consume("ASTERISK")
            columns = ["*"]
        else:
            while True:
                columns.append(self.consume("IDENTIFIER"))
                if self.position < len(self.tokens) and self.tokens[self.position][0] == "COMMA":
                    self.consume("COMMA")
                elif self.position < len(self.tokens) and self.tokens[self.position][0] == "DESDE":
                    break
                else:
                    raise SyntaxError(f"Se esperaba ',' o 'DESDE', pero se encontró {self.tokens[self.position][0]}")
        
        self.consume("DESDE")
        table_name = self.consume("IDENTIFIER")

        where_clause = None
        if self.position < len(self.tokens) and self.tokens[self.position][0] == "DONDE":
            self.consume("DONDE")
            where_column = self.consume("IDENTIFIER")
            
            # --- Corrección: Almacenar el tipo de token para el operador, no el valor ---
            operator_token_type = self.tokens[self.position][0]
            self.consume(operator_token_type) 
            
            where_value = self.consume(self.tokens[self.position][0])
            where_clause = (where_column, operator_token_type, where_value)

        order_by_clause = None
        order_direction = "ASC"  # Por defecto es ascendente
        if self.position < len(self.tokens) and self.tokens[self.position][0] == "ORDENAR":
            self.consume("ORDENAR")
            self.consume("POR")
            order_by_column = self.consume("IDENTIFIER")
            order_by_clause = order_by_column

            # Verifica si hay una dirección de orden (ASC o DESC)
            if self.position < len(self.tokens) and self.tokens[self.position][0] in ["ASC", "DESC"]:
                order_direction = self.consume(self.tokens[self.position][0])

        if self.position < len(self.tokens) and self.tokens[self.position][0] == "SEMICOLON":
            self.consume("SEMICOLON")

        return {
            "type": "SELECT",
            "columns": columns,
            "table": table_name,
            "where": where_clause,
            "order_by": order_by_clause,
            "order_direction": order_direction
        }
