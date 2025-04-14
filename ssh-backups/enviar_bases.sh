#!/bin/bash

# Ruta base local de las bases de datos
CARPETA_DATABASES="./databases"

# Argumentos
USUARIO_DESTINO="$1"
RUTA_REMOTA="$2"
HOST="${3:-localhost}"
PUERTO="${4:-5000}"
LLAVE_PRIVADA="${5:-~/.ssh/id_rsa}"
BASE_ESPECIFICA="$6"  # Nombre de la base específica (opcional)

# Verifica que se pasaron los argumentos necesarios
if [ -z "$USUARIO_DESTINO" ] || [ -z "$RUTA_REMOTA" ]; then
  echo "Uso: $0 usuario_destino ruta_remota [host] [puerto] [llave_ssh] [base_especifica]"
  exit 1
fi

# Decide qué bases procesar
if [ -n "$BASE_ESPECIFICA" ]; then
  BASES=("$CARPETA_DATABASES/$BASE_ESPECIFICA")
else
  BASES=("$CARPETA_DATABASES"/*)
fi

# Recorre las bases
for BASE in "${BASES[@]}"; do
  if [ -d "$BASE" ]; then
    NOMBRE_BASE=$(basename "$BASE")
    ARCHIVO_TEMP="${NOMBRE_BASE}.tar.gz"
    ARCHIVO_CIFRADO="${ARCHIVO_TEMP}.gpg"

    echo "⏳ Empaquetando base de datos: $NOMBRE_BASE"
    tar -czf "$ARCHIVO_TEMP" -C "$CARPETA_DATABASES" "$NOMBRE_BASE"

    echo "🔐 Cifrando $ARCHIVO_TEMP"
    gpg --batch --yes --symmetric --cipher-algo AES256 "$ARCHIVO_TEMP"

    echo "🚀 Enviando $ARCHIVO_CIFRADO a $USUARIO_DESTINO@$HOST:$RUTA_REMOTA usando llave $LLAVE_PRIVADA"
    scp -i "$LLAVE_PRIVADA" -P "$PUERTO" "$ARCHIVO_CIFRADO" "$USUARIO_DESTINO@$HOST:$RUTA_REMOTA"

    echo "🧹 Limpiando archivos temporales"
    rm "$ARCHIVO_TEMP" "$ARCHIVO_CIFRADO"

    echo "✅ Base $NOMBRE_BASE procesada."
  else
    echo "⚠️ La base '$BASE_ESPECIFICA' no existe en $CARPETA_DATABASES"
  fi
done
