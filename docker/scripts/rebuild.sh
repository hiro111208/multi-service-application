#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

echo "=== Full teardown ==="
docker compose down -v --remove-orphans

echo
echo "=== Rebuild base images ==="
DOCKER_BUILDKIT=1 docker build -f api/docker/Dockerfile.base -t multi-service-api-base ./api
DOCKER_BUILDKIT=1 docker build -f web/docker/Dockerfile.base -t multi-service-web-base ./web

echo
echo "=== Rebuild and start stack ==="
DOCKER_BUILDKIT=1 docker compose up -d --build

echo
echo "=== Wait for healthy services ==="
"$ROOT_DIR/docker/scripts/wait-healthy.sh"

echo
echo "=== Image sizes ==="
docker images --format 'table {{.Repository}}\t{{.Tag}}\t{{.Size}}' \
  | grep -E 'multi-service|REPOSITORY'

echo
echo "=== Integration validation ==="
"$ROOT_DIR/docker/scripts/validate.sh"

echo
echo "=== Reproducible build confirmed ==="
