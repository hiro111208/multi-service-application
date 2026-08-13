#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

echo "Waiting for services to become healthy..."
for _ in $(seq 1 30); do
  unhealthy="$(docker compose ps --format json | python3 -c "
import json, sys
rows = [json.loads(line) for line in sys.stdin if line.strip()]
print(sum(1 for row in rows if row.get('Health') not in (None, 'healthy')))
")"

  if [ "$unhealthy" -eq 0 ]; then
    docker compose ps
    echo
    echo "All services are healthy."
    exit 0
  fi

  sleep 2
done

echo "Timed out waiting for healthy services:" >&2
docker compose ps >&2
exit 1
