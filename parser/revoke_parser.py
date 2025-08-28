class RevokeParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        self.expect("REVOKE", "REVOCAR")
        permiso = self.expect("IDENTIFIER")[1]  # ej: "crear_tabla"
        self.expect("TO", "A")
        usuario = self.expect("IDENTIFIER")[1]  # ej: "fernando"
        return {"type": "REVOKE", "permiso": permiso, "usuario": usuario}

    def expect(self, token_type, token_value=None):
        if self.position >= len(self.tokens):
            raise SyntaxError("Token inesperado al final de la instrucción.")
        current_token = self.tokens[self.position]
        if current_token[0] != token_type or (token_value and current_token[1] != token_value):
            raise SyntaxError(f"Se esperaba '{token_value}'")
        self.position += 1
        return current_token
