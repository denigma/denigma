#!/bin/bash
echo "Configuring AMI: "

sudo aptitude update; sudo aptitude -y safe-upgrade

bash ./mysql-ebs /def/sdf

bash ./init-db -D clktc -l https://github.com/hevok/denigma/raw/master/dump.sql
