#!/bin/bash

# set -o errexit
# set -o pipefail
# set -o nounset

aerich init -t app.database_schemas.TORTOISE_ORM --src_folder /home/app/web --location /home/app/web/migrations
python  /home/app/web/app/database_populate_fake_data.py

gunicorn --bind 0.0.0.0:8000 app.main:app -k uvicorn.workers.UvicornWorker