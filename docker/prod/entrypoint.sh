#!/bin/bash

#/etc/init.d/syslog-ng start
/etc/init.d/redis-server start
/etc/init.d/postgresql start
/etc/init.d/ssh start
#/etc/init.d/nginx start

echo Society Builder development environment started
read
echo Exiting...
