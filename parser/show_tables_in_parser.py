#  ___      ___   __    _____  ___    _______  
# |"  \    /"  | |" \  (\"   \|"  \  /"     "| 
#  \   \  //   | ||  | |.\\   \    |(: ______) 
#  /\\  \/.    | |:  | |: \.   \\  | \/    |   
# |: \.        | |.  | |.  \    \. | // ___)_  
# |.  \    /:  | /\  |\|    \    \ |(:      "| 
# |___|\__/|___|(__\_|_)\___|\____\) \_______)
# 
# MinervaSQL - Intérprete SQL en Español v1.0

class ShowTablesInParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        if self.tokens[self.pos][1] != "MOSTRAR":
            raise SyntaxError("Se esperaba 'MOSTRAR'")
        self.pos += 1
        if self.tokens[self.pos][1] != "TABLAS":
            raise SyntaxError("Se esperaba 'TABLAS'")
        self.pos += 1
        if self.tokens[self.pos][1] != "DE":
            raise SyntaxError("Se esperaba 'DE'")
        self.pos += 1
        if self.tokens[self.pos][0] != "IDENTIFIER":
            raise SyntaxError("Se esperaba el nombre de la base de datos")
        database_name = self.tokens[self.pos][1]
        return {"action": "show_tables_in", "database": database_name}
