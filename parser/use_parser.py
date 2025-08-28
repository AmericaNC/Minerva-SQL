#  ___      ___   __    _____  ___    _______  
# |"  \    /"  | |" \  (\"   \|"  \  /"     "| 
#  \   \  //   | ||  | |.\\   \    |(: ______) 
#  /\\  \/.    | |:  | |: \.   \\  | \/    |   
# |: \.        | |.  | |.  \    \. | // ___)_  
# |.  \    /:  | /\  |\|    \    \ |(:      "| 
# |___|\__/|___|(__\_|_)\___|\____\) \_______)
# 
# MinervaSQL - Intérprete SQL en Español v1.0

class UseDatabaseParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        if self.tokens[self.pos][0] != 'USE':
            raise SyntaxError("Se esperaba 'USAR'")
        self.pos += 1

        if self.tokens[self.pos][0] != 'DATABASE':
            raise SyntaxError("Se esperaba 'BASE'")
        self.pos += 1

        if self.tokens[self.pos][0] != 'IDENTIFIER':
            raise SyntaxError("Se esperaba el nombre de la base de datos")

        db_name = self.tokens[self.pos][1]
        self.pos += 1

        return {"type": "USE", "database": db_name}
