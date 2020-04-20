#!/usr/bin/env bash
# wait 30 second while completely started elasticsearch and mysql
sleep 10
echo "waited 10 sec"
sleep 10
echo "waited 20 sec"
# start uwsgi with config from current directory
uwsgi --ini uwsgi.ini
