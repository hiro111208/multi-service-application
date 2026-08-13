# Multi-Service Application

A multi-service Docker application with a React frontend, Flask API, MongoDB database, Redis cache, and Nginx reverse proxy.

## Project structure

```
.
├── api/                 # Flask backend service
├── web/                 # React frontend service
├── nginx/               # Nginx reverse proxy configuration
│   └── conf.d/
├── docker/
│   ├── mongodb/         # MongoDB entrypoint & healthcheck scripts
│   └── secrets/         # Docker secret files (git-ignored)
├── docs/
│   ├── requirements/
│   └── tasks/
├── docker-compose.yml   # (added in a later task)
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
   ```

   Edit `docker/secrets/mongodb_password` with a strong password. Secret files must not be committed to git.

4. **Build custom API base image** (required before first compose build)

   ```bash
   docker build -f api/docker/Dockerfile.base -t multi-service-api-base ./api
   ```

## Running the application

Start MongoDB and the API:

```bash
docker compose up -d mongodb api
```

Verify MongoDB connectivity:

```bash
docker compose exec api curl -s http://localhost:5000/ready
```

Once the full stack is complete, start everything with:

```bash
docker compose up --build
```

Then open the app at `http://localhost:8080` (or the port set in `.env`).

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
