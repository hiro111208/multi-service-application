# Web Service

React + TypeScript frontend built with Vite and served by Nginx in production.

## Local development

```bash
npm install
npm run dev
```

The dev server proxies `/api` requests to `http://localhost:5000` (Flask API).

## Docker

Build the custom base image, then the production image:

```bash
docker build -f docker/Dockerfile.base -t multi-service-web-base .
docker build -t multi-service-web .
docker run --rm -p 8081:80 multi-service-web
```

Open `http://localhost:8081`.
