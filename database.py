class Database:
    def __init__(self):
        self.databases = {"default": {}}
        self.current_db = "default"

        # Usuarios
        self.users = {"root": "rootpass"}
        self.current_user = "root"  # ← login automático

        # Permisos
        self.permissions = {
            "root": {"crear_tabla", "ver_usuario", "insertar", "usar_base", "crear_base", 
                     "eliminar_usuario", "otorgar", "ver_bases", "ver_tablas", 
                     "actualizar", "contar", "eliminar", "eliminar_tablas"}
        }
    @property
    def tables(self):
        return self.databases[self.current_db]
    
    def use_database(self, name):
        if name not in self.databases:
            self.databases[name] = {}
        self.current_db = name
        return f"Usando base de datos: {name}"
    
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

        # Obtener las columnas de la tabla
        table_columns = list(self.tables[table_name][0].keys())

        if columns:
            if set(columns) - set(table_columns):
                raise ValueError(f"Columnas inválidas: {set(columns) - set(table_columns)}")

        else:
            columns = table_columns  # Si no se especifican columnas, usamos todas en orden

        if len(columns) != len(values):
            raise ValueError("El número de valores no coincide con el número de columnas.")

        # Crear el nuevo registro con valores alineados a las columnas
        new_row = {col: val for col, val in zip(columns, values)}
        self.tables[table_name].append(new_row)

        return f"Datos insertados en '{table_name}': {new_row}"

    def select(self, table_name, columns, where_clause=None):
        """Consulta datos de la tabla especificada."""
        if table_name not in self.tables:
            raise ValueError(f"La tabla '{table_name}' no existe.")

        # Obtener la tabla
        table = self.tables[table_name]
        results = []

        # Filtrar por la condición WHERE si existe
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
        # Obtén la tabla de los datos en memoria
        table = self.tables.get(table_name)
        if not table:
            print(f"Error: La tabla '{table_name}' no existe.")
            return 0

        # Desempaquetamos la cláusula WHERE
        where_column, operator, where_value = where_clause

        # Contador de filas actualizadas
        updated_rows = 0

        # Recorremos las filas de la tabla
        for row in table:
            # Verificar si la condición WHERE se cumple
            if check_condition(row, where_column, operator, where_value):
                # Si se cumple, actualizamos la columna
                row[column] = value
                updated_rows += 1

        return updated_rows


def check_condition(row, column, operator, value):
    """Verifica si la condición WHERE se cumple para una fila"""
    row_value = row[column]

    if operator == "=":
        return row_value == value
    elif operator == ">":
        return row_value > value
    elif operator == "<":
        return row_value < value
    else:
        return False

