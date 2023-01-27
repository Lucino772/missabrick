#!/usr/bin/env bash

if [ -n "$MISSABRICK_CELERY_WORKER" ]; then
    celery -A missabrick worker -B -l INFO
else
    gunicorn missabrick.wsgi -b 0.0.0.0:8000 --workers 3 & nginx -g "daemon off;"
fi