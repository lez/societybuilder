FROM sb-pynode:latest
MAINTAINER lez <lez@cirka.hu>

ADD . /src
RUN /src/docker/prod/provision.sh

ENTRYPOINT /src/docker/prod/entrypoint.sh
