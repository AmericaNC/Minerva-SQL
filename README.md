# Intérprete Funcional

### Tareas Pendientes:
1. Guardar los datos en un `data.json`.
2. Agregar más símbolos al alfabeto.
3. Agregar la interfaz gráfica.

## 🚀 Cómo Ejecutarlo
```sh
python main.py
```

## Secuencias Actuales

```sh
SELECCIONA HR, TEMP DESDE datos DONDE HR > 100;
```

```sh
INSERTAR EN datos VALORES (130, 39);
```
```sh
ACTUALIZAR datos CON HR = 95 DONDE TEMP = 36.5;
```

## Léxico Actual

```python
TOKEN_PATTERNS = [
    (r'\bSELECCIONA\b', 'SELECT'),
    (r'\bDESDE\b', 'FROM'),
    (r'\bDONDE\b', 'WHERE'),
    (r'\bINSERTAR\b', 'INSERT'),
    (r'\bEN\b', 'INTO'),
    (r'\bVALORES\b', 'VALUES'),
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
```
## Cambios
    1. Traducir INTO a EN
    2. Agregar UPDATE
    3. Agregar SELECT (sencillo)
    4. Agregar INSERT 
