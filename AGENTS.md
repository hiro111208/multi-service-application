# AGENTS

## Architecture

- Backend: Flask
- Frontend: React, TypeScript, Vite
- Database: MongoDB
- Cache: Redis
- Reverse Proxy: Nginx

## Testing

Follow the [testing pyramid](https://martinfowler.com/bliki/TestPyramid.html):

| Layer | Location | Command |
|-------|----------|---------|
| Unit / integration (API) | `api/tests/` | `pytest api/tests` |
| Unit (Web) | `web/src/*.test.*` | `npm --prefix web run test` |
| End-to-end (Docker stack) | `docker/scripts/validate.sh` | `./docker/scripts/validate.sh` |

Run all local automated tests:

```bash
./scripts/test.sh
```
