# Intérprete Funcional

"""
  ___      ___   __    _____  ___    _______  
 |"  \    /"  | |" \  (\"   \|"  \  /"     "| 
  \   \  //   | ||  | |.\\   \    |(: ______) 
  /\\  \/.    | |:  | |: \.   \\  | \/    |    ╱|、
 |: \.        | |.  | |.  \    \. | // ___)_  (˚ˎ 。7 
 |.  \    /:  | /\  |\|    \    \ |(:      "| |、˜〵  
 |___|\__/|___|(__\_|_)\___|\____\) \_______) じしˍ,)ノ
 
 MinervaSQL - Intérprete SQL en Español v1.0
"""

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
BORRAR DE datos DONDE HR EQ 90;
```
```sh
DESHACER datos;
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
```sh
CREAR BASE laboratorio;
```
```sh
CREAR USUARIO fernando PARA 1234
```
```sh
LOGIN fernando PARA 1234
```
```sh
ELIMINAR USUARIO fernando
```
```sh
MOSTRAR BASES
```
```sh
MOSTRAR TABLAS
```
```sh
MOSTRAR USUARIOS
```
```sh
OTORGAR crear_tabla A fernando;
```
```sh
USUARIO_ACTUAL;
```
```sh
ELIMINAR BASE oficina;
```
```sh
BASE_ACTUAL;
```
```sh
HELP
```
```sh
MODO DEPURACION
```
## Permisos disponibles
|   Permiso           |     Descripción                          |
|---------------------|------------------------------------------|
|   eliminar_usuario  |     Eliminar un usuario del sistema      |
|   ver_bases         |     Listar todas las bases de datos      |
|   otorgar           |     Asignar permisos a usuarios          |
|   ver_tablas        |     Mostrar tablas de una base           |
|   insertar          |     Añadir nuevos registros              |
|   usar_base         |     Seleccionar una base para trabajar   |
|   ver_usuarios      |     Listar usuarios existentes           |
|   crear_base        |     Crear nuevas bases de datos          |
|   actualizar        |     Modificar registros existentes       |
|   contar            |     Obtener cantidad de registros        |
|   eliminar          |     Borrar registros                     |
|   crear_tabla       |     Crear nuevas tablas                  |
|   eliminar_tabla    |     Eliminar tablas existentes           |
## Léxico Actual

```python
TOKEN_PATTERNS = [
    (r'\bSELECCIONA\b', 'SELECCIONA'),
    #(r'\bELIMINAR\b', 'ELIMINAR'),
    (r'\bDESDE\b', 'DESDE'),
    (r'\bDONDE\b', 'DONDE'),
    (r'\bINSERTAR\b', 'INSERT'),
    (r'\bEN\b', 'INTO'),  
    (r'\bVALORES\b', 'VALUES'),  
    (r'\bUSAR\b', 'USE'),
    (r'\bBASE\b', 'DATABASE'),
    (r'\bCREAR\b', 'CREATE'),
    (r'\bBASES\b', 'DATABASES'),
    (r'\bMOSTRAR\b', 'SHOW'),
    (r'\bOTORGAR\b', 'GRANT'),
    (r'\bA\b', 'TO'),
    (r'\bMOSTRAR\b', 'MOSTRAR'),
    (r'\bTABLAS\b', 'TABLES'),
    (r'\bUSUARIO\b', 'USER'),
    (r'\bPARA\b', 'WITH'),
    (r'\bCREAR\b', 'CREATE'),
    (r'\bLOGIN\b', 'LOGIN'),
    (r'\bUSUARIO\b', 'USUARIO'),
    (r'\bUSUARIOS\b', 'USUARIOS'),
    #(r'\bDENTRO\b', 'IN'),
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
    10. Agregar CREATE DATABASE
    11. Crear usuarios
    12. Iniciar sesion como usuarios
    13. Eliminar usuario
    14. Mostrar bases
    15. Mostar tablas generalmente
    16. Mostrar usuarios
    17. Otorgar permisos a usuarios

    MODIFICAR 
    Mostrar bases (incluir lectura en tiempo real)
    Usar base (incluir lectura en tiempo real)
    Una vez insertado el primer registro, borrar el primero por default (nulo) INSERT
    ARREGLAR EL DROP QUE NO SIRVE
    