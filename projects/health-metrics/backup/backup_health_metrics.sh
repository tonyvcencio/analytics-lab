#!/usr/bin/env bash
set -Eeuo pipefail

DB_NAME="health_metrics"
BACKUP_DIR="/var/backups/health-metrics"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.dump"
TEMP_FILE="${BACKUP_FILE}.partial"

umask 077

if [[ "$(id -un)" != "postgres" ]]; then
    echo "ERROR: This script must run as the postgres OS user." >&2
    exit 1
fi

if [[ ! -d "$BACKUP_DIR" ]]; then
    echo "ERROR: Backup directory does not exist: $BACKUP_DIR" >&2
    exit 1
fi

cleanup() {
    rm -f -- "$TEMP_FILE"
}
trap cleanup EXIT

echo "Starting backup of ${DB_NAME} at ${TIMESTAMP}"

pg_dump \
    --dbname="$DB_NAME" \
    --format=custom \
    --file="$TEMP_FILE"

pg_restore --list "$TEMP_FILE" > /dev/null

if [[ -e "$BACKUP_FILE" ]]; then
    echo "ERROR: Backup destination already exists: $BACKUP_FILE" >&2
    exit 1
fi

mv -- "$TEMP_FILE" "$BACKUP_FILE"

echo "Backup completed: ${BACKUP_FILE}"

find "$BACKUP_DIR" \
    -maxdepth 1 \
    -type f \
    -name "${DB_NAME}_20??????T??????Z.dump" \
    -mmin +10080 \
    -print \
    -delete

echo "Backup rotation completed."
