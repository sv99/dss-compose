#!/usr/bin/env bash
# default value for first comand line argument - backup source
BACKUP_FILE=${1:-$(ls -td dbbackup/*.sql | head -1)}
CMD="export MYSQL_PWD=\$MYSQL_ROOT_PASSWORD; exec mysql -D DSS"
echo $CMD

echo Restore from $BACKUP_FILE
docker-compose exec -T mysql sh -c "$CMD" < $BACKUP_FILE
