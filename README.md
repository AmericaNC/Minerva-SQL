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
SELECCIONA HR, TEMP DESDE datos;
```
```sh
INSERTAR EN datos VALORES (130, 39);
```
```sh
INSERTAR EN datos (HR, TEMP) VALORES (100, 37.1);
```
```sh
ACTUALIZAR datos CON HR = 95 DONDE TEMP = 36.5;
```
```sh
ELIMINAR DE datos DONDE HR EQ 90;
```
```sh
DESHACER TABLA datos;
```
```sh
CONTAR DESDE datos;
```
```sh
CREAR TABLA pacientes (ID, NOMBRE, EDAD);
```
```sh
USAR BASE datos;
```
## Léxico Actual

```python
TOKEN_PATTERNS = [
    (r'\bSELECCIONA\b', 'SELECCIONA'),
    (r'\bDESDE\b', 'DESDE'),
    (r'\bDONDE\b', 'DONDE'),
    (r'\bINSERTAR\b', 'INSERT'),
    (r'\bEN\b', 'INTO'),  
    (r'\bVALORES\b', 'VALUES'),  
    (r'\bUSAR\b', 'USE'),
    (r'\bBASE\b', 'DATABASE'),
    (r'\bACTUALIZAR\b', 'ACTUALIZAR'),  
    (r'\bCREAR\b', 'CREATE'),
    (r'\bCON\b', 'SET'),
    (r'\bTABLA\b', 'TABLE'),
    (r'\bDESHACER\b', 'DROP'),
    (r'\bELIMINAR\b', 'DELETE'),
    (r'\bDE\b', 'FROM'),
    (r'\bCONTAR\b', 'COUNT'),
    (r'\bEQ\b', '='),
    (r'[a-zA-Z_][a-zA-Z0-9_]*', 'IDENTIFIER'),
    (r'\d+\.\d+', 'FLOAT'),
    (r'\d+', 'NUMBER'),  # Asegura que los valores flotantes también se manejen
    (r'>', 'GT'),
    (r'<', 'LT'),
    (r'=', 'EQ'),
    (r',', 'COMMA'),
    (r';', 'SEMICOLON'),
    (r'\(', 'PARIZQ'),
    (r'\)', 'PARDER'),
    (r'\'[^\']*\'', 'STRING'), 
    (r'\s+', None)  # Espacios en blanco que se ignoran
]

```
## Cambios
    1. Traducir INTO a EN
    2. Agregar UPDATE
    3. Agregar SELECT (sencillo)
    4. Agregar INSERT 
    5. Sofisticar INSERT 
    6. Agregar CREATE
    
    5. Agregar DELETE (con condicion)
    6. Agregar DROP 
    7. Agregar CREATE
    8. Agregar COUNT simple
    9. Agregar USE database
