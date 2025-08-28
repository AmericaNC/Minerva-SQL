#  ___      ___   __    _____  ___    _______  
# |"  \    /"  | |" \  (\"   \|"  \  /"     "| 
#  \   \  //   | ||  | |.\\   \    |(: ______) 
#  /\\  \/.    | |:  | |: \.   \\  | \/    |   
# |: \.        | |.  | |.  \    \. | // ___)_  
# |.  \    /:  | /\  |\|    \    \ |(:      "| 
# |___|\__/|___|(__\_|_)\___|\____\) \_______)
# 
# MinervaSQL - Intérprete SQL en Español v1.0

class GrantParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        self.expect("GRANT", "OTORGAR")
        permiso = self.expect("IDENTIFIER")[1]  # el permiso, ej: "crear_tabla"
        self.expect("TO", "A")
        usuario = self.expect("IDENTIFIER")[1]  # el usuario, ej: "fernando"
        return {"type": "GRANT", "permiso": permiso, "usuario": usuario}

    def expect(self, token_type, token_value=None):
        if self.position >= len(self.tokens):
            raise SyntaxError("Token inesperado al final de la instrucción.")
        current_token = self.tokens[self.position]
        if current_token[0] != token_type or (token_value and current_token[1] != token_value):
            raise SyntaxError(f"Se esperaba '{token_value}'")
        self.position += 1
        return current_token
