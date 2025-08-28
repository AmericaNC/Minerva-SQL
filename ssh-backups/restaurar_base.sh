#!/bin/bash

# Argumentos: archivo_cifrado destino_base_de_datos
ARCHIVO_BINARIO="$1"
CARPETA_RESTAURACION="${2:-./databases}"  # Usamos ./databases como ruta por defecto si no se pasa una ruta

# Verifica que se pasaron los argumentos
if [ -z "$ARCHIVO_BINARIO" ]; then
  echo "Uso: $0 archivo_cifrado [carpeta_destino]"
  exit 1
fi

# Verifica que el archivo binario exista
if [ ! -f "$ARCHIVO_BINARIO" ]; then
  echo "❌ Archivo no encontrado: $ARCHIVO_BINARIO"
  exit 1
fi

# Solicitar la passphrase para el archivo cifrado
echo "🔑 Ingresa la passphrase para descifrar el archivo:"
read -s PASSPHRASE  # La opción -s hace que no se muestre lo que se ingresa

# Paso 1: Descifrar el archivo binario cifrado
ARCHIVO_DESCIFRADO="${ARCHIVO_BINARIO%.gpg}"  # Remueve la extensión .gpg del archivo
echo "🔓 Descifrando $ARCHIVO_BINARIO..."
echo "$PASSPHRASE" | gpg --batch --yes --passphrase-fd 0 --decrypt -o "$ARCHIVO_DESCIFRADO" "$ARCHIVO_BINARIO"
if [ $? -ne 0 ]; then
  echo "❌ Error al descifrar. Verifica la passphrase."
  exit 1
fi

# Paso 2: Extraer el archivo si es un archivo .tar.gz
echo "📦 Extrayendo $ARCHIVO_DESCIFRADO en $CARPETA_RESTAURACION..."
mkdir -p "$CARPETA_RESTAURACION"  # Crea la carpeta de restauración si no existe
tar -xzf "$ARCHIVO_DESCIFRADO" -C "$CARPETA_RESTAURACION"  # Extrae el archivo tar.gz en la carpeta indicada
if [ $? -ne 0 ]; then
  echo "❌ Error al extraer."
  exit 1
fi

# Paso 3: Limpiar los archivos temporales
echo "🧹 Eliminando el archivo temporal: $ARCHIVO_DESCIFRADO"
rm "$ARCHIVO_DESCIFRADO"

echo "✅ Restauración completada en $CARPETA_RESTAURACION"