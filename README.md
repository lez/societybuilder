# Society Builder #

[Society Builder](https://github.com/lez/societybuilder) is a free and open-source community site engine.

## Goals ##

The main goal is to create effective communication means for groups with purpose.
Another goal is to keep the developing experience joyful.

## Installing the development environment ##

```
git clone https://github.com/lez/societybuilder
cd societybuilder
./build all
docker run --volume=$(pwd):/src -i sb-dev
```

Once the environment is up and running, run gulp to (re)build the js and css bundles.
```
ssh root@172.17.0.2
Password: a

cd /src/frontend
gulp
```

Gulp runs a BrowserSync proxy on [port 3000](http://172.17.0.2:3000) to the [application](http://172.17.0.2).
If source files are modified in /src, gulp rebuilds the web artifacts and notifies the browser via BrowserSync.

On a separate shell, run (as root):
```
cd /src
pserve development.ini --reload
```

This serves the site on http://172.17.0.2

## Technology stack ##

 * Python on the backend side
 * Pyramid web framework
 * modified version of [pyxl3](https://github.com/lez/pyxl3) for generating static HTML content
 * React and Redux in the browser
 * Postgresql for data storage
 * Redis for session storage

## Roadmap ##

 * peer moderation of comments and posts
   * Any user can suggest alternative version of content. The suggestion can be discussed among all participants.
 * image browser

## License ##

Affero General Public License 3.0

