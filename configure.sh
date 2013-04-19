#!/bin/bash
echo "Configuring AMI: "

sudo aptitude update; sudo aptitude -y safe-upgrade

sudo bash ./denigma/mysql-ebs /def/sdf

sudo bash ./denigma/init-db -D denigma -l https://github.com/denigma/denigma/raw/master/dump.sql
