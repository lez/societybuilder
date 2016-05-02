#!/bin/bash -e

echo "[*] installing gulp"
npm install -g gulp

echo "[*] installing npm packages for the frontend"
cd /src/frontend
npm install

echo "[*] installing python dependencies"
cd /src
pip install -r requirements.txt
echo "import pyxl.codec.register" > /usr/local/lib/python3.5/site-packages/pyxl.pth

chown -R sb.sb /src
echo 'PATH=/node/node-v6.0.0-linux-x64/bin:$PATH' >> /home/sb/.bash_profile

echo "[*] setting up credentials"
bash -c "echo -ne \"a\na\n\"" | passwd
bash -c "echo -ne \"sb\nsb\n\"" | passwd sb
sed -i s/PermitRootLogin\ without-password/PermitRootLogin\ yes/ /etc/ssh/sshd_config

/etc/init.d/postgresql start
(sleep 1;echo -e "sb\nsb\n") | su - postgres -c "createuser -P sb"

echo "[*] creating database tables"
cd /src/
export PYTHONPATH=.
python script/create_tables.py development.ini
/etc/init.d/postgresql stop

echo "[*] Done."
