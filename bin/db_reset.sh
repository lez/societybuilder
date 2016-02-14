#!/bin/sh

DBNAME=is

psql -U $DBNAME << _EOF
drop schema public cascade;
create schema public;
_EOF

bin_dir=$(dirname $(readlink -f "$0"))
export PYTHONPATH=$(dirname "$bin_dir")
python "$bin_dir/create_tables.py"
