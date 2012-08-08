#!/bin/bash
echo "Configuring AMI: "

sudo aptitude  update; sudo -y safe-upgrade

git clone https://github.com/hevok/denigma.git

bash /home/ubuntu/denigma/mysql-ebs /def/sdf

bash /home/denigma/init-db -D clktc -l https://github.com/hevok/denigma/raw/master/dump.sql

read -e ACCESS

sudo bash /home/ubuntu/denigma/aws-django -n clktc -d https://github.com/hevok/denigma/raw/master/clktc.tgz -s "/s" $ACCESS
