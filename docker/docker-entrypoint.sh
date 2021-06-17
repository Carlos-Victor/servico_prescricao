#!/bin/sh
set -e

python /source/manage.py migrate
coverage run --source='.' --omit=manage.py,project_prescription/asgi.py,project_prescription/wsgi.py manage.py test
coverage report -m --fail-under=80

exec "$@"