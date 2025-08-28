#!/bin/bash

# Uso: ./descargar_respaldo.sh usuario_servidor archivo_remoto [host] [carpeta_local]
USUARIO="$1"
ARCHIVO_REMOTO="$2"
HOST="${3:-localhost}"  # Si no se especifica, usa localhost
DESTINO="${4:-./backups}"  # Carpeta destino, por defecto ./backups
PUERTO="${5:-5000}"  # Puerto, por defecto 5000

if [ -z "$USUARIO" ] || [ -z "$ARCHIVO_REMOTO" ]; then
  echo "Uso: $0 usuario archivo_remoto [host] [carpeta_local] [puerto]"
  exit 1
fi

# Asegúrate de que la carpeta de destino exista
mkdir -p "$DESTINO"

# Componer el nombre del archivo descargado (se cambiará a "respaldo" siempre)
ARCHIVO_DESTINO="$DESTINO/respaldo"

echo "📥 Descargando $ARCHIVO_REMOTO desde $USUARIO@$HOST:$PUERTO a $ARCHIVO_DESTINO..."

# Usar scp para descargar el archivo
scp -P "$PUERTO" "$USUARIO@$HOST:$ARCHIVO_REMOTO" "$ARCHIVO_DESTINO"

# Comprobamos si la descarga fue exitosa
if [ $? -eq 0 ]; then
  echo "✅ Descarga completada correctamente en $ARCHIVO_DESTINO."
else
  echo "❌ Error durante la descarga."
fi