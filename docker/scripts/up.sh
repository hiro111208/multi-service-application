#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Building custom base images..."
docker build -f "$ROOT_DIR/api/docker/Dockerfile.base" -t multi-service-api-base "$ROOT_DIR/api"
docker build -f "$ROOT_DIR/web/docker/Dockerfile.base" -t multi-service-web-base "$ROOT_DIR/web"

echo "Starting full stack..."
docker compose -f "$ROOT_DIR/docker-compose.yml" up -d --build "$@"

echo "Waiting for services to become healthy..."
sleep 10
docker compose -f "$ROOT_DIR/docker-compose.yml" ps

echo
echo "Stack is ready at http://localhost:${NGINX_HTTP_PORT:-8080}"
