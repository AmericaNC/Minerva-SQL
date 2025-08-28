#!/bin/bash

ARCHIVO_CIFRADO="$1"
CARPETA_RESTAURACION="${2:-./databases}" 

if [ -z "$ARCHIVO_CIFRADO" ]; then
  echo "Uso: $0 archivo_cifrado [carpeta_destino]"
  exit 1
fi

if [ ! -f "$ARCHIVO_CIFRADO" ]; then
  echo "❌ Archivo no encontrado: $ARCHIVO_CIFRADO"
  exit 1
fi

echo "🔑 Ingresa la passphrase para la clave privada GPG:"
read -s PASSPHRASE  
ARCHIVO_DESCIFRADO="${ARCHIVO_CIFRADO%.gpg}"  
echo "🔓 Descifrando $ARCHIVO_CIFRADO..."

gpg --batch --yes --passphrase "$PASSPHRASE" --decrypt -o "$ARCHIVO_DESCIFRADO" "$ARCHIVO_CIFRADO"
if [ $? -ne 0 ]; then
  echo "❌ Error al descifrar. Verifica la passphrase."
  exit 1
fi

echo "📦 Extrayendo $ARCHIVO_DESCIFRADO en $CARPETA_RESTAURACION..."
mkdir -p "$CARPETA_RESTAURACION"  


tar -xzf "$ARCHIVO_DESCIFRADO" -C "$CARPETA_RESTAURACION" --strip-components=1  

if [ $? -ne 0 ]; then
  echo "❌ Error al extraer."
  exit 1
fi

echo "🧹 Eliminando el archivo temporal: $ARCHIVO_DESCIFRADO"
rm "$ARCHIVO_DESCIFRADO"

echo "✅ Restauración completada en $CARPETA_RESTAURACION"
