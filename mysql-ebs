#!/bin/sh

VOLUME=$1

if [ -z $VOLUME ]; then
    echo "You must specify the volume, like /dev/sdf"
    exit 1;
fi

echo "*** Installing MySQL (with no root password) ***"
sudo DEBIAN_FRONTEND=noninteractive aptitude install -y mysql-server

echo "*** Creating XFS filesystem and moving mysql configuration ***"
sudo apt-get install -y xfsprogs
grep -q xfs /proc/filesystems || sudo modprobe xfs
sudo mkfs.xfs $VOLUME

echo "$VOLUME /vol xfs noatime 0 0" | sudo tee -a /etc/fstab
sudo mkdir -m 000 /vol
sudo mount /vol

sudo /etc/init.d/mysql stop
sudo mkdir /vol/etc /vol/lib /vol/log
sudo mv /etc/mysql     /vol/etc/
sudo mv /var/lib/mysql /vol/lib/
sudo mv /var/log/mysql /vol/log/

sudo mkdir /etc/mysql
sudo mkdir /var/lib/mysql
sudo mkdir /var/log/mysql

echo "/vol/etc/mysql /etc/mysql     none bind" | sudo tee -a /etc/fstab
sudo mount /etc/mysql

echo "/vol/lib/mysql /var/lib/mysql none bind" | sudo tee -a /etc/fstab
sudo mount /var/lib/mysql

echo "/vol/log/mysql /var/log/mysql none bind" | sudo tee -a /etc/fstab
sudo mount /var/log/mysql

sudo /etc/init.d/mysql start

echo "*** Done. Mysql is now running on EBS backed volume at $VOLUME ***"
