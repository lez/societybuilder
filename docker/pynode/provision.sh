#!/bin/bash -e

echo "[*] installing node.js"
ln -s /node/node-v6.0.0-linux-x64 /node/current

echo "[*] installing python"
cd /root/Python-3.5.1
CXX=/usr/bin/g++ ./configure
make
make install
ln -s python3 /usr/local/bin/python
cd ..
rm -rf Python*

echo "[*] installing pip"
python3 /root/get-pip.py
rm /root/get-pip.py

echo "[*] Done."
