FROM sb-pynode:latest
MAINTAINER lez <lez@cirka.hu>

ADD docker/prod/pg_hba.conf /root/
ADD docker/prod/pg_ident.conf /root/

ADD . /src
RUN /src/docker/dev/provision.sh

ENTRYPOINT /src/docker/dev/entrypoint.sh
