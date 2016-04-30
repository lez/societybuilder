FROM debian:jessie
MAINTAINER lez <lez@cirka.hu>

ADD provision.sh /root/provision-base.sh
ADD pg_hba.conf /root/
ADD pg_ident.conf /root/
RUN /root/provision-base.sh

