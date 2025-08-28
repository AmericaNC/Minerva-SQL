#  ___      ___   __    _____  ___    _______  
# |"  \    /"  | |" \  (\"   \|"  \  /"     "| 
#  \   \  //   | ||  | |.\\   \    |(: ______) 
#  /\\  \/.    | |:  | |: \.   \\  | \/    |   
# |: \.        | |.  | |.  \    \. | // ___)_  
# |.  \    /:  | /\  |\|    \    \ |(:      "| 
# |___|\__/|___|(__\_|_)\___|\____\) \_______)
# 
# MinervaSQL - Intérprete SQL en Español v1.0

class CreateTableParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def match(self, expected_type):
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == expected_type:
            self.pos += 1
            return True
        return False

    def parse(self):
        if not self.match("CREATE"):
            raise SyntaxError("Se esperaba 'CREAR'")
        if not self.match("TABLE"):
            raise SyntaxError("Se esperaba 'TABLA'")
        if self.tokens[self.pos][0] != "IDENTIFIER":
            raise SyntaxError("Se esperaba el nombre de la tabla")

        table_name = self.tokens[self.pos][1]
        self.pos += 1

        if not self.match("PARIZQ"):
            raise SyntaxError("Se esperaba '(' después del nombre de la tabla")

        columns = []
        while self.tokens[self.pos][0] == "IDENTIFIER":
            columns.append(self.tokens[self.pos][1])
            self.pos += 1
            if not self.match("COMMA"):
                break

        if not self.match("PARDER"):
            raise SyntaxError("Se esperaba ')' al final de la definición de la tabla")

        return {"type": "CREATE", "table": table_name, "columns": columns}
