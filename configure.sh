#!/bin/bash
echo "Configuring AMI: "

sudo aptitude update; sudo aptitude -y safe-upgrade

git clone https://github.com/hevok/denigma.git

bash /home/ubuntu/denigma/mysql-ebs /def/sdf

bash /home/ubuntu/denigma/init-db -D clktc -l https://github.com/hevok/denigma/raw/master/dump.sql
