#!/usr/bin/env bash

if [ -n "$MISSABRICK_CELERY_WORKER" ]; then
    gunicorn missabrick.wsgi -b 0.0.0.0:8000 --workers 3 & nginx -g "daemon off;"
else
    celery -A missabrick worker -l INFO
fi