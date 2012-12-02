#!/usr/bin/env bash

. env/bin/activate
python ./manage.py rebuild_index
chmod 777 ./denigma/whoosh_index