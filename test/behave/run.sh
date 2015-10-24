#!/bin/sh

psql -U is >/dev/null << _EOF
DELETE from users where login='testuser';
_EOF

behave
