#  ___      ___   __    _____  ___    _______  
# |"  \    /"  | |" \  (\"   \|"  \  /"     "| 
#  \   \  //   | ||  | |.\\   \    |(: ______) 
#  /\\  \/.    | |:  | |: \.   \\  | \/    |   
# |: \.        | |.  | |.  \    \. | // ___)_  
# |.  \    /:  | /\  |\|    \    \ |(:      "| 
# |___|\__/|___|(__\_|_)\___|\____\) \_______)
# 
# MinervaSQL - Intérprete SQL en Español v1.0

from pathlib import Path
import os
import json

def check_condition(row, condition):
        columna, operador, valor = condition
        if operador == "=":
            return row.get(columna) == valor
        elif operador == "!=":
            return row.get(columna) != valor
        elif operador == ">":
            return row.get(columna) > valor
        elif operador == "<":
            return row.get(columna) < valor
        elif operador == ">=":
            return row.get(columna) >= valor
        elif operador == "<=":
            return row.get(columna) <= valor
        else:
            raise ValueError(f"Operador no soportado: {operador}")


class Database:
    def __init__(self):
        self.databases_path = Path("databases")
        self.databases_dir = "databases"
        self.triggers = {} 
        self.triggers_file_path = Path("databases/triggers.json")
        self.load_triggers()
        self.databases_path.mkdir(exist_ok=True)
        self.databases = {"default": {}}
        self.current_db = "default"
        #self.users = {"root": "rootpass"}
        self.current_user = "root"  # ← login automático
        self.load_all_databases()
        # Si no hay bases, creamos 'default'
        if "default" not in self.databases:
            self.create_database("default")
        self.set_current_database("default") 

    #@property
    def tables(self):
        return self.databases[self.current_db]
    
    def ensure_default_database(self):
        """Asegura que exista la carpeta de bases y la base 'default' al inicio."""
        if not os.path.exists(self.databases_dir):
            os.makedirs(self.databases_dir)
        default_path = os.path.join(self.databases_dir, "default")
        if not os.path.exists(default_path):
            os.makedirs(default_path)
    
    




    def load_triggers(self):
        """Carga los triggers desde el archivo JSON al iniciar el programa."""
        if self.triggers_file_path.exists():
            with open(self.triggers_file_path, "r") as f:
                try:
                    # Cargar los triggers del archivo. Por ahora, solo los nombres.
                    # La lógica de las funciones se define al cargarlas.
                    self.triggers = json.load(f)
                    print(f"Triggers cargados desde {self.triggers_file_path}")
                except (json.JSONDecodeError, FileNotFoundError):
                    print("Error al cargar triggers o archivo no encontrado. Creando uno nuevo.")
                    self.triggers = {}
        else:
            self.save_triggers()  # Crea el archivo si no existe

    def save_triggers(self):
        """Guarda los triggers en un archivo JSON."""
        # Se guarda el diccionario de triggers en el archivo
        with open(self.triggers_file_path, "w") as f:
            # Serializamos el diccionario para guardarlo como JSON
            json.dump(self.triggers, f, indent=4)
            print(f"Triggers guardados en {self.triggers_file_path}")

    def add_trigger(self, table, event, function_name):
        """Añade un trigger y lo guarda en el archivo."""
        if table not in self.triggers:
            self.triggers[table] = {}
        self.triggers[table][event] = function_name
        self.save_triggers() # Guarda el estado después de añadir un trigger

    # ... tu método run_triggers() necesita ser actualizado
    # para usar el nombre de la función y no la función en sí
    def run_triggers(self, table, event, row):
        function_name = self.triggers.get(table, {}).get(event)
        if function_name:
            # Aquí necesitarás un mapeo de nombres a funciones
            # para invocar la función correcta.
            # Ejemplo simple:
            if function_name == "user_login_message":
                user_login_message(row) 





    def run_triggers(self, table_name, event):
    # Obtener el trigger para la tabla y el evento.
    # Por ahora, solo tenemos uno fijo.
        trigger_func = self.triggers.get(table_name, {}).get(event)
    
        if trigger_func:
        # Aquí, podrías pasar la fila de datos si estuvieras
        # manejando la lógica de la operación (ej. INSERT, UPDATE).
        # Por ahora, solo ejecutamos la función.
            trigger_func()

    def list_databases(self):
        """Lista las carpetas dentro de 'databases/' que representan bases de datos."""
        return [
            name for name in os.listdir(self.databases_dir)
            if os.path.isdir(os.path.join(self.databases_dir, name))
        ]
    def load_all_databases(self):
        """Carga todas las bases de datos existentes desde disco."""
        for db_folder in self.databases_path.iterdir():
            if db_folder.is_dir():
                db_name = db_folder.name
                self.databases[db_name] = self.load_tables(db_name)

    def add_trigger(self, table, event, function):
        if table not in self.triggers:
            self.triggers[table] = {}
        if event not in self.triggers[table]:
            self.triggers[table][event] = []
        self.triggers[table][event].append(function)

    def run_triggers(self, table, event, row):
        for func in self.triggers.get(table, {}).get(event, []):
            func(row)

    def set_current_database(self, db_name):
        db_folder = self.databases_path / db_name
        db_folder.mkdir(exist_ok=True)
        self.current_db = db_name
        self.tables = self.load_tables(db_name)

    def load_tables(self, db_name):
        db_folder = self.databases_path / db_name
        tables = {}
        for file in db_folder.glob("*.json"):
            with open(file, "r", encoding="utf-8") as f:
                table_name = file.stem
                tables[table_name] = json.load(f)
        return tables

    def save_table(self, table_name):
        if self.current_db is None:
            raise ValueError("No hay una base de datos seleccionada")
        db_folder = self.databases_path / self.current_db
        with open(db_folder / f"{table_name}.json", "w", encoding="utf-8") as f:
            json.dump(self.tables[table_name], f, indent=2, ensure_ascii=False)
    
    def use_database(self, name):
        path = os.path.join(self.databases_dir, name)
        if os.path.exists(path):
            self.current_database = name
            self.tables = self.load_all_tables(path)
            return True
        else:
            return False
    
    def create_user(self, username, password):
        if username in self.users:
            return f"El usuario '{username}' ya existe."
        self.users[username] = password
        return f"Usuario '{username}' creado."

    def login(self, username, password):
        if username not in self.users or self.users[username] != password:
            return "Usuario o contraseña incorrectos."
    
        self.current_user = username
    
    # Ejecutar trigger tipo AFTER_LOGIN si existe
    # Asumiendo que creaste un trigger en la tabla 'usuarios' y evento 'LOGIN'
        fake_row = {"username": username}  # Puedes pasar los datos que necesites
        self.run_triggers("usuarios", "LOGIN", fake_row)
    
        return f"Sesión iniciada como '{username}'."


    def eliminar_usuario(self, nombre):
        if nombre not in self.users:
            return f"El usuario '{nombre}' no existe."
        if self.current_user == nombre:
            self.current_user = None
        del self.users[nombre]
        return f"Usuario '{nombre}' eliminado correctamente."


   # def insert(self, table_name, values, columns=None):
       # if table_name not in self.tables:
            #raise ValueError(f"La tabla '{table_name}' no existe.")
        #table_columns = list(self.tables[table_name][0].keys())
       # if columns:
           # if set(columns) - set(table_columns):
               # raise ValueError(f"Columnas inválidas: {set(columns) - set(table_columns)}")
       # else:
           # columns = table_columns  # Si no se especifican columnas, usamos todas en orden
       # if len(columns) != len(values):
            #raise ValueError("El número de valores no coincide con el número de columnas.")
       # new_row = {col: val for col, val in zip(columns, values)}
       # self.tables[table_name].append(new_row)
       # self.save_table(table_name)
       # return f"Datos insertados en '{table_name}': {new_row}"

    def insert(self, table_name, values, columns=None):
        if table_name not in self.tables:
            raise ValueError(f"La tabla '{table_name}' no existe.")
    
    # Si la tabla está vacía, usamos las columnas proporcionadas
        if self.tables[table_name]:
            table_columns = list(self.tables[table_name][0].keys())
        elif columns:
            table_columns = columns
        else:
            raise ValueError("No se puede inferir columnas de tabla vacía. Especifica columnas.")

        if columns:
            if set(columns) - set(table_columns):
                raise ValueError(f"Columnas inválidas: {set(columns) - set(table_columns)}")
        else:
            columns = table_columns

        if len(columns) != len(values):
            raise ValueError("El número de valores no coincide con el número de columnas.")

        new_row = {col: val for col, val in zip(columns, values)}
        self.tables[table_name].append(new_row)
        self.save_table(table_name)
        return f"Datos insertados en '{table_name}': {new_row}"



    def select(self, table_name, columns, where_clause=None, order_by_clause=None, order_direction=None):
        """
        Consulta datos de la tabla especificada y los devuelve en formato de tabla.
        Ahora incluye la funcionalidad de ordenamiento ascendente o descendente.
        """
        if table_name not in self.tables:
            raise ValueError(f"La tabla '{table_name}' no existe.")

        table = self.tables[table_name]

        if columns == ["*"]:
            if not table:
                return "La tabla está vacía."
            columns = list(table[0].keys())
    
        results = []
        for row in table:
            row_matches_condition = True
            if where_clause:
                column, operator, value = where_clause
            
            # Convierte el valor a comparar al tipo de dato de la columna
            # para que la comparación funcione correctamente.
                try:
                # Intenta convertir el valor de comparación al tipo del valor en la fila
                    converted_value = type(row[column])(value)
                except (ValueError, TypeError):
                # Si no se puede convertir, usa el valor original
                    converted_value = value
            
            # Nueva lógica de comparación: solo continúa si la condición es verdadera
                if operator == "EQ":
                    if row[column] != converted_value:
                        row_matches_condition = False
                elif operator == "GT":
                    if not (row[column] > converted_value):
                        row_matches_condition = False
                elif operator == "LT":
                    if not (row[column] < converted_value):
                        row_matches_condition = False
        
            if row_matches_condition:
                results.append({col: row[col] for col in columns})

        if order_by_clause:
            if not results:
                return "La tabla está vacía y no puede ser ordenada."
        
            try:
            # Convierte la dirección a mayúsculas para evitar problemas de sensibilidad a mayúsculas
                reverse_order = order_direction.upper() == "DESC"
                results.sort(key=lambda row: row[order_by_clause], reverse=reverse_order)
            except KeyError:
                raise ValueError(f"La columna '{order_by_clause}' no existe en la tabla.")

        if not results:
            return "No se encontraron resultados"

        col_widths = {}
        for col in columns:
            col_widths[col] = max(len(str(col)), max(len(str(row[col])) for row in results))

        border = "+" + "+".join(["-" * (width + 2) for width in col_widths.values()]) + "+"
        table_str = f"\n{border}\n"
        table_str += "|" + "|".join([f" {col.center(col_widths[col])} " for col in columns]) + "|\n"
        table_str += border + "\n"
    
        for row in results:
            row_str = "|"
            for col in columns:
                row_str += f" {str(row[col]).ljust(col_widths[col])} |"
            table_str += row_str + "\n"
    
        table_str += border
        return table_str




    def delete(self, table_name, where_clause):
        if table_name not in self.tables:
            raise ValueError(f"La tabla '{table_name}' no existe.")
        table = self.tables[table_name]
        initial_count = len(table)
        if where_clause:
            table[:] = [row for row in table if not check_condition(row, where_clause)]
            self.save_table(table_name)
        return initial_count - len(table)  # Número de filas eliminadas
    
    #def create_table(self, table_name, columns):
        #if table_name in self.tables:
           # raise ValueError(f"La tabla '{table_name}' ya existe.")
        #self.tables[table_name] = [{col: None for col in columns}]
        #return f"Tabla '{table_name}' creada con columnas {columns}."
    def create_table(self, table_name, columns):
        if table_name in self.tables:
            raise ValueError(f"La tabla '{table_name}' ya existe.")
        self.tables[table_name] = {
            "columnas": columns,
            "filas": []
        }

    def count(self, table_name, where_clause=None):
        if table_name not in self.tables:
            raise ValueError(f"La tabla '{table_name}' no existe.")
        table = self.tables[table_name]
        count = 0
        for row in table:
            if where_clause:
                column, operator, value = where_clause
                if operator == "EQ" and row[column] == value:
                    count += 1
                elif operator == "GT" and row[column] > value:
                    count += 1
                elif operator == "LT" and row[column] < value:
                    count += 1
            else:
                count += 1
        return count
    

    def update(self, table_name, column, value, where_clause):
        """Actualiza valores en la tabla especificada según la condición WHERE."""
        table = self.tables.get(table_name)
        if not table:
            print(f"Error: La tabla '{table_name}' no existe.")
            return 0
        updated_rows = 0
        for row in table:
            if check_condition(row, where_clause): 
                row[column] = value
                updated_rows += 1
        self.save_table(table_name)
        return updated_rows
     
    def drop_table(self, table_name):
        """Elimina físicamente y en memoria la tabla indicada."""
        current_path = os.path.join("databases", self.current_db)
        table_file = os.path.join(current_path, f"{table_name}.json")
        if table_name in self.tables:
            del self.tables[table_name]
        if os.path.exists(table_file):
            os.remove(table_file)
            return True
        else:
            print(f"Archivo {table_file} no existe.")
        return False

    def drop_database(self, db_name):
        db_path = self.databases_path / db_name
        if not db_path.exists():
            raise FileNotFoundError(f"La base de datos '{db_name}' no existe.")
        import shutil
        shutil.rmtree(db_path)
        if db_name in self.databases:
            del self.databases[db_name]
        return True



