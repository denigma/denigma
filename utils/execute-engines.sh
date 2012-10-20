!#/usr/bin/env/ bash

DATABASENAME="denigma"

echo 'SHOW TABLES;' \
 | mysql --defaults-file=/etc/mysql/debian.cnf ${DATABASENAME} \
 | awk '!/^Tables_in_/ {print "ALTER TABLE `"$0"` ENGINE = InnoDB;"}' \
 | column -t \
 | mysql --defaults-file=/etc/mysql/debian.cnf ${DATABASENAME}