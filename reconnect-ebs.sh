#!/bin/sh
echo "*** Restoring an EBS database connection. ***"
sudo aptitude update && sudo aptitude upgrade -y
export DEBIAN_FRONTEND=noninteractive
sudo -E aptitude install -y xfsprogs mysql-server

echo "/dev/sdf /vol xfs noatime 0 0" | sudo tee -a /etc/fstab
sudo mkdir -m 000 /vol
sudo mount /vol

sudo find /vol/{lib,log}/mysql/ ! -user root -print0 | sudo xargs -0 -r chown mysql
sudo find /vol/{lib,log}/mysql/ ! -group root -a ! -group adm -print0 | sudo xargs -0 -r chgrp mysql

echo "*** Point MySQL to the correct database files on the EBS volume. **"
sudo /etc/init.d/mysql stop
echo "/vol/etc/mysql /etc/mysql none bind" | sudo tee -a /etc/fstab
sudo mount /etc/mysql

echo "/vol/lib/mysql /var/lib/mysql none bind" | sudo tee -a /etc/fstab
sudo mount /var/lib/mysql

echo "/vol/log/mysql /var/log/mysql none bind" | sudo tee -a /etc/fstab
sudo mount /var/log/mysql

sudo /etc/init.d/mysql start
