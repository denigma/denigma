#!/usr/bin/env bash

open_external_port() {
    cat <<EOF | sudo tee /etc/mysql/conf.d/listen_externally.cnf
[mysqld]
    bind-address = 0.0.0.0
EOF
    sudo /etc/init.d/mysql restart
}
open_external_port






