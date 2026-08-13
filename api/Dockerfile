# syntax=docker/dockerfile:1

# Custom base image — build first when developing locally:
#   docker build -f docker/Dockerfile.base -t multi-service-api-base .
ARG BASE_IMAGE=multi-service-api-base:latest
FROM ${BASE_IMAGE} AS base

# Install dependencies in a dedicated layer for cache reuse
FROM base AS deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime image
FROM base AS runtime
COPY --from=deps /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin
COPY app ./app
COPY wsgi.py .

ENV FLASK_ENV=production

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl --fail --silent http://127.0.0.1:5000/health || exit 1

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--access-logfile", "-", "--error-logfile", "-", "wsgi:app"]
