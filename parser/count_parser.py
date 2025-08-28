#  ___      ___   __    _____  ___    _______  
# |"  \    /"  | |" \  (\"   \|"  \  /"     "| 
#  \   \  //   | ||  | |.\\   \    |(: ______) 
#  /\\  \/.    | |:  | |: \.   \\  | \/    |   
# |: \.        | |.  | |.  \    \. | // ___)_  
# |.  \    /:  | /\  |\|    \    \ |(:      "| 
# |___|\__/|___|(__\_|_)\___|\____\) \_______)
# 
# MinervaSQL - Intérprete SQL en Español v1.0

class CountParser:
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
        self.consume("COUNT")
        self.consume("DESDE")
        table_name = self.consume("IDENTIFIER")

        # Opcional: cláusula WHERE
        where_clause = None
        if self.tokens[self.position][0] == "DONDE":
            self.consume("DONDE")
            column = self.consume("IDENTIFIER")
            operator = self.consume("EQ")
            value = self.consume("NUMBER")  # Puedes ajustar esto para que acepte STRING o FLOAT si es necesario
            where_clause = (column, operator, value)

        self.consume("SEMICOLON")

        return {"type": "COUNT", "table": table_name, "where": where_clause}
