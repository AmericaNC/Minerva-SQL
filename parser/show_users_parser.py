#  ___      ___   __    _____  ___    _______  
# |"  \    /"  | |" \  (\"   \|"  \  /"     "| 
#  \   \  //   | ||  | |.\\   \    |(: ______) 
#  /\\  \/.    | |:  | |: \.   \\  | \/    |   
# |: \.        | |.  | |.  \    \. | // ___)_  
# |.  \    /:  | /\  |\|    \    \ |(:      "| 
# |___|\__/|___|(__\_|_)\___|\____\) \_______)
# 
# MinervaSQL - Intérprete SQL en Español v1.0

class ShowUsersParser:
    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self):
        if len(self.tokens) != 3 or self.tokens[0][1] != "MOSTRAR" or self.tokens[1][1] != "USUARIOS" or self.tokens[2][0] != "SEMICOLON":
            raise SyntaxError("Sintaxis esperada: MOSTRAR USUARIOS;")
        return {"type": "SHOW_USERS"}
