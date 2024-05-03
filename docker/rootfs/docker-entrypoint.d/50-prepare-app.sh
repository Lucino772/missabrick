#!/bin/sh

flask -A app.app db upgrade
# flask data load
flask -A app.app user demo
