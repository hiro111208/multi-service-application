#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

PORT="${NGINX_HTTP_PORT:-8080}"
BASE_URL="http://localhost:${PORT}"
PASS=0
FAIL=0

pass() {
  echo "✓ $1"
  PASS=$((PASS + 1))
}

fail() {
  echo "✗ $1" >&2
  FAIL=$((FAIL + 1))
}

echo "=== Integration validation ==="
echo

# 1. Full stack is up and healthy
if docker compose ps --format json | python3 -c "
import json, sys
rows = [json.loads(line) for line in sys.stdin if line.strip()]
required = {'mongodb', 'redis', 'api', 'web', 'nginx'}
running = {row['Service'] for row in rows if row.get('State') == 'running'}
missing = required - running
unhealthy = [row['Service'] for row in rows if row.get('Health') not in (None, 'healthy')]
if missing:
    print(f'missing services: {missing}')
    sys.exit(1)
if unhealthy:
    print(f'unhealthy services: {unhealthy}')
    sys.exit(1)
"; then
  pass "All 5 services running and healthy"
else
  fail "Not all services are running and healthy"
fi

# 2. Frontend loads through Nginx
if curl -sf "${BASE_URL}/" | grep -q '<div id="root">'; then
  pass "Frontend loads through Nginx (${BASE_URL}/)"
else
  fail "Frontend did not load through Nginx"
fi

# 3. API requests through Nginx
HEALTH="$(curl -sf "${BASE_URL}/api/health")"
if echo "$HEALTH" | grep -q '"status":"ok"'; then
  pass "API /api/health returns expected data"
else
  fail "API /api/health unexpected response: ${HEALTH}"
fi

READY="$(curl -sf "${BASE_URL}/api/ready")"
if echo "$READY" | grep -q '"mongodb":"ok"' && echo "$READY" | grep -q '"redis":"ok"'; then
  pass "API /api/ready confirms MongoDB and Redis connectivity"
else
  fail "API /api/ready unexpected response: ${READY}"
fi

ITEM_NAME="integration-test-$(date +%s)"
CREATE="$(curl -sf -X POST "${BASE_URL}/api/items" \
  -H 'Content-Type: application/json' \
  -d "{\"name\":\"${ITEM_NAME}\"}")"
if echo "$CREATE" | grep -q "\"name\":\"${ITEM_NAME}\""; then
  pass "API POST /api/items creates data via Nginx"
else
  fail "API POST /api/items failed: ${CREATE}"
fi

ITEMS="$(curl -sf "${BASE_URL}/api/items")"
if echo "$ITEMS" | grep -q "${ITEM_NAME}"; then
  pass "API GET /api/items returns created item"
else
  fail "API GET /api/items missing created item"
fi

# 4. MongoDB persistence across API restart
docker compose restart api >/dev/null
sleep 8
ITEMS_AFTER="$(curl -sf "${BASE_URL}/api/items")"
if echo "$ITEMS_AFTER" | grep -q "${ITEM_NAME}"; then
  pass "MongoDB data persists after API container restart"
else
  fail "MongoDB data lost after API restart"
fi

# 5. Redis cache behavior
docker compose exec -T redis redis-cli DEL items:all >/dev/null
FIRST="$(curl -sf "${BASE_URL}/api/items")"
if docker compose exec -T redis redis-cli EXISTS items:all | grep -q '^1$'; then
  pass "Redis cache populated on GET /api/items (cache miss → set)"
else
  fail "Redis cache key items:all not set after first GET"
fi

TTL="$(docker compose exec -T redis redis-cli TTL items:all | tr -d '\r\n')"
if [ "$TTL" -gt 0 ] 2>/dev/null; then
  pass "Redis cache TTL is active (${TTL}s remaining)"
else
  fail "Redis cache TTL not set (got: ${TTL})"
fi

docker compose exec -T redis redis-cli DEL items:all >/dev/null
curl -sf "${BASE_URL}/api/items" >/dev/null
if docker compose exec -T redis redis-cli EXISTS items:all | grep -q '^1$'; then
  pass "Redis cache repopulated after invalidation"
else
  fail "Redis cache not repopulated after DEL"
fi

# 6. Only Nginx exposes host ports
EXPOSED="$(docker compose ps --format json | python3 -c "
import json, sys
rows = [json.loads(line) for line in sys.stdin if line.strip()]
for row in rows:
    ports = row.get('Publishers') or []
    published = [p for p in ports if p.get('PublishedPort')]
    if published and row['Service'] != 'nginx':
        print(row['Service'])
")"
if [ -z "$EXPOSED" ]; then
  NGINX_PORT="$(docker compose ps --format json | python3 -c "
import json, sys
for row in map(json.loads, sys.stdin):
    if row['Service'] == 'nginx':
        pubs = row.get('Publishers') or []
        print(next((p['PublishedPort'] for p in pubs if p.get('PublishedPort')), ''))
")"
  pass "Only nginx exposes a host port (:${NGINX_PORT})"
else
  fail "Unexpected host port exposure: ${EXPOSED}"
fi

echo
echo "=== Results: ${PASS} passed, ${FAIL} failed ==="
[ "$FAIL" -eq 0 ]
