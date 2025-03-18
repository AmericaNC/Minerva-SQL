class Database:
    def __init__(self):
        self.tables = {}  # Diccionario para almacenar las tablas

    def insert(self, table_name, values):
        """Inserta valores en la tabla especificada."""
        # Si la tabla no existe, la creamos.
        if table_name not in self.tables:
            self.tables[table_name] = []

        # Convertir los valores a enteros o flotantes si es necesario
        converted_values = [
            int(val) if val.isdigit() else float(val) if "." in val else val
            for val in values
        ]

        # Agregar los valores convertidos a la tabla
        self.tables[table_name].append(
            dict(zip(self.tables[table_name][0].keys(), converted_values))
        )
        # Se usa 'dict(zip(...))' para crear un diccionario con las claves de la tabla.

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

