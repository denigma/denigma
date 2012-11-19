#!/usr/bin/env/ bash

DATABASENAME="denigma"

echo "SELECT TABLE_NAME, ENGINE
  FROM information_schema.TABLES
  WHERE TABLE_SCHEMA = '${DATABASENAME}';" | mysql --defaults-file=/etc/mysql/debian.cnf