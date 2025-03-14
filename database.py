class Database:
    def __init__(self):
        self.tables = {}  # Diccionario para almacenar las tablas

    def insert(self, table_name, values):
        """Inserta valores en la tabla especificada."""
        # Si la tabla no existe, la creamos.
        if table_name not in self.tables:
            self.tables[table_name] = []
        
        # Convertir los valores a enteros o flotantes si es necesario
        converted_values = [int(val) if val.isdigit() else float(val) if '.' in val else val for val in values]

        # Agregar los valores convertidos a la tabla
        self.tables[table_name].append(dict(zip(self.tables[table_name][0].keys(), converted_values)))
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
                if operator == "GT" and not (row[column] > value): continue
                if operator == "LT" and not (row[column] < value): continue
                if operator == "EQ" and not (row[column] == value): continue
            results.append({col: row[col] for col in columns})

        return results
