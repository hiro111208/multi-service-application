# Requirements

Create a multi-service application using Docker that consists of the following components:

- **Web Application**: A basic react-based frontend application.

- **API Service**: A Flask-based backend API.

- **Database**: A MongoDB instance for storing application data.

- **Cache**: A Redis cache for improving performance.

- **Reverse Proxy**: An Nginx reverse proxy to handle incoming requests.

Implement the following Docker features and best practices:

- Use Docker Compose to define and run the multi-container application.

- Create custom base images for the web application and API service.

- Implement multi-stage builds for the web application to optimize the final image size.

- Set up a Docker network to allow communication between services.

- Use Docker volumes for persistent data storage (database and cache).

- Implement Docker secrets for sensitive information (e.g., database passwords).

- Configure health checks for each service.

- Optimize Dockerfiles for each service to reduce image sizes and improve build times.

- Implement logging and log rotation for all services.
