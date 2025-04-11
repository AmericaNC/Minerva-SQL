class CreateUserParser:
    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self):
        if len(self.tokens) < 5:
            raise SyntaxError("Sintaxis: CREAR USUARIO nombre CON contraseña")

        if self.tokens[0][0] != "CREATE" or self.tokens[1][0] != "USER" or self.tokens[3][0] != "WITH":
            raise SyntaxError("Se esperaba 'CREAR USUARIO nombre CON contraseña'")

        return {"type": "CREATE_USER", "username": self.tokens[2][1], "password": self.tokens[4][1]}
