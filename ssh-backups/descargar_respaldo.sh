#!/bin/bash

# Uso: ./descargar_respaldo.sh usuario_servidor archivo_remoto [host] [carpeta_local]
USUARIO="$1"
ARCHIVO_REMOTO="$2"
HOST="${3:-localhost}"
DESTINO="${4:-.}"
PUERTO="${5:-5000}"  # Puerto, por defecto 5000

if [ -z "$USUARIO" ] || [ -z "$ARCHIVO_REMOTO" ]; then
  echo "Uso: $0 usuario archivo_remoto [host] [carpeta_local] [puerto]"
  exit 1
fi

echo "📥 Descargando $ARCHIVO_REMOTO desde $USUARIO@$HOST:$PUERTO a $DESTINO..."
scp -P "$PUERTO" "$USUARIO@$HOST:$ARCHIVO_REMOTO" "$DESTINO"

if [ $? -eq 0 ]; then
  echo "✅ Descarga completada."
else
  echo "❌ Error durante la descarga."
fi
