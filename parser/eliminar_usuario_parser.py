class EliminarUsuarioParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def parse(self):
        self._expect("ELIMINAR")
        self._expect("USER")  # <--- esto debe ser USER, no USUARIO
        nombre = self._consume("IDENTIFIER")
        return {"type": "ELIMINAR_USUARIO", "nombre": nombre}

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
