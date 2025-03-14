import re

TOKEN_PATTERNS = [
    (r'\bSELECCIONA\b', 'SELECT'),
    (r'\bDESDE\b', 'FROM'),
    (r'\bDONDE\b', 'WHERE'),
    (r'\bINSERTAR\b', 'INSERT'),
    (r'\bINTO\b', 'INTO'),  # Asegúrate de incluir 'INTO' aquí
    (r'\bVALORES\b', 'VALUES'),  # Asegúrate de incluir 'VALUES' aquí
    (r'[a-zA-Z_][a-zA-Z0-9_]*', 'IDENTIFIER'),
    (r'\d+', 'NUMBER'),
    (r'>', 'GT'),
    (r'<', 'LT'),
    (r'=', 'EQ'),
    (r',', 'COMMA'),
    (r';', 'SEMICOLON'),
    (r'\(', 'PARIZQ'),
    (r'\)', 'PARDER'),
    (r'\s+', None)  # Espacios en blanco que se ignoran
]



def lexer(input_text):
    tokens = []
    while input_text:
        match = None
        for pattern, token_type in TOKEN_PATTERNS:
            regex = re.match(pattern, input_text)
            if regex:
                match = regex.group(0)
                if token_type:
                    tokens.append((token_type, match))
                input_text = input_text[len(match):]
                break
        if not match:
            raise SyntaxError(f"Token inesperado: {input_text[0]}")
    return tokens
