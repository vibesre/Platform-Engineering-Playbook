# Docker Compose

## Overview

Docker Compose is a tool for defining and running multi-container Docker applications. It uses YAML files to configure application services and enables you to create and start all services with a single command.

## Key Features

- **Multi-Container Applications**: Define complex applications with multiple services
- **Declarative Configuration**: YAML-based service definitions
- **Environment Management**: Different configurations for dev, staging, production
- **Service Dependencies**: Define startup order and dependencies
- **Volume and Network Management**: Shared storage and networking

## Common Use Cases

### Basic Web Application Stack
```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/myapp
    depends_on:
      - db
      - redis
    volumes:
      - .:/app
      - /app/node_modules

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Development Environment
```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DEBUG=app:*
    volumes:
      - .:/usr/src/app
      - /usr/src/app/node_modules
    command: npm run dev

  database:
    image: postgres:15
    environment:
      POSTGRES_DB: myapp_dev
      POSTGRES_USER: developer
      POSTGRES_PASSWORD: devpass
    ports:
      - "5432:5432"
    volumes:
      - dev_db_data:/var/lib/postgresql/data

volumes:
  dev_db_data:
```

### Monitoring Stack
```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards

  node-exporter:
    image: prom/node-exporter:latest
    ports:
      - "9100:9100"
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.ignored-mount-points=^/(sys|proc|dev|host|etc)($$|/)'

volumes:
  prometheus_data:
  grafana_data:
```

## Advanced Configuration

### Environment Variables and Secrets
```yaml
version: '3.8'

services:
  app:
    image: myapp:latest
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - API_KEY_FILE=/run/secrets/api_key
    env_file:
      - .env
      - .env.local
    secrets:
      - api_key
      - db_password

secrets:
  api_key:
    file: ./secrets/api_key.txt
  db_password:
    external: true
```

### Health Checks
```yaml
version: '3.8'

services:
  web:
    image: nginx:alpine
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  api:
    build: .
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
```

### Scaling and Resource Limits
```yaml
version: '3.8'

services:
  worker:
    image: myapp:latest
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
```

## Common Commands

### Basic Operations
```bash
# Start services
docker-compose up
docker-compose up -d  # Detached mode

# Stop services
docker-compose down
docker-compose down -v  # Remove volumes

# Build and start
docker-compose up --build

# Scale services
docker-compose up --scale worker=3

# View logs
docker-compose logs
docker-compose logs -f web  # Follow logs for specific service
```

### Development Workflow
```bash
# Use different compose files
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Run one-off commands
docker-compose exec web bash
docker-compose run --rm web python manage.py migrate

# View service status
docker-compose ps
docker-compose top

# Restart specific service
docker-compose restart web
```

## Production Considerations

### Production Compose File
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  web:
    image: myapp:${TAG:-latest}
    restart: unless-stopped
    environment:
      - NODE_ENV=production
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    deploy:
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M

  nginx:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
```

### CI/CD Integration
```bash
#!/bin/bash
# deploy.sh

set -e

# Build and tag images
docker-compose build
docker-compose push

# Deploy to production
export TAG=${GITHUB_SHA}
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d

# Health check
docker-compose -f docker-compose.prod.yml exec -T web curl -f http://localhost:8000/health
```

## Best Practices

- Use specific image tags instead of `latest`
- Implement health checks for all services
- Use secrets for sensitive data, not environment variables
- Set resource limits to prevent resource exhaustion
- Use multi-stage builds for smaller images
- Implement proper logging configuration
- Use `.env` files for environment-specific configuration
- Version your compose files in source control

## Great Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/) - Official comprehensive documentation
- [Compose File Reference](https://docs.docker.com/compose/compose-file/) - Complete YAML specification
- [Awesome Compose](https://github.com/docker/awesome-compose) - Collection of sample applications
- [Docker Compose Examples](https://github.com/docker/compose/tree/master/docs) - Official examples repository
- [Best Practices Guide](https://docs.docker.com/develop/dev-best-practices/) - Docker development best practices
- [Compose Production](https://docs.docker.com/compose/production/) - Production deployment guidance
- [Docker Compose Override](https://docs.docker.com/compose/extends/) - Environment-specific configurations