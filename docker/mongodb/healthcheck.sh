#!/bin/bash
set -euo pipefail

password="$(tr -d '\n' < /run/secrets/mongodb_password)"

mongosh \
  --username "${MONGO_INITDB_ROOT_USERNAME}" \
  --password "${password}" \
  --authenticationDatabase admin \
  --quiet \
  --eval "db.adminCommand('ping').ok"
