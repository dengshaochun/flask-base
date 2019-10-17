#!/usr/bin/env sh

until flask db upgrade 2> /dev/null
do
    flask db init || echo "init failed"
    flask db migrate || echo "migrate failed"
done

exec flask $@
