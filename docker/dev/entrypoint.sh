#!/bin/bash

echo "[*] Starting Society Builder development environment"
/etc/init.d/redis-server start
/etc/init.d/postgresql start
/etc/init.d/ssh start

ip -4 addr

cd /src
pserve development.ini --reload > /tmp/pserve.log &


echo "[i] Started gulp and pserve. Stop container by pressing Enter"
read
echo "[*] Exiting..."
