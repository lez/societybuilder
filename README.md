# Society Builder #

[Society Builder](https://github.com/lez/societybuilder) is an open-source community site engine.

## Why? ##

The software was written in the need of a good quality society building platform.
Developing this software must be a joyful experience.

## Goals ##

The goal is to create effective communication means for groups

## Installing the development environment ##

git clone https://github.com/lez/societybuilder
cd societybuilder
./build all
docker run -i sb-app

ssh into the box

cd /src/frontend
gulp

cd /src
pserve development.ini --reload

you can visit the site (most probably http://172.17.0.2)

## Technology stack ##

 * python
 * pyramid web framework
 * a modified version of [pyxl3](https://github.com/lez/pyxl3) for creating HTML blocks in a safe way
 * React and Redux for the client
 * postgresql for persistent data storage
 * redis for session storage and caching
 * node.js for rendering react elements on the server

## License ##

Affero General Public License 3.0

