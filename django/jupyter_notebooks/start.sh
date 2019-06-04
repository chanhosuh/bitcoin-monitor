#!/bin/bash
# run script from /code in the "django" container

cd "$(dirname "$0")"
jupyter nbextension enable --py widgetsnbextension && manage.py shell_plus --notebook
