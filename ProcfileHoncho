web: gunicorn Covid.wsgi --workers 1
celery: celery -A Covid worker --without-heartbeat --without-gossip --without-mingle -l info -P eventlet