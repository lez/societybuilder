FROM sb-pynode:latest
MAINTAINER lez <lez@cirka.hu>

ADD docker/prod/fs /

ADD . /src
RUN /src/docker/prod/provision.sh

ENTRYPOINT /src/docker/prod/entrypoint.sh
EXPOSE 80
EXPOSE 443
