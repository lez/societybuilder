#!/bin/bash -e

mkdir /node
cd /node

echo "[*] installing node.js"
wget --no-check-certificate https://nodejs.org/dist/v6.0.0/node-v6.0.0-linux-x64.tar.xz
tar xfJ node-v6.0.0-linux-x64.tar.xz
ln -s /node/node-v6.0.0-linux-x64/bin/node /usr/local/bin/node
ln -s /node/node-v6.0.0-linux-x64/bin/npm /usr/local/bin/npm

echo "[*] installing python"
cd /root
wget --no-check-certificate https://www.python.org/ftp/python/3.5.1/Python-3.5.1.tar.xz
tar xfJ Python-3.5.1.tar.xz
cd Python-3.5.1
CXX=/usr/bin/g++ ./configure
make
make install
ln -s python3 /usr/local/bin/python
cd ..
rm -rf Python*

echo "[*] installing pip"
wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py

echo "[*] Done."
