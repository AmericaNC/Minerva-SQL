class TransactionParser:
    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self):
        token = self.tokens[0][1]
        if token == "BEGIN":
            return {"type": "BEGIN"}
        elif token == "COMMIT":
            return {"type": "COMMIT"}
        elif token == "ROLLBACK":
            return {"type": "ROLLBACK"}
        else:
            raise SyntaxError("Transacción no reconocida.")
