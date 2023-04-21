#!/usr/bin/env bash

gunicorn "app:create_app()" -b 0.0.0.0:8000 -w 4 & nginx -g "daemon off;"