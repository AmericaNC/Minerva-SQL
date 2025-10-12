import os
from flask import Flask, request, jsonify, render_template
DATABASE_DIR = 'databases'
try:
    if not os.path.exists(DATABASE_DIR):
        # Crear el directorio 'databases'
        os.makedirs(DATABASE_DIR, exist_ok=True)
    ejemplo_db_path = os.path.join(DATABASE_DIR, 'mi_primera_bd')
    if not os.path.exists(ejemplo_db_path):
         os.makedirs(ejemplo_db_path, exist_ok=True)
         
         with open(os.path.join(ejemplo_db_path, 'usuarios.json'), 'w') as f:
             f.write('{"columns": ["id", "nombre", "edad"], "data": []}')
             
         with open(os.path.join(ejemplo_db_path, 'productos.json'), 'w') as f:
             f.write('{"columns": ["sku", "nombre_prod", "precio"], "data": []}')
    # -----------------------------------------------------------


    
    # DEBUG: Muestra la ruta absoluta en la consola al iniciar
    print("--- Configuración de Directorios ---")
    print(f"Ruta Absoluta de Bases de Datos: {os.path.abspath(DATABASE_DIR)}")
    print("-----------------------------------")

except Exception as e:
    # Si hay un error de permisos o ruta, lo registramos.
    print(f"Advertencia: No se pudo verificar o crear el directorio de BDD en {DATABASE_DIR}. Error: {e}")

# ***********************************
# 2. LÓGICA DEL CORE
# ***********************************
# Asegúrate de que este archivo existe y es accesible
try:
    from interprete_core import procesar_consulta 
except ImportError:
    print("¡ERROR CRÍTICO! No se encontró interprete_core.py.")
    # Función de simulación para pruebas si el core no está disponible
    def procesar_consulta(comando):
          return f"Error: Core no encontrado. Comando simulado: {comando}"
    
# ***********************************
# 3. APLICACIÓN FLASK
# ***********************************
app = Flask(__name__)

@app.route('/')
def home():
    """Sirve el archivo HTML principal (index.html) desde la carpeta 'templates'."""
    # Nota: Flask busca por defecto en la carpeta 'templates'
    return render_template('index.html')

# ENDPOINT: Para obtener la lista de bases de datos
@app.route('/databases', methods=['GET'])
def get_databases():
    """Escanea el directorio de BDD (carpetas) y devuelve una lista de nombres."""
    try:
        items = os.listdir(DATABASE_DIR)
        databases = [
            item for item in items 
            if os.path.isdir(os.path.join(DATABASE_DIR, item)) and not item.startswith('.')
        ]
        
        databases.sort()
        print(f"DEBUG BDD: Bases de datos encontradas: {databases}") # LOG DEPURACIÓN
        
        return jsonify({'databases': databases})
    except FileNotFoundError:
        return jsonify({'error': f"Ruta no encontrada: {DATABASE_DIR}", 'databases': []}), 404
    except Exception as e:
        print(f"Error al listar bases de datos: {e}")
        return jsonify({'error': str(e), 'databases': []}), 500

# NUEVO ENDPOINT: Para obtener las tablas dentro de una BDD específica
@app.route('/tables/<db_name>', methods=['GET'])
def get_tables(db_name):
    """Escanea la carpeta de una BDD específica y devuelve una lista de archivos JSON (tablas)."""
    db_path = os.path.join(DATABASE_DIR, db_name)
    
    if not os.path.isdir(db_path):
        print(f"DEBUG TABLAS: Error, el path {db_path} NO es un directorio.") # LOG DEPURACIÓN
        return jsonify({'error': f"Base de datos '{db_name}' no encontrada."}), 404

    try:
        # LOG DEPURACIÓN: Ruta y contenido
        print(f"DEBUG TABLAS: Intentando listar archivos en: {db_path}")
        items = os.listdir(db_path)
        print(f"DEBUG TABLAS: Contenido crudo de la carpeta: {items}")

        tables = []
        for item in items:
            item_path = os.path.join(db_path, item)
            # Asegura que sea un archivo y no un archivo oculto, y lo trata como tabla
            if os.path.isfile(item_path) and not item.startswith('.'):
                # Elimina la extensión del archivo (ej: 'usuarios.json' -> 'usuarios')
                table_name, _ = os.path.splitext(item)
                tables.append(table_name)

        tables.sort()
        # LOG DEPURACIÓN: Resultado final
        print(f"DEBUG TABLAS: Tablas finales a enviar: {tables}")
        
        return jsonify({'tables': tables})
    except Exception as e:
        print(f"Error al listar tablas en {db_name}: {e}")
        return jsonify({'error': str(e)}), 500


# ENDPOINT: Para ejecutar comandos SQL
@app.route('/interpretar', methods=['POST'])
def interpretar_comando():
    """Ruta para enviar el comando SQL al core del intérprete."""
    try:
        comando = request.json['comando']
        
        # Llama a tu función principal de lógica
        resultado = procesar_consulta(comando)
        
        # Devuelve el resultado. Es crucial que el core devuelva el resultado
        # en formato string para que el frontend lo muestre.
        return jsonify({'resultado': resultado})

    except Exception as e:
        # Captura errores de tu intérprete o errores internos del servidor
        return jsonify({'resultado': f"Error en el servidor: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
