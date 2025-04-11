class LoginParser:
    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self):
        if len(self.tokens) < 4:
            raise SyntaxError("Sintaxis: LOGIN nombre PARA contraseña")

        if self.tokens[0][0] != "LOGIN" or self.tokens[2][0] != "WITH":
            raise SyntaxError("Se esperaba 'LOGIN nombre CON contraseña'")

        return {"type": "LOGIN", "username": self.tokens[1][1], "password": self.tokens[3][1]}
