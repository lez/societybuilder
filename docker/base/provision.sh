#!/bin/bash -e

cat > /etc/apt/sources.list << __EOF
deb http://ftp.de.debian.org/debian jessie main contrib non-free
deb http://security.debian.org/ jessie/updates main contrib non-free
__EOF

echo "[*] updating package list"
apt-get update
apt-get upgrade

# pre-configure locale
debconf-set-selections <<< 'locales locales/default_environment_locale select   en_US.UTF-8'
debconf-set-selections <<< 'locales locales/locales_to_be_generated multiselect en_US.UTF-8 UTF-8'

echo "[*] installing packages"
DEBIAN_FRONTEND=noninteractive apt-get install -y -o APT::Install-Recommends=no \
	apt-utils \
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
	redis-server \
	syslog-ng \
	vim \
	wget \
	xz-utils \
	zlib1g-dev

sed -i s/PermitRootLogin\ without-password/PermitRootLogin\ yes/ /etc/ssh/sshd_config
bash -c "echo -ne \"a\na\n\"" | passwd
echo -e "\e[1;33mSociety Builder\e[0m development enironment\n" > /etc/motd

echo "[*] Done."
