FROM sb-base:latest
MAINTAINER lez <lez@cirka.hu>

ADD node-v6.0.0-linux-x64.tar.xz /node
ADD Python-3.5.1.tar.xz /root/
ADD get-pip.py /root/

ADD provision.sh /root/provision-pynode.sh
RUN /root/provision-pynode.sh
