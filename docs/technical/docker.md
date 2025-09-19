---
title: Docker
description: Master containerization with Docker for modern application deployment
---

# Docker

Docker revolutionized how we package, distribute, and run applications. As a platform engineer, understanding Docker is essential for building modern infrastructure.

## 📚 Top Learning Resources

### 🎥 Video Courses

#### **Docker Tutorial for Beginners - Full Course**
- **Channel**: TechWorld with Nana
- **Link**: [YouTube - 3 hours](https://www.youtube.com/watch?v=3c-iBn73dDE)
- **Why it's great**: Perfect balance of theory and hands-on practice

#### **Docker Crash Course Tutorial**
- **Channel**: NetworkChuck
- **Link**: [YouTube - 1 hour](https://www.youtube.com/watch?v=eGz9DS-aIeY)
- **Why it's great**: Entertaining and fast-paced introduction

#### **Docker Deep Dive**
- **Channel**: Nigel Poulton
- **Link**: [Pluralsight Course](https://www.pluralsight.com/courses/docker-deep-dive-update)
- **Why it's great**: Comprehensive coverage by Docker Captain

### 📖 Essential Documentation

#### **Docker Official Documentation**
- **Link**: [docs.docker.com](https://docs.docker.com/)
- **Why it's great**: Always up-to-date, includes best practices

#### **Docker Best Practices**
- **Link**: [docs.docker.com/develop/dev-best-practices/](https://docs.docker.com/develop/dev-best-practices/)
- **Why it's great**: Official recommendations for production use

#### **Dockerfile Reference**
- **Link**: [docs.docker.com/engine/reference/builder/](https://docs.docker.com/engine/reference/builder/)
- **Why it's great**: Complete reference for writing Dockerfiles

### 📝 Must-Read Blogs & Articles

#### **Docker Blog - Engineering Posts**
- **Link**: [docker.com/blog/tag/engineering/](https://www.docker.com/blog/tag/engineering/)
- **Why it's great**: Deep technical insights from Docker engineers

#### **Container Security Best Practices**
- **Link**: [snyk.io/blog/10-docker-image-security-best-practices/](https://snyk.io/blog/10-docker-image-security-best-practices/)
- **Why it's great**: Critical security considerations

#### **Julia Evans - How Containers Work**
- **Link**: [jvns.ca/blog/2016/10/10/what-even-is-a-container/](https://jvns.ca/blog/2016/10/10/what-even-is-a-container/)
- **Why it's great**: Demystifies container internals

### 🎓 Structured Courses

#### **Docker Mastery: with Kubernetes +Swarm**
- **Instructor**: Bret Fisher (Docker Captain)
- **Platform**: Udemy
- **Link**: [udemy.com/course/docker-mastery/](https://www.udemy.com/course/docker-mastery/)
- **Why it's great**: Comprehensive, regularly updated, great community

#### **Play with Docker Classroom**
- **Link**: [training.play-with-docker.com](https://training.play-with-docker.com/)
- **Cost**: Free
- **Why it's great**: Browser-based labs, no installation required

### 🔧 Interactive Labs

#### **Play with Docker**
- **Link**: [play-with-docker.com](https://play-with-docker.com/)
- **Why it's great**: Free 4-hour sessions in browser

#### **KillerCoda Docker Scenarios**
- **Link**: [killercoda.com/docker](https://killercoda.com/docker)
- **Why it's great**: Guided scenarios with real environments

## 🎯 Key Concepts to Master

### Container Fundamentals
- Containers vs Virtual Machines
- Docker architecture (daemon, client, registry)
- Container lifecycle
- Namespaces and cgroups
- Union filesystems

### Images & Dockerfiles
```dockerfile
# Multi-stage build example
FROM golang:1.19 AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o app

FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /app/app .
CMD ["./app"]
```

### Essential Commands
```bash
# Container Management
docker run -d -p 80:80 --name web nginx
docker ps -a
docker logs -f container_name
docker exec -it container_name /bin/bash
docker stop/start/restart container_name
docker rm container_name

# Image Management
docker build -t myapp:v1 .
docker images
docker pull image:tag
docker push image:tag
docker rmi image:tag

# Volumes & Networks
docker volume create mydata
docker network create mynet
docker run -v mydata:/data --network mynet app

# Docker Compose
docker-compose up -d
docker-compose down
docker-compose logs -f service_name
```

### Docker Compose
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "80:80"
    environment:
      - NODE_ENV=production
    depends_on:
      - db
  db:
    image: postgres:14
    volumes:
      - db-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=secret
volumes:
  db-data:
```

### Container Security
- Run as non-root user
- Scan images for vulnerabilities
- Use minimal base images (alpine, distroless)
- Don't store secrets in images
- Use read-only root filesystem
- Limit resources (CPU, memory)

## 💡 Interview Tips

### Common Interview Questions

1. **Explain Docker architecture**
   - Client-server architecture
   - Docker daemon, REST API, CLI
   - Images, containers, registries

2. **What's the difference between CMD and ENTRYPOINT?**
   - ENTRYPOINT: defines executable
   - CMD: provides default arguments
   - CMD can be overridden, ENTRYPOINT harder to override

3. **How do you optimize Docker image size?**
   - Multi-stage builds
   - Minimal base images
   - Combine RUN commands
   - Remove unnecessary files
   - Use .dockerignore

4. **Explain Docker networking modes**
   - Bridge: default, isolated network
   - Host: shares host network
   - None: no networking
   - Overlay: multi-host networking

5. **How do you handle persistent data?**
   - Volumes: managed by Docker
   - Bind mounts: host filesystem
   - tmpfs mounts: memory only

### Practical Scenarios
- "Containerize a multi-tier application"
- "Debug a container that won't start"
- "Implement a CI/CD pipeline with Docker"
- "Optimize a slow Docker build"
- "Secure a containerized application"

## 🏆 Hands-On Practice

### Build These Projects

1. **Multi-Stage Build Pipeline**
   - Create optimized images for different languages
   - Implement build caching strategies
   - Compare image sizes

2. **Microservices with Docker Compose**
   - Build a complete application stack
   - Implement service discovery
   - Add monitoring and logging

3. **Container Security Scanner**
   - Integrate vulnerability scanning
   - Implement security policies
   - Automate compliance checks

4. **Docker Registry**
   - Set up private registry
   - Implement authentication
   - Configure garbage collection

### Advanced Topics to Explore
- **BuildKit**: Next-gen image building
- **Docker Swarm**: Native orchestration
- **Container runtimes**: containerd, CRI-O
- **OCI standards**: Image and runtime specs

## 📊 Learning Path

### Week 1: Fundamentals
- Install Docker
- Run first containers
- Basic commands
- Understanding images

### Week 2: Dockerfile Mastery
- Write efficient Dockerfiles
- Multi-stage builds
- Best practices
- Image optimization

### Week 3: Networking & Storage
- Docker networks
- Volumes and bind mounts
- Container communication
- Data persistence

### Week 4: Docker Compose & Production
- Multi-container applications
- Environment management
- Security hardening
- Monitoring and logging

## Docker Compose

Docker Compose is a tool for defining and running multi-container Docker applications. It uses YAML files to configure application services and enables you to create and start all services with a single command.

### Key Features

- **Multi-Container Applications**: Define complex applications with multiple services
- **Declarative Configuration**: YAML-based service definitions
- **Environment Management**: Different configurations for dev, staging, production
- **Service Dependencies**: Define startup order and dependencies
- **Volume and Network Management**: Shared storage and networking

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
  postgres_data:
```

### Environment-Specific Configurations

```yaml
# docker-compose.override.yml (development)
version: '3.8'

services:
  web:
    environment:
      - DEBUG=true
      - LOG_LEVEL=debug
    volumes:
      - .:/app  # Enable hot reload

# docker-compose.prod.yml (production)
version: '3.8'

services:
  web:
    environment:
      - DEBUG=false
      - LOG_LEVEL=info
    restart: unless-stopped
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
```

### Advanced Compose Features

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.prod
      args:
        - NODE_ENV=production
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  nginx:
    image: nginx:alpine
    configs:
      - source: nginx_config
        target: /etc/nginx/nginx.conf
    secrets:
      - ssl_cert
      - ssl_key

configs:
  nginx_config:
    file: ./nginx.conf

secrets:
  ssl_cert:
    file: ./ssl/cert.pem
  ssl_key:
    file: ./ssl/key.pem

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true
```

### Common Compose Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f service_name

# Scale services
docker-compose up -d --scale web=3

# Build services
docker-compose build

# Execute commands in running containers
docker-compose exec web bash

# Environment-specific deployment
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

**Next Steps**: After mastering Docker and Compose, dive into [Kubernetes](/technical/kubernetes) to orchestrate containers at scale.