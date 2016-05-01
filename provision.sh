#!/bin/bash -e

echo "[*] building frontend"
cd /src/frontend
npm install

echo "[*] installing python dependencies"
cd /src
pip install -r requirements.txt
echo "import pyxl.codec.register" > /usr/local/lib/python3.5/site-packages/pyxl.pth

echo "[*] Done."
