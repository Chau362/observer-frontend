#!/usr/bin/env bash
source venv/bin/activate
gunicorn3 --log-level=info --access-logfile '/var/log/gunicorn/access.log' --access-logformat '%(t)s "%(r)s" %(s)s %(b)s' --error-logfile '/var/log/gunicorn/error.log' --bind unix:observer.sock src:app
deactivate