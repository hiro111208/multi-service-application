# API Service

Flask backend with MongoDB persistence and Redis caching.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness probe |
| GET | `/ready` | Readiness probe (MongoDB + Redis) |
| GET | `/items` | List items (cached in Redis) |
| GET | `/items/<id>` | Get a single item |
| POST | `/items` | Create an item (`{"name": "..."}`) |

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export MONGODB_HOST=localhost
export REDIS_HOST=localhost
export MONGODB_PASSWORD=your-password

flask --app wsgi:app run --debug --port 5000
```

MongoDB and Redis must be running locally for `/ready` and `/items` to work.

## Docker

Build the custom base image, then the production image:

```bash
docker build -f docker/Dockerfile.base -t multi-service-api-base .
docker build -t multi-service-api .
docker run --rm -p 5000:5000 multi-service-api
```

The container expects MongoDB and Redis to be reachable on the Docker network configured via environment variables.
