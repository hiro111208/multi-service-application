# Multi-Service Application

A multi-service Docker application with a React frontend, Flask API, MongoDB database, Redis cache, and Nginx reverse proxy.

## Project structure

```
.
├── api/                 # Flask backend service
├── web/                 # React frontend service
├── nginx/               # Nginx reverse proxy configuration
│   └── conf.d/
├── docker-compose.yml   # Full multi-service orchestration
├── docker/
│   ├── mongodb/         # MongoDB entrypoint & healthcheck scripts
│   ├── scripts/         # Compose helper scripts
│   └── secrets/         # Docker secret files (git-ignored)
├── .env.example         # Non-secret configuration template
└── README.md
```

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (Engine 24+ recommended)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2 plugin)

Verify your installation:

```bash
docker --version
docker compose version
```

## Local setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd multi-service-application
   ```

2. **Create your environment file**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` if you need to change ports or service names. Sensitive values (database passwords, API keys) are managed separately via Docker secrets in `docker/secrets/` and will be wired up in a later task.

3. **Create Docker secret files**

   ```bash
   cp docker/secrets/mongodb_password.example docker/secrets/mongodb_password
   cp docker/secrets/api_secret_key.example docker/secrets/api_secret_key
   ```

   Edit both files with strong values. Secret files are mounted at `/run/secrets/` inside containers and must not be committed to git.

   | Secret file | Mounted in | Used by |
   |-------------|------------|---------|
   | `mongodb_password` | mongodb, api | MongoDB root password |
   | `api_secret_key` | api | Flask `SECRET_KEY` |

4. **Build custom base images** (required before first compose build)

   ```bash
   docker build -f api/docker/Dockerfile.base -t multi-service-api-base ./api
   docker build -f web/docker/Dockerfile.base -t multi-service-web-base ./web
   ```

   Or use the helper script to build bases and start the stack:

   ```bash
   chmod +x docker/scripts/up.sh
   ./docker/scripts/up.sh
   ```

## Running the application

Start the full stack:

```bash
docker compose up -d --build
```

Open the app at `http://localhost:8080` (or the port set in `.env`).

### Service orchestration

| Service | Hostname | Depends on | Host port |
|---------|----------|------------|-----------|
| mongodb | `mongodb` | — | — |
| redis | `redis` | — | — |
| api | `api` | mongodb, redis (healthy) | — |
| web | `web` | — | — |
| nginx | `nginx` | web, api (healthy) | `${NGINX_HTTP_PORT}` |

All services share the `app-network` bridge network. Only nginx is exposed to the host.

Verify routing through Nginx:

```bash
curl -s http://localhost:8080/health
curl -s http://localhost:8080/api/health
curl -s http://localhost:8080/api/ready
```

Check that all containers are healthy:

```bash
docker compose ps
# or wait until every service reports healthy
./docker/scripts/wait-healthy.sh
```

### Health checks

| Service | Dockerfile `HEALTHCHECK` | Compose health check |
|---------|--------------------------|----------------------|
| web | `GET /health` | `GET /health` |
| api | `GET /health` | `GET /health` |
| mongodb | — | authenticated `mongosh ping` |
| redis | — | `redis-cli ping` |
| nginx | — | `GET /health` |

### Logging

All services use the `json-file` logging driver with rotation (`max-size: 10m`, `max-file: 3`). Application processes write to stdout/stderr so Docker can capture logs:

| Service | Log destination |
|---------|-----------------|
| api | Gunicorn access/error → stdout/stderr |
| web | Nginx access → stdout, errors → stderr |
| nginx | Nginx access → stdout, errors → stderr |
| mongodb, redis | Process stdout/stderr |

Inspect logs:

```bash
# All services (follow)
docker compose logs -f

# Single service
docker compose logs -f api
docker compose logs -f nginx

# Recent lines
docker compose logs --tail=100 api
```

### Integration validation

Run the full validation suite (stack health, Nginx routing, MongoDB persistence, Redis caching, port exposure):

```bash
./docker/scripts/validate.sh
```

### Optimization

Production images use multi-stage builds with BuildKit cache mounts for dependency layers:

| Image | Base | Approx. size |
|-------|------|--------------|
| `multi-service-web` | `nginx:1.27-alpine` | ~76 MB |
| `multi-service-api` | `python:3.12-slim` | ~255 MB |

Confirm a clean reproducible build:

```bash
./docker/scripts/rebuild.sh
```

### Automated testing

```bash
# Unit & integration tests (API + Web)
./scripts/test.sh

# End-to-end stack validation (requires Docker)
./docker/scripts/validate.sh
```

Useful commands:

```bash
# Run in the background
docker compose up --build -d

# View logs
docker compose logs -f

# Stop and remove containers
docker compose down

# Stop and remove containers, volumes, and networks
docker compose down -v
```

## Architecture

| Service       | Technology | Role                              |
|---------------|------------|-----------------------------------|
| Web           | React      | Frontend UI                       |
| API           | Flask      | Backend REST API                  |
| Database      | MongoDB    | Persistent application data       |
| Cache         | Redis      | Performance caching               |
| Reverse proxy | Nginx      | Single public entry point         |

See [docs/requirements/requirements.md](docs/requirements/requirements.md) for full requirements and [docs/tasks/tasks.md](docs/tasks/tasks.md) for the implementation checklist.
