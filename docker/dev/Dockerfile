FROM sb-pynode:latest
MAINTAINER lez <lez@cirka.hu>

ADD docker/dev/.bashrc /root
ADD . /src
RUN /src/docker/dev/provision.sh

ENTRYPOINT /src/docker/dev/entrypoint.sh
