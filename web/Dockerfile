# syntax=docker/dockerfile:1

# Custom base image — build first when developing locally:
#   docker build -f docker/Dockerfile.base -t multi-service-web-base .
ARG BASE_IMAGE=multi-service-web-base:latest
FROM ${BASE_IMAGE} AS base

# Install dependencies in a dedicated layer for cache reuse
FROM base AS deps
COPY package.json package-lock.json ./
RUN npm ci

# Build static assets
FROM base AS build
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NODE_ENV=production
RUN npm run build

# Minimal runtime image serving the production bundle
FROM nginx:1.27-alpine AS runtime

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:80/ || exit 1

EXPOSE 80
