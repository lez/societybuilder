#!/bin/bash

echo "[*] Starting Society Builder development environment"
/etc/init.d/redis-server start
/etc/init.d/postgresql start
/etc/init.d/ssh start

ip -4 a
echo "[i] Run gulp and pserve manually. Stop container by pressing Enter"
read
echo "[*] Exiting..."
