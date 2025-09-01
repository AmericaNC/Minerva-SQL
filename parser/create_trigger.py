class CreateTriggerParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        self.consume('CREAR')
        self.consume('TRIGGER')
        trigger_name = self.consume('IDENTIFIER')
        
        timing = 'DESPUES' # Asumimos DESPUES si no se especifica
        if self.tokens[self.pos][1] in ['ANTES', 'DESPUES']:
            timing = self.consume_any(['ANTES', 'DESPUES'])
        
        event = self.consume_any(['INSERTAR', 'ACTUALIZAR', 'ELIMINAR'])
        self.consume('EN')
        table_name = self.consume('IDENTIFIER')

        self.consume('SEMICOLON')

        return {
            "type": "CREATE_TRIGGER",
            "trigger_name": trigger_name,
            "timing": timing,
            "event": event,
            "table": table_name
        }
    
    def consume(self, expected_type):
        if self.pos >= len(self.tokens) or self.tokens[self.pos][0] != expected_type:
            raise SyntaxError(f"Error de sintaxis: se esperaba {expected_type}")
        value = self.tokens[self.pos][1]
        self.pos += 1
        return value

    def consume_any(self, expected_types):
        if self.pos >= len(self.tokens) or self.tokens[self.pos][0] not in expected_types:
            raise SyntaxError(f"Error de sintaxis: se esperaba uno de {expected_types}")
        value = self.tokens[self.pos][1]
        self.pos += 1
        return value