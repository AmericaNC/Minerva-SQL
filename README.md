# Intérprete SQL ESPAÑOL

```
  ___      ___   __    _____  ___    _______  
 |"  \    /"  | |" \  (\"   \|"  \  /"     "| 
  \   \  //   | ||  | |.\\   \    |(: ______) 
  /\\  \/.    | |:  | |: \.   \\  | \/    |          へ♡ ╱|-`♡´-   
 |: \.        | |.  | |.  \    \. | // ___)_    ૮  >  <) (˚ˎ 。7  ִ ࣪𖤐
 |.  \    /:  | /\  |\|    \    \ |(:      "|   /  ⁻  ៸|  |、˜〵   
 |___|\__/|___|(__\_|_)\___|\____\) \_______) 乀(ˍ, ل ل  じしˍ,)ノ⁠♡
 
 MinervaSQL - Intérprete SQL en Español v1.0
```

## 🚀 Cómo Ejecutarlo
```sh
python main.py
```

## Secuencias Actuales
Éstas son las instrucciones reconocidas por el motor (ejemplos que pueden copiarse y probarse, no estrictamente la estructura lógica de las instrucciones, ésta se encuentra en HELP)

```sh
SELECCIONA HR, TEMP DESDE datos;
```
```sh
SELECCIONA * DESDE datos;
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
SALIR
```
```sh
MODO DEPURACION
```
## Permisos
```sh
OTORGAR ver_bases A fernando;
```
```sh
OTORGAR otorgar A fernando;
```
```sh
OTORGAR ver_tablas A fernando;
```
```sh
OTORGAR insertar A fernando;
```
```sh
OTORGAR usar_base A fernando;
```
```sh
OTORGAR ver_usuarios A fernando;
```
```sh
OTORGAR crear_base A fernando;
```
```sh
OTORGAR actualizar A fernando;
```
```sh
OTORGAR contar A fernando;
```
```sh
OTORGAR eliminar A fernando;
```
```sh
OTORGAR crear_tabla A fernando;
```
```sh
OTORGAR eliminar_tabla A fernando;
```
## Explicación

La siguiente tabla da una breve decripción de los permisos que se pueden asignar a los usuarios.
|   Permiso           |     Descripción                          |
|---------------------|------------------------------------------|
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
    (r'\bBORRAR\b', 'ELIMINAR'),
    (r'\bDESDE\b', 'DESDE'),
    (r'\bDONDE\b', 'DONDE'),
    (r'\bINSERTAR\b', 'INSERT'),
    (r'\bEN\b', 'INTO'),  
    (r'\bUSUARIO_ACTUAL\b', 'CURRENT_USER'),
    (r'\bBASE_ACTUAL\b', 'CURRENT_DATABASE'),
    (r'\bVALORES\b', 'VALUES'),  
    (r'\bUSAR\b', 'USE'),
    (r'\bBASE\b', 'DATABASE'),
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
    (r'\bACTUALIZAR\b', 'ACTUALIZAR'),  
    (r'\bCREAR\b', 'CREATE'),
    (r'\bCON\b', 'SET'),
    (r'\bTABLA\b', 'TABLE'),
    (r'\bDESHACER\b', 'DESHACER'),
    (r'\bELIMINAR\b', 'DELETE'),
    (r'\bDE\b', 'FROM'),
    (r'\bCONTAR\b', 'COUNT'),
    (r'\bEQ\b', '='),
    (r'[a-zA-Z_][a-zA-Z0-9_]*', 'IDENTIFIER'),
    (r'\d+\.\d+', 'FLOAT'),
    (r'\d+', 'NUMBER'),  # Asegura que los valores flotantes también se manejen
    (r"\*", "ASTERISK"),
    (r'>', 'GT'),
    (r'<', 'LT'),
    (r'=', 'EQ'),
    (r',', 'COMMA'),
    (r';', 'SEMICOLON'),
    (r'\(', 'PARIZQ'),
    (r'\)', 'PARDER'),
    (r'(".*?"|\'.*?\')', 'STRING'),
    (r'\s+', None)  # Espacios en blanco que se ignoran
]

```
## A considerar
    Interprete basado en SQL Español.
    Algunas reglas y aspectos relevantes:

        Las consultas como promedio, suma, entre otras, se realizan por edio de codigo externo.
        Los tipos de datos en insersion son de tipo FLOAT, INT y STRING.
        La eliminacion de usuarios se maneja desde el archivo de control.
        Los archivos de base de datos estan en la carpeta **database**.
        Los archivos de base de datos se generan con extensión JSON.
        El gestor tiene su propio motor de depuración.
        El usuario root no se puede borrar.
        El usuario root se carga con el primer inicio de sesion, después pueden crearse usuarios y loguearse.
        El usuario root es administrador y tiene todos los permisos disponibles.
        El ";"es opcional en la mayoria de instrucciones, solo necesario cuando hay una instruccion que tiene la ntencion de perdurar.
        El motor es sensible a mayusculas y minusculas.
        Todas las palabras reservadas se escribiran en mayusculas.
        El modo de depuración se activa y desactiva con la misma instrucción (MODO DEPURACION)
        El modo de depuración explica en texto plano el debbugin.
        No pueden revocarse permisos, seria neceario modificarlos desde JSON



    