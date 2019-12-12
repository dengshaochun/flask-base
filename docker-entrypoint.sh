#!/usr/bin/env bash

set -e

celery_worker() {
  echo "start celery worker"
  exec celery -A demo.celery_app.celery_worker worker -l info
}

celery_beat() {
  echo "start celery beat"
  exec celery -A demo.celery_app.celery_worker beat -l info
}

server() {
  echo "start web server"
  exec gunicorn -w 4 -b 0.0.0.0:5000 manage:app
}

upgrade() {
  echo "upgrade db"
  exec python manage.py db upgrade
}


case "$1" in
  celery_worker)
    shift
    celery_worker
    ;;
  celery_beat)
    shift
    celery_beat
    ;;
  server)
    shift
    server
    ;;
  upgrade)
    upgrade
    ;;
  debug)
    export FLASK_DEBUG=1
    export REMOTE_DEBUG=1
    exec python manage.py runserver --debugger --no-reload -h 0.0.0.0
    ;;
  shell)
    exec python manage.py shell
    ;;
  manage)
    shift
    exec python manage.py $*
    ;;
  *)
    exec "$@"
    ;;
esac
