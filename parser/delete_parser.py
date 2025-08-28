#  ___      ___   __    _____  ___    _______  
# |"  \    /"  | |" \  (\"   \|"  \  /"     "| 
#  \   \  //   | ||  | |.\\   \    |(: ______) 
#  /\\  \/.    | |:  | |: \.   \\  | \/    |   
# |: \.        | |.  | |.  \    \. | // ___)_  
# |.  \    /:  | /\  |\|    \    \ |(:      "| 
# |___|\__/|___|(__\_|_)\___|\____\) \_______)
# 
# MinervaSQL - Intérprete SQL en Español v1.0

class DeleteParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def match(self, expected_type):
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == expected_type:
            self.pos += 1
            return True
        return False

    def parse(self):
        # Aquí buscamos el token 'ELIMINAR', que es como lo traduce el lexer desde 'BORRAR'
        if not self.match("ELIMINAR"):
            raise SyntaxError("Se esperaba 'BORRAR'")
        
        if not self.match("FROM"):
            raise SyntaxError("Se esperaba 'DE'")
        
        if self.tokens[self.pos][0] != "IDENTIFIER":
            raise SyntaxError("Se esperaba el nombre de la tabla")
        
        table_name = self.tokens[self.pos][1]
        self.pos += 1

        where_clause = None
        if self.match("DONDE"):
            if self.pos + 2 >= len(self.tokens):
                raise SyntaxError("Condición WHERE incompleta")
            
            column = self.tokens[self.pos][1]
            operator = self.tokens[self.pos + 1][0]
            value = self.tokens[self.pos + 2][1]
            self.pos += 3

            # Conversión de valor a tipo adecuado
            if value.isdigit():
                value = int(value)
            elif "." in value:
                try:
                    value = float(value)
                except ValueError:
                    pass  # mantener como string si no se puede convertir

            where_clause = (column, operator, value)

        return {
            "type": "DELETE",
            "table": table_name,
            "where": where_clause
        }
