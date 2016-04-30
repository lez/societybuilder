#!/bin/bash -e

echo "[*] building frontend"
cd /src/frontend
/usr/local/bin/npm install
# FIXME node ./node_modules/gulp/bin/gulp.js build_js
# FIXME node ./node_modules/gulp/bin/gulp.js build_css

echo "[*] installing python dependencies"
cd /src
pip install -r requirements.txt
echo "import pyxl.codec.register" > /usr/local/lib/python3.5/site-packages/pyxl.pth

echo "[*] Done."
