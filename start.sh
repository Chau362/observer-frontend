#!/usr/bin/env bash
source venv/bin/activate
gunicorn --log-level=info --access-logfile '/var/log/gunicorn/info.log' --access-logformat '%(t)s "%(r)s" %(s)s %(b)s' --error-logfile '/var/log/gunicorn/info.log' --bind unix:observer.sock src:app
deactivate