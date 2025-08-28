#  ___      ___   __    _____  ___    _______  
# |"  \    /"  | |" \  (\"   \|"  \  /"     "| 
#  \   \  //   | ||  | |.\\   \    |(: ______) 
#  /\\  \/.    | |:  | |: \.   \\  | \/    |   
# |: \.        | |.  | |.  \    \. | // ___)_  
# |.  \    /:  | /\  |\|    \    \ |(:      "| 
# |___|\__/|___|(__\_|_)\___|\____\) \_______)
# 
# MinervaSQL - Intérprete SQL en Español v1.0

class EliminarUsuarioParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def parse(self):
        if len(self.tokens) < 3:
            raise Exception("Error de sintaxis en ELIMINAR USUARIO.")
        if self.tokens[0][0] != "ELIMINAR" or self.tokens[1][0] != "USER" or self.tokens[2][0] != "IDENTIFIER":
            raise Exception("Error de sintaxis en ELIMINAR USUARIO.")
        return {"nombre": self.tokens[2][1]}


    def _expect(self, token_type):
        if self.tokens[self.index][0] != token_type:
            raise SyntaxError(f"Se esperaba '{token_type}'")
        self.index += 1

    def _consume(self, token_type):
        if self.tokens[self.index][0] != token_type:
            raise SyntaxError(f"Se esperaba un {token_type}")
        value = self.tokens[self.index][1]
        self.index += 1
        return value
