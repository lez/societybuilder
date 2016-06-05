#!/bin/bash -e

cat > /etc/apt/sources.list << __EOF
deb http://ftp.de.debian.org/debian jessie main contrib non-free
deb http://ftp.de.debian.org/debian jessie-backports main
deb http://security.debian.org/ jessie/updates main contrib non-free
__EOF

echo "[*] updating package list"
apt-get update
apt-get -y upgrade

# pre-configure locale
debconf-set-selections <<< 'locales locales/default_environment_locale select   en_US.UTF-8'
debconf-set-selections <<< 'locales locales/locales_to_be_generated multiselect en_US.UTF-8 UTF-8'

echo "[*] installing packages"
DEBIAN_FRONTEND=noninteractive apt-get install -y -o APT::Install-Recommends=no \
    apt-utils \
    build-essential \
    bzip2 \
    curl \
    g++ \
    gcc \
    git \
    imagemagick \
    libssl-dev \
    locales \
    make \
    man \
    mytop \
    nginx \
    openssh-server \
    postgresql \
    postgresql-server-dev-9.4 \
    psmisc \
    redis-server \
    syslog-ng \
    vim \
    wget \
    xz-utils \
    zlib1g-dev

echo "[*] installing certbot (from backports)"
DEBIAN_FRONTEND=noninteractive apt-get install -y -t jessie-backports -o APT::Install-Recommends=no \
    certbot

echo "[*] removing default nginx site config"
rm /etc/nginx/sites-enabled/default

echo "[*] setting up database"
mv /root/pg_*.conf /etc/postgresql/9.4/main/
chmod 644 /etc/postgresql/9.4/main/*
/etc/init.d/postgresql start
su - postgres -c "createdb sb"
/etc/init.d/postgresql stop

echo "[*] adding user"
useradd -m sb -s /bin/bash

echo -e "\e[1;33mSociety Builder\e[0m development environment\n" > /etc/motd

echo "[*] Done."
