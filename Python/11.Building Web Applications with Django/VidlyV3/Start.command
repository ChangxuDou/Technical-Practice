#!/bin/bash
set -e
cd "$(dirname "$0")"
python3 -c 'import sys; assert sys.version_info >= (3,10), "Python 3.10 or newer is required"'
if [ ! -x .venv/bin/python ]; then
  python3 -m venv .venv
fi
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py setup_demo --accounts --only-empty
printf '\nOpen in your browser: http://127.0.0.1:%s/\nDemo accounts: demo / cashier / manager. Password: VidlyDemo!2026\n\n' "${PORT:-8000}"
.venv/bin/python manage.py runserver "127.0.0.1:${PORT:-8000}"
