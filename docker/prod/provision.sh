#!/bin/bash -e
PATH=/node/current/bin:$PATH

echo "[*] installing python dependencies"
cd /src
pip install -r requirements.txt
echo "import pyxl.codec.register" > /usr/local/lib/python3.5/site-packages/pyxl.pth
pip install .

echo "[*] installing frontend dependencies"
cd /src/frontend
npm install

echo "[*] building js"
gulp build_js

echo "[*] building css"
gulp build_css

echo "[*] setting up periodic letsencrypt cert renewal"
crontab /src/docker/prod/crontab

echo "[i] start with \`docker run --env DB_PASSWD=sb --env ROOT_PASSWD=a --env SB_PASSWD=sb --hostname prod --name prod -i sb-prod\`"
echo "[*] Done."
