#!/usr/bin/env bash
# default value for first comand line argument - backup source
BACKUP_FILE=dbbackup/dss_$(date +%Y%m%d).sql
CMD="export MYSQL_PWD=\$MYSQL_ROOT_PASSWORD; exec mysqldump DSS"
echo $CMD

echo Dump to $BACKUP_FILE
docker-compose exec mysql sh -c "$CMD" > $BACKUP_FILE
