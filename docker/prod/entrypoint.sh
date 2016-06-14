#!/bin/bash

umask 022
PATH=/node/current/bin:$PATH

#/etc/init.d/syslog-ng start
/etc/init.d/redis-server start
/etc/init.d/postgresql start
cd /root/python-react/examples/basic_rendering
node render_server.js 2>&1 >/var/log/react.log &
mkdir -p /var/run/uwsgi
chown sb:sb /var/run/uwsgi
cd /src

if [[ ! -f /INITIALIZED ]]; then
    if [[ -z $ROOT_PASSWD || -z $SB_PASSWD || -z $DB_PASSWD ]]; then
        echo error: missing --env ROOT_PASSWD=..., SB_PASSWD or DB_PASSWD
        exit 1
    fi
    echo "[*] setting up credentials"
    echo -e "$ROOT_PASSWD\n$ROOT_PASSWD\n" | passwd
    echo -e "$SB_PASSWD\n$SB_PASSWD\n" | passwd sb
    (sleep 1; echo -e "$DB_PASSWD\n$DB_PASSWD\n") | su - postgres -c "createuser -P sb"
    echo "[*] creating database tables"
    sed s/DB_PASSWD/$DB_PASSWD/ < production.ini.sample > production.ini
    python script/create_tables.py production.ini
    touch /INITIALIZED
fi

uwsgi --ini-paste-logged production.ini
/etc/init.d/nginx start
/etc/init.d/ssh start

echo Society Builder in production...

read;exit

while true; do
    read
done
