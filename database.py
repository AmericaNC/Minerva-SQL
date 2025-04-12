from pathlib import Path
import os
import json

class Database:
    def __init__(self):
        self.databases_path = Path("databases")
        self.databases_dir = "databases"
        self.databases_path.mkdir(exist_ok=True)
        self.databases = {"default": {}}
        self.current_db = "default"
        self.users = {"root": "rootpass"}
        self.current_user = "root"  # ← login automático
        self.permissions = {
            "root": {"crear_tabla", "ver_usuarios", "insertar", "usar_base", "crear_base", 
                     "eliminar_usuario", "otorgar", "ver_bases", "ver_tablas", 
                     "actualizar", "contar", "eliminar", "eliminar_tablas"}
        }

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
        return f"Sesión iniciada como '{username}'."

    def eliminar_usuario(self, nombre):
        if nombre not in self.users:
            return f"El usuario '{nombre}' no existe."
        if self.current_user == nombre:
            self.current_user = None
        del self.users[nombre]
        return f"Usuario '{nombre}' eliminado correctamente."


    def insert(self, table_name, values, columns=None):
        if table_name not in self.tables:
            raise ValueError(f"La tabla '{table_name}' no existe.")
        table_columns = list(self.tables[table_name][0].keys())
        if columns:
            if set(columns) - set(table_columns):
                raise ValueError(f"Columnas inválidas: {set(columns) - set(table_columns)}")
        else:
            columns = table_columns  # Si no se especifican columnas, usamos todas en orden
        if len(columns) != len(values):
            raise ValueError("El número de valores no coincide con el número de columnas.")
        new_row = {col: val for col, val in zip(columns, values)}
        self.tables[table_name].append(new_row)
        self.save_table(table_name)
        return f"Datos insertados en '{table_name}': {new_row}"

    def select(self, table_name, columns, where_clause=None):
        """Consulta datos de la tabla especificada."""
        if table_name not in self.tables:
            raise ValueError(f"La tabla '{table_name}' no existe.")
        table = self.tables[table_name]
        results = []
        for row in table:
            if where_clause:
                column, operator, value = where_clause
                if operator == "GT" and not (row[column] > value):
                    continue
                if operator == "LT" and not (row[column] < value):
                    continue
                if operator == "EQ" and not (row[column] == value):
                    continue
            results.append({col: row[col] for col in columns})
        return results
    
    def delete(self, table_name, where_clause):
        if table_name not in self.tables:
            raise ValueError(f"La tabla '{table_name}' no existe.")
        table = self.tables[table_name]
        initial_count = len(table)
        if where_clause:
            column, operator, value = where_clause
            table[:] = [row for row in table if not check_condition(row, column, operator, value)]
            self.save_table(table_name)
        return initial_count - len(table)  # Número de filas eliminadas
    
    def create_table(self, table_name, columns):
        if table_name in self.tables:
            raise ValueError(f"La tabla '{table_name}' ya existe.")
        
        # Crear una tabla vacía con las columnas especificadas
        self.tables[table_name] = [{col: None for col in columns}]
        return f"Tabla '{table_name}' creada con columnas {columns}."
    
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
        where_column, operator, where_value = where_clause
        updated_rows = 0
        for row in table:
            if check_condition(row, where_column, operator, where_value):
                row[column] = value
                updated_rows += 1
        self.save_table(table_name)
        return updated_rows
     
    def drop_table(self, table_name, current_path):
        """Elimina físicamente y en memoria la tabla indicada."""
        table_file = os.path.join(current_path, f"{table_name}.json")
        if table_name in self.tables:
            del self.tables[table_name]
        if os.path.exists(table_file):
            os.remove(table_file)
            return True
        else:
            print(f"Archivo {table_file} no existe.")
        return False


    def check_condition(row, column, operator, value):
        row_value = row.get(column)
        if operator == '=':
            return row_value == value
        elif operator == '>':
            return row_value > value
        elif operator == '<':
            return row_value < value
        else:
            raise ValueError(f"Operador desconocido: {operator}")


