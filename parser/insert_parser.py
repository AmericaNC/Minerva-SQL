#  ___      ___   __    _____  ___    _______  
# |"  \    /"  | |" \  (\"   \|"  \  /"     "| 
#  \   \  //   | ||  | |.\\   \    |(: ______) 
#  /\\  \/.    | |:  | |: \.   \\  | \/    |   
# |: \.        | |.  | |.  \    \. | // ___)_  
# |.  \    /:  | /\  |\|    \    \ |(:      "| 
# |___|\__/|___|(__\_|_)\___|\____\) \_______)
# 
# MinervaSQL - Intérprete SQL en Español v1.0

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

        # Opcional: columnas
        columns = []
        if self.tokens[self.position][0] == "PARIZQ":
            self.consume("PARIZQ")
            while self.tokens[self.position][0] == "IDENTIFIER":
                columns.append(self.consume("IDENTIFIER"))
                if self.tokens[self.position][0] == "COMMA":
                    self.consume("COMMA")
                else:
                    break
            self.consume("PARDER")

        self.consume("VALUES")
        self.consume("PARIZQ")
        values = []
        while True:
            token_type, token_value = self.tokens[self.position]

            if token_type == "NUMBER":
                values.append(int(token_value))  # Es un entero
                self.position += 1
            elif token_type == "FLOAT":
                values.append(float(token_value))  # Es un flotante
                self.position += 1
            elif token_type == "STRING":
                values.append(token_value[1:-1])  # Eliminar las comillas
                self.position += 1
            else:
                raise SyntaxError(f"Se esperaba NUMBER o STRING, pero se encontró {token_type}")
            
            if self.tokens[self.position][0] == "COMMA":
                self.consume("COMMA")
            else:
                break
        self.consume("PARDER")
        self.consume("SEMICOLON")
        
        return {"type": "INSERT", "table": table_name, "columns": columns, "values": values}
