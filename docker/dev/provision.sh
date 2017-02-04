#!/bin/bash -e
PATH=/node/current/bin:$PATH

echo "[*] setting up database"
/etc/init.d/postgresql start
mv /root/pg_*.conf /etc/postgresql/9.4/main/
chmod 644 /etc/postgresql/9.4/main/*
su - postgres -c "createdb sb"

echo "[*] setting up credentials"
bash -c "echo -ne \"a\na\n\"" | passwd
sed -i s/PermitRootLogin\ without-password/PermitRootLogin\ yes/ /etc/ssh/sshd_config
(sleep 1;echo -e "sb\nsb\n") | su - postgres -c "createuser -P sb"

echo "[*] setting up hstore"
cd /root
cat > .pgpass <<< 'localhost:5432:sb:sb:sb'
chmod 600 .pgpass
su - postgres -c "psql sb" <<< "create extension hstore;"

echo "[*] installing frontend dependencies"
cd /src/frontend
npm install

echo "[*] installing python dependencies"
cd /src
pip install -r requirements.txt
echo "import pyxl.codec.register" > /usr/local/lib/python3.5/site-packages/pyxl.pth
pip install -e .

echo "[*] creating database tables"
cd /src/
PYTHONPATH=/src python script/create_tables.py development.ini
/etc/init.d/postgresql stop

echo "[*] Done."
