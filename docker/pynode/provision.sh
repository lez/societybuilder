#!/bin/bash -e

echo "[*] installing node.js"
ln -s /node/node-v6.0.0-linux-x64 /node/current
PATH=/node/current/bin:$PATH

echo "[*] installing gulp globally"
npm install -g gulp

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

echo "[*] installing react render server"
cd /root
git clone git://github.com/markfinger/python-react.git
cd python-react
pip install -r requirements.txt
cd examples/basic_rendering
npm install

echo "[*] Done."
