FROM sb-pynode:latest
MAINTAINER lez <lez@cirka.hu>

ADD . /src
RUN /src/provision.sh

ENTRYPOINT /src/entrypoint.sh
