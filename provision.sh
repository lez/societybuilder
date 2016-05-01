#!/bin/bash -e

echo "[*] building frontend"
cd /src/frontend
npm install

echo "[*] installing python dependencies"
cd /src
pip install -r requirements.txt
echo "import pyxl.codec.register" > /usr/local/lib/python3.5/site-packages/pyxl.pth

chown -R sb.sb /src

echo "[*] setting up credentials"
bash -c "echo -ne \"a\na\n\"" | passwd
bash -c "echo -ne \"sb\nsb\n\"" | passwd sb
sed -i s/PermitRootLogin\ without-password/PermitRootLogin\ yes/ /etc/ssh/sshd_config

(sleep 1;echo -e "sb\nsb\n") | su - postgres -c "createuser -P sb"

echo "[*] Done."
