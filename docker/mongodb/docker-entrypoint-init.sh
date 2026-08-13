#!/bin/bash
set -euo pipefail

export MONGO_INITDB_ROOT_PASSWORD="$(tr -d '\n' < /run/secrets/mongodb_password)"
exec /usr/local/bin/docker-entrypoint.sh "$@"
