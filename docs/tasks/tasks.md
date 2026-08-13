# Tasks

Actionable breakdown of [requirements](../requirements/requirements.md).

---

## 1. Project scaffolding

- [ ] Create root project layout (`web/`, `api/`, `nginx/`, `docker/`, etc.)
- [ ] Add a root `.env.example` for non-secret configuration values
- [ ] Add a root `.gitignore` (node_modules, Python cache, `.env`, build artifacts)
- [ ] Document local setup and startup in `README.md`

---

## 2. Web application (React)

- [ ] Scaffold a basic React frontend (build tooling, entry point, minimal UI)
- [ ] Add a simple page that calls the API and displays the response
- [ ] Create a custom base image Dockerfile for the web service
- [ ] Implement a multi-stage Dockerfile (build stage → minimal runtime/nginx or static server stage)
- [ ] Optimize the web Dockerfile (layer caching, `.dockerignore`, slim final image)
- [ ] Add a Docker health check for the web container

---

## 3. API service (Flask)

- [ ] Scaffold a Flask app with a basic health/readiness endpoint
- [ ] Add at least one API endpoint that reads or writes application data via MongoDB
- [ ] Integrate Redis for caching (e.g., cache API responses or session data)
- [ ] Create a custom base image Dockerfile for the API service
- [ ] Optimize the API Dockerfile (layer caching, `.dockerignore`, slim final image)
- [ ] Add a Docker health check for the API container

---

## 4. Database (MongoDB)

- [ ] Add MongoDB service definition to Docker Compose
- [ ] Configure a named Docker volume for persistent MongoDB data
- [ ] Wire MongoDB credentials via Docker secrets (not plain env vars in compose)
- [ ] Add a Docker health check for the MongoDB container
- [ ] Verify the API can connect to MongoDB on the internal network

---

## 5. Cache (Redis)

- [ ] Add Redis service definition to Docker Compose
- [ ] Configure a named Docker volume for persistent Redis data (if persistence is required)
- [ ] Add a Docker health check for the Redis container
- [ ] Verify the API can connect to Redis on the internal network

---

## 6. Reverse proxy (Nginx)

- [ ] Create Nginx configuration to route traffic:
  - [ ] `/` → web application
  - [ ] `/api` (or equivalent) → Flask API
- [ ] Add Nginx service to Docker Compose
- [ ] Expose only Nginx to the host (single public entry point)
- [ ] Add a Docker health check for the Nginx container

---

## 7. Docker Compose orchestration

- [ ] Create `docker-compose.yml` defining all services: web, api, mongodb, redis, nginx
- [ ] Define a custom Docker network and attach all services to it
- [ ] Configure service dependencies (`depends_on` with health conditions where supported)
- [ ] Map internal service hostnames for inter-service communication
- [ ] Add compose profiles or overrides only if needed for dev vs prod

---

## 8. Docker secrets

- [ ] Create secret files (e.g., MongoDB root password, API secret key)
- [ ] Mount secrets into relevant containers via Docker Compose `secrets`
- [ ] Update API and database startup to read credentials from secret mounts
- [ ] Ensure secrets are excluded from git and documented in `.env.example` / README

---

## 9. Health checks

- [ ] Define `HEALTHCHECK` in each custom Dockerfile (web, api)
- [ ] Define health checks in Compose for infrastructure services (mongodb, redis, nginx)
- [ ] Confirm `docker compose ps` shows all services as healthy after startup

---

## 10. Logging and log rotation

- [ ] Configure Docker logging driver options for all services (e.g., `json-file` with size/file limits)
- [ ] Ensure application logs go to stdout/stderr (12-factor) for Docker to capture
- [ ] Document how to inspect logs (`docker compose logs`) in README

---

## 11. Integration and validation

- [ ] Bring up the full stack with `docker compose up --build`
- [ ] Verify frontend loads through Nginx on the host port
- [ ] Verify API requests succeed through Nginx and return expected data
- [ ] Verify MongoDB data persists across container restarts
- [ ] Verify Redis cache behavior (cache hit/miss or TTL expiry)
- [ ] Confirm no service exposes unnecessary ports to the host

---

## 12. Final optimization pass

- [ ] Review all image sizes (`docker images`) and reduce where possible
- [ ] Review build times and improve layer ordering / cache reuse
- [ ] Run a full teardown and rebuild to confirm reproducible builds
