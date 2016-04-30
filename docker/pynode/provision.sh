#!/bin/bash -e

mkdir /root/src
cd /root/src

echo "[*] installing node.js"
wget --no-check-certificate https://nodejs.org/dist/v6.0.0/node-v6.0.0-linux-x64.tar.xz
tar xfJ node-v6.0.0-linux-x64.tar.xz
ln -s /root/src/node-v6.0.0-linux-x64/bin/node /usr/local/bin/node
ln -s /root/src/node-v6.0.0-linux-x64/bin/npm /usr/local/bin/npm

echo "[*] installing python"
wget --no-check-certificate https://www.python.org/ftp/python/3.5.1/Python-3.5.1.tar.xz
tar xfJ Python-3.5.1.tar.xz
cd Python-3.5.1
CXX=/usr/bin/g++ ./configure
make
make install
ln -s python3 /usr/local/bin/python
cd ..
wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py

echo "[*] Done."
