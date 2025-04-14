#!/bin/bash

# Argumentos: archivo_cifrado destino_base_de_datos
ARCHIVO_CIFRADO="$1"
CARPETA_RESTAURACION="${2:-./databases}"

# Verifica argumentos
if [ -z "$ARCHIVO_CIFRADO" ]; then
  echo "Uso: $0 archivo_cifrado.gpg [carpeta_destino]"
  exit 1
fi

# Verifica que exista el archivo
if [ ! -f "$ARCHIVO_CIFRADO" ]; then
  echo "❌ Archivo no encontrado: $ARCHIVO_CIFRADO"
  exit 1
fi

# Paso 1: Descifrar
ARCHIVO_TAR="${ARCHIVO_CIFRADO%.gpg}"
echo "🔓 Descifrando $ARCHIVO_CIFRADO..."
gpg --batch --yes --decrypt -o "$ARCHIVO_TAR" "$ARCHIVO_CIFRADO"
if [ $? -ne 0 ]; then
  echo "❌ Error al descifrar."
  exit 1
fi

# Paso 2: Extraer
echo "📦 Extrayendo $ARCHIVO_TAR en $CARPETA_RESTAURACION..."
mkdir -p "$CARPETA_RESTAURACION"
tar -xzf "$ARCHIVO_TAR" -C "$CARPETA_RESTAURACION"
if [ $? -ne 0 ]; then
  echo "❌ Error al extraer."
  exit 1
fi

# Paso 3: Limpiar temporal
echo "🧹 Eliminando temporal: $ARCHIVO_TAR"
rm "$ARCHIVO_TAR"

echo "✅ Restauración completada en $CARPETA_RESTAURACION"
