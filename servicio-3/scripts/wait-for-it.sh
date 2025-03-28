#!/usr/bin/env bash
#   Use this script to test if a given TCP host/port are available

WAITFORIT_HOST="$1"
WAITFORIT_PORT="$2"
shift 2
WAITFORIT_TIMEOUT="${WAITFORIT_TIMEOUT:-15}"

echo "[WAIT-FOR-IT] Esperando $WAITFORIT_HOST:$WAITFORIT_PORT por hasta $WAITFORIT_TIMEOUT segundos..."

for i in $(seq $WAITFORIT_TIMEOUT); do
  nc -z "$WAITFORIT_HOST" "$WAITFORIT_PORT" > /dev/null 2>&1
  result=$?
  if [ $result -eq 0 ]; then
    echo "[WAIT-FOR-IT] $WAITFORIT_HOST:$WAITFORIT_PORT está disponible 🎉"
    break
  fi
  echo "[WAIT-FOR-IT] Esperando... ($i)"
  sleep 1
done

if [ $result -ne 0 ]; then
  echo "[WAIT-FOR-IT] Timeout después de $WAITFORIT_TIMEOUT segundos ⌛"
  exit 1
fi

exec "$@"