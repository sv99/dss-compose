#!/usr/bin/env bash
# wait 30 second while completely started elasticsearch
sleep 15
echo "waited 15 sec"
sleep 15
echo "waited 30 sec"
# start uwsgi with config from current directory
uwsgi --ini uwsgi.ini
