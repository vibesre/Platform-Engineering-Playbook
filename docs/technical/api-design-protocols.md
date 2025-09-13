---
title: API Design & Protocols
sidebar_position: 11
---

# API Design & Protocols Deep Dive

Master the art of designing scalable, secure, and developer-friendly APIs. From REST to GraphQL to gRPC, learn the protocols and patterns that power modern distributed systems.

## API Design Fundamentals

### REST API Design Principles

**RESTful Best Practices:**
```yaml
# OpenAPI 3.0 Specification Example
openapi: 3.0.0
info:
  title: Platform API
  version: 1.0.0
  description: Production-grade API design

paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            maximum: 100
            default: 20
      responses:
        200:
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
```

**Resource-Oriented Design:**
```python
# FastAPI implementation with best practices
from fastapi import FastAPI, HTTPException, Query, Depends
from typing import Optional, List
from datetime import datetime
import asyncpg

app = FastAPI(title="Platform API", version="1.0.0")

class UserRepository:
    def __init__(self, db_pool):
        self.db = db_pool
    
    async def get_users(self, offset: int, limit: int, 
                       filters: Optional[dict] = None):
        query = """
            SELECT id, username, email, created_at
            FROM users
            WHERE ($1::jsonb IS NULL OR attributes @> $1::jsonb)
            ORDER BY created_at DESC
            LIMIT $2 OFFSET $3
        """
        return await self.db.fetch(query, filters, limit, offset)

@app.get("/api/v1/users", response_model=UserListResponse)
async def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort: str = Query("created_at", regex="^(created_at|username)$"),
    order: str = Query("desc", regex="^(asc|desc)$"),
    db: asyncpg.Pool = Depends(get_db_pool)
):
    """
    List users with pagination, filtering, and sorting.
    
    - **page**: Page number (starting from 1)
    - **limit**: Number of items per page (max: 100)
    - **sort**: Field to sort by
    - **order**: Sort order (asc/desc)
    """
    offset = (page - 1) * limit
    
    users = await UserRepository(db).get_users(offset, limit)
    total = await UserRepository(db).count_users()
    
    return {
        "data": users,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        },
        "links": {
            "self": f"/api/v1/users?page={page}&limit={limit}",
            "next": f"/api/v1/users?page={page+1}&limit={limit}" if page * limit < total else None,
            "prev": f"/api/v1/users?page={page-1}&limit={limit}" if page > 1 else None
        }
    }
```

### API Versioning Strategies

**URL Path Versioning:**
```nginx
# Nginx configuration for API versioning
location /api/v1/ {
    proxy_pass http://api-v1-backend;
}

location /api/v2/ {
    proxy_pass http://api-v2-backend;
}

# Redirect latest to current version
location /api/latest/ {
    rewrite ^/api/latest/(.*)$ /api/v2/$1 redirect;
}
```

**Header-Based Versioning:**
```python
from fastapi import Header, HTTPException

@app.get("/api/users")
async def get_users_versioned(
    api_version: str = Header(None, alias="X-API-Version")
):
    if api_version == "2.0":
        return await get_users_v2()
    elif api_version == "1.0" or api_version is None:
        return await get_users_v1()
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported API version: {api_version}"
        )
```

**Resources:**
- 📖 [REST API Design Best Practices](https://restfulapi.net/)
- 📚 [API Design Patterns](https://www.oreilly.com/library/view/api-design-patterns/9781617295850/)
- 🎥 [API Design Course](https://www.youtube.com/watch?v=_YlYuNMTCc8)

## GraphQL API Design

### Schema Design

```graphql
# schema.graphql
type Query {
  user(id: ID!): User
  users(
    first: Int = 20
    after: String
    filter: UserFilter
    orderBy: UserOrderBy
  ): UserConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
}

type User implements Node {
  id: ID!
  username: String!
  email: String!
  posts(first: Int, after: String): PostConnection!
  createdAt: DateTime!
  updatedAt: DateTime!
}

# Relay-style pagination
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  cursor: String!
  node: User!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

### GraphQL Implementation

```python
# GraphQL with Strawberry (Python)
import strawberry
from typing import Optional, List
import asyncio
from dataclasses import dataclass

@strawberry.type
class User:
    id: strawberry.ID
    username: str
    email: str
    created_at: datetime
    
    @strawberry.field
    async def posts(self, first: int = 10) -> List["Post"]:
        # N+1 query prevention with DataLoader
        return await post_loader.load(self.id)

@strawberry.type
class Query:
    @strawberry.field
    async def users(
        self,
        first: int = 20,
        after: Optional[str] = None,
        filter: Optional[UserFilter] = None
    ) -> UserConnection:
        # Implement cursor-based pagination
        cursor = decode_cursor(after) if after else 0
        
        users = await db.fetch_users(
            offset=cursor,
            limit=first + 1,  # Fetch one extra to check hasNextPage
            filter=filter
        )
        
        has_next = len(users) > first
        if has_next:
            users = users[:-1]
        
        edges = [
            UserEdge(
                cursor=encode_cursor(cursor + i),
                node=user
            ) for i, user in enumerate(users)
        ]
        
        return UserConnection(
            edges=edges,
            page_info=PageInfo(
                has_next_page=has_next,
                has_previous_page=cursor > 0,
                start_cursor=edges[0].cursor if edges else None,
                end_cursor=edges[-1].cursor if edges else None
            )
        )

# DataLoader for N+1 prevention
class PostLoader(DataLoader):
    async def batch_load_fn(self, user_ids):
        posts = await db.fetch_posts_by_user_ids(user_ids)
        posts_by_user = defaultdict(list)
        for post in posts:
            posts_by_user[post.user_id].append(post)
        return [posts_by_user.get(user_id, []) for user_id in user_ids]
```

**Resources:**
- 📖 [GraphQL Best Practices](https://graphql.org/learn/best-practices/)
- 📚 [Production Ready GraphQL](https://productionreadygraphql.com/)
- 🎥 [GraphQL at Scale](https://www.youtube.com/watch?v=SB3m7wIpBXs)

## gRPC and Protocol Buffers

### Protocol Buffer Definition

```protobuf
// user_service.proto
syntax = "proto3";

package platform.v1;

import "google/protobuf/timestamp.proto";
import "google/protobuf/empty.proto";

service UserService {
  // Unary RPC
  rpc GetUser(GetUserRequest) returns (User) {}
  
  // Server streaming RPC
  rpc ListUsers(ListUsersRequest) returns (stream User) {}
  
  // Client streaming RPC
  rpc CreateUsers(stream CreateUserRequest) returns (CreateUsersResponse) {}
  
  // Bidirectional streaming RPC
  rpc UserChat(stream ChatMessage) returns (stream ChatMessage) {}
}

message User {
  string id = 1;
  string username = 2;
  string email = 3;
  google.protobuf.Timestamp created_at = 4;
  map<string, string> metadata = 5;
}

message GetUserRequest {
  string id = 1;
}

message ListUsersRequest {
  int32 page_size = 1;
  string page_token = 2;
  UserFilter filter = 3;
}

message UserFilter {
  repeated string usernames = 1;
  google.protobuf.Timestamp created_after = 2;
}
```

### gRPC Server Implementation

```python
# gRPC server with interceptors and error handling
import grpc
from concurrent import futures
import logging
from grpc_interceptor import ServerInterceptor
from opentelemetry import trace

class LoggingInterceptor(ServerInterceptor):
    def intercept(self, method, request, context, method_name):
        start_time = time.time()
        try:
            response = method(request, context)
            duration = time.time() - start_time
            logging.info(f"RPC {method_name} completed in {duration:.3f}s")
            return response
        except Exception as e:
            duration = time.time() - start_time
            logging.error(f"RPC {method_name} failed after {duration:.3f}s: {e}")
            raise

class UserServicer(user_service_pb2_grpc.UserServiceServicer):
    def __init__(self, db_pool):
        self.db = db_pool
        self.tracer = trace.get_tracer(__name__)
    
    async def GetUser(self, request, context):
        with self.tracer.start_as_current_span("GetUser"):
            user = await self.db.get_user(request.id)
            if not user:
                context.abort(
                    grpc.StatusCode.NOT_FOUND,
                    f"User {request.id} not found"
                )
            
            return user_pb2.User(
                id=user.id,
                username=user.username,
                email=user.email,
                created_at=user.created_at
            )
    
    async def ListUsers(self, request, context):
        """Server streaming example"""
        async for user in self.db.stream_users(
            page_size=request.page_size,
            filter=request.filter
        ):
            # Check if client is still connected
            if context.is_active():
                yield user_pb2.User(
                    id=user.id,
                    username=user.username,
                    email=user.email
                )
            else:
                break

# Server setup with TLS
def serve():
    server = grpc.aio.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=[LoggingInterceptor()],
        options=[
            ('grpc.max_send_message_length', 50 * 1024 * 1024),
            ('grpc.max_receive_message_length', 50 * 1024 * 1024),
            ('grpc.keepalive_time_ms', 30000),
            ('grpc.keepalive_timeout_ms', 10000),
        ]
    )
    
    user_service_pb2_grpc.add_UserServiceServicer_to_server(
        UserServicer(db_pool), server
    )
    
    # TLS configuration
    with open('server.key', 'rb') as f:
        private_key = f.read()
    with open('server.crt', 'rb') as f:
        certificate_chain = f.read()
    
    server_credentials = grpc.ssl_server_credentials(
        [(private_key, certificate_chain)]
    )
    
    server.add_secure_port('[::]:50051', server_credentials)
    server.start()
    server.wait_for_termination()
```

**Resources:**
- 📖 [gRPC Documentation](https://grpc.io/docs/)
- 📚 [gRPC Up and Running](https://www.oreilly.com/library/view/grpc-up-and/9781492058328/)
- 🎥 [Protocol Buffers Crash Course](https://www.youtube.com/watch?v=46O73On0gyI)

## API Gateway Patterns

### Kong Gateway Configuration

```yaml
# kong.yml - Declarative configuration
_format_version: "2.1"

services:
  - name: user-service
    url: http://user-service.internal:8080
    retries: 3
    connect_timeout: 5000
    write_timeout: 60000
    read_timeout: 60000

routes:
  - name: user-routes
    service: user-service
    paths:
      - /api/v1/users
    strip_path: false

plugins:
  - name: rate-limiting
    service: user-service
    config:
      minute: 100
      hour: 5000
      policy: redis
      redis_host: redis.internal

  - name: jwt
    service: user-service
    config:
      secret_is_base64: false
      claims_to_verify:
        - exp
        - nbf

  - name: cors
    service: user-service
    config:
      origins:
        - https://app.example.com
      methods:
        - GET
        - POST
        - PUT
        - DELETE
      headers:
        - Accept
        - Authorization
        - Content-Type
      credentials: true
      max_age: 3600

  - name: prometheus
    config:
      per_consumer: true
```

### API Gateway Implementation

```python
# Custom API Gateway with FastAPI
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx
import asyncio
from circuit_breaker import CircuitBreaker

class APIGateway:
    def __init__(self):
        self.app = FastAPI(title="API Gateway")
        self.client = httpx.AsyncClient()
        self.circuit_breakers = {}
        self.rate_limiters = {}
        self.setup_routes()
    
    def setup_routes(self):
        @self.app.middleware("http")
        async def add_common_headers(request: Request, call_next):
            start_time = time.time()
            
            # Add request ID for tracing
            request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
            request.state.request_id = request_id
            
            response = await call_next(request)
            
            # Add common response headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Response-Time"] = str(time.time() - start_time)
            
            return response
        
        @self.app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
        async def gateway_handler(request: Request, path: str):
            # Route to appropriate service
            service = self.get_service_for_path(path)
            
            # Check rate limit
            if not await self.check_rate_limit(request, service):
                raise HTTPException(status_code=429, detail="Rate limit exceeded")
            
            # Get circuit breaker for service
            cb = self.get_circuit_breaker(service)
            
            try:
                # Forward request with circuit breaker
                response = await cb.call(
                    self.forward_request, request, service, path
                )
                return response
            except Exception as e:
                return JSONResponse(
                    status_code=503,
                    content={"error": "Service unavailable", "detail": str(e)}
                )
    
    async def forward_request(self, request, service, path):
        # Build upstream URL
        upstream_url = f"{service['url']}/{path}"
        
        # Forward request with timeout
        response = await self.client.request(
            method=request.method,
            url=upstream_url,
            headers=dict(request.headers),
            content=await request.body(),
            timeout=30.0
        )
        
        return JSONResponse(
            content=response.json(),
            status_code=response.status_code,
            headers=dict(response.headers)
        )
```

## WebSocket and Real-time APIs

### WebSocket Server Implementation

```python
# WebSocket with FastAPI
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_rooms: Dict[str, Set[str]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
    
    async def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        
        # Remove from all rooms
        for room in list(self.user_rooms.get(user_id, [])):
            await self.leave_room(user_id, room)
    
    async def join_room(self, user_id: str, room: str):
        if user_id not in self.user_rooms:
            self.user_rooms[user_id] = set()
        self.user_rooms[user_id].add(room)
    
    async def broadcast_to_room(self, room: str, message: dict, exclude: str = None):
        # Find all users in room
        tasks = []
        for user_id, rooms in self.user_rooms.items():
            if room in rooms and user_id != exclude:
                if user_id in self.active_connections:
                    websocket = self.active_connections[user_id]
                    tasks.append(websocket.send_json(message))
        
        # Send concurrently
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

manager = ConnectionManager()

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_json()
            
            # Handle different message types
            if data["type"] == "join_room":
                await manager.join_room(user_id, data["room"])
                await websocket.send_json({
                    "type": "room_joined",
                    "room": data["room"]
                })
            
            elif data["type"] == "message":
                # Broadcast to room
                await manager.broadcast_to_room(
                    data["room"],
                    {
                        "type": "message",
                        "user_id": user_id,
                        "message": data["message"],
                        "timestamp": datetime.utcnow().isoformat()
                    },
                    exclude=user_id
                )
    
    except WebSocketDisconnect:
        await manager.disconnect(user_id)
```

### Server-Sent Events (SSE)

```python
# SSE implementation for real-time updates
from fastapi import FastAPI
from sse_starlette.sse import EventSourceResponse
import asyncio

@app.get("/events/{channel}")
async def event_stream(channel: str):
    async def event_generator():
        # Subscribe to Redis pub/sub or other event source
        pubsub = redis_client.pubsub()
        await pubsub.subscribe(channel)
        
        try:
            while True:
                message = await pubsub.get_message(timeout=1.0)
                if message and message['type'] == 'message':
                    yield {
                        "event": "update",
                        "data": message['data'].decode('utf-8'),
                        "id": str(uuid.uuid4()),
                        "retry": 30000
                    }
                
                # Send heartbeat every 30 seconds
                yield {
                    "event": "heartbeat",
                    "data": "ping"
                }
                
                await asyncio.sleep(0.1)
        finally:
            await pubsub.unsubscribe(channel)
    
    return EventSourceResponse(event_generator())
```

## API Security Best Practices

### Authentication & Authorization

```python
# OAuth2 + JWT implementation
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

class AuthHandler:
    def __init__(self):
        self.secret = os.getenv("JWT_SECRET")
        self.algorithm = "HS256"
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
    
    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire, "iat": datetime.utcnow()})
        
        return jwt.encode(to_encode, self.secret, algorithm=self.algorithm)
    
    async def get_current_user(self, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        
        user = await get_user(user_id)
        if user is None:
            raise credentials_exception
        
        return user

# API key authentication for service-to-service
class APIKeyAuth:
    def __init__(self, api_key_header: str = "X-API-Key"):
        self.api_key_header = api_key_header
    
    async def __call__(self, request: Request) -> str:
        api_key = request.headers.get(self.api_key_header)
        if not api_key:
            raise HTTPException(
                status_code=401,
                detail="API key required"
            )
        
        # Validate API key
        key_data = await validate_api_key(api_key)
        if not key_data:
            raise HTTPException(
                status_code=401,
                detail="Invalid API key"
            )
        
        # Check rate limits for this key
        if not await check_rate_limit(api_key):
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded"
            )
        
        return key_data
```

### Input Validation and Sanitization

```python
# Request validation with Pydantic
from pydantic import BaseModel, validator, Field
from typing import Optional, List
import re

class CreateUserRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, regex="^[a-zA-Z0-9_]+$")
    email: EmailStr
    password: str = Field(..., min_length=8)
    age: int = Field(..., ge=13, le=120)
    tags: List[str] = Field(default_factory=list, max_items=10)
    
    @validator('password')
    def validate_password(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain digit')
        return v
    
    @validator('tags', each_item=True)
    def validate_tags(cls, v):
        if len(v) > 20:
            raise ValueError('Tag too long')
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Invalid tag format')
        return v.lower()

# SQL injection prevention
class SafeQueryBuilder:
    def __init__(self, db_connection):
        self.db = db_connection
    
    async def find_users(self, filters: dict):
        # Use parameterized queries
        query = """
            SELECT * FROM users
            WHERE 1=1
        """
        params = []
        param_count = 1
        
        if 'username' in filters:
            query += f" AND username = ${param_count}"
            params.append(filters['username'])
            param_count += 1
        
        if 'email' in filters:
            query += f" AND email = ${param_count}"
            params.append(filters['email'])
            param_count += 1
        
        # Never use string interpolation for user input!
        return await self.db.fetch(query, *params)
```

## Performance Optimization

### Response Caching

```python
# Redis-based response caching
from functools import wraps
import hashlib
import pickle

class CacheManager:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def cache_response(self, ttl=300, key_prefix="api"):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Generate cache key
                cache_key = self._generate_cache_key(
                    key_prefix, func.__name__, args, kwargs
                )
                
                # Try to get from cache
                cached = await self.redis.get(cache_key)
                if cached:
                    return pickle.loads(cached)
                
                # Call function
                result = await func(*args, **kwargs)
                
                # Cache result
                await self.redis.setex(
                    cache_key, ttl, pickle.dumps(result)
                )
                
                return result
            return wrapper
        return decorator
    
    def _generate_cache_key(self, prefix, func_name, args, kwargs):
        # Create deterministic key from function arguments
        key_parts = [prefix, func_name]
        
        # Add positional arguments
        for arg in args:
            if hasattr(arg, '__dict__'):
                # Skip object arguments (like self)
                continue
            key_parts.append(str(arg))
        
        # Add keyword arguments
        for k, v in sorted(kwargs.items()):
            key_parts.append(f"{k}:{v}")
        
        key_string = ":".join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()

# Usage
@cache_response(ttl=3600)
async def get_user_profile(user_id: str):
    # Expensive operation
    return await fetch_user_with_relations(user_id)
```

### Connection Pooling

```python
# Database connection pooling
import asyncpg
from contextlib import asynccontextmanager

class DatabasePool:
    def __init__(self, dsn: str, min_size=10, max_size=20):
        self.dsn = dsn
        self.min_size = min_size
        self.max_size = max_size
        self._pool = None
    
    async def connect(self):
        self._pool = await asyncpg.create_pool(
            self.dsn,
            min_size=self.min_size,
            max_size=self.max_size,
            max_queries=50000,
            max_inactive_connection_lifetime=300,
            command_timeout=60
        )
    
    async def disconnect(self):
        if self._pool:
            await self._pool.close()
    
    @asynccontextmanager
    async def acquire(self):
        async with self._pool.acquire() as connection:
            async with connection.transaction():
                yield connection

# HTTP connection pooling
class HTTPClientPool:
    def __init__(self):
        self.client = httpx.AsyncClient(
            limits=httpx.Limits(
                max_keepalive_connections=20,
                max_connections=100,
                keepalive_expiry=30
            ),
            timeout=httpx.Timeout(30.0),
            transport=httpx.AsyncHTTPTransport(
                retries=3
            )
        )
```

## API Testing Strategies

### Contract Testing

```python
# Pact contract testing
from pact import Consumer, Provider

pact = Consumer('UserService').has_pact_with(Provider('AuthService'))

@pytest.fixture
def client():
    pact.start_service()
    yield TestClient(app)
    pact.stop_service()

def test_user_authentication(client):
    expected = {
        'id': '123',
        'username': 'testuser',
        'token': pact.like('jwt-token-here')
    }
    
    (pact
     .given('User exists')
     .upon_receiving('a request for authentication')
     .with_request('post', '/auth/login', 
                  body={'username': 'testuser', 'password': 'password'})
     .will_respond_with(200, body=expected))
    
    with pact:
        response = client.post('/auth/login', 
                             json={'username': 'testuser', 'password': 'password'})
        assert response.status_code == 200
        assert response.json()['username'] == 'testuser'
```

### Load Testing

```python
# Locust load testing
from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Login once
        response = self.client.post("/auth/login", json={
            "username": "testuser",
            "password": "password"
        })
        self.token = response.json()["token"]
        self.client.headers.update({"Authorization": f"Bearer {self.token}"})
    
    @task(3)
    def get_users(self):
        self.client.get("/api/v1/users?limit=20")
    
    @task(1)
    def get_user_detail(self):
        user_id = random.randint(1, 1000)
        self.client.get(f"/api/v1/users/{user_id}")
    
    @task(2)
    def create_user(self):
        self.client.post("/api/v1/users", json={
            "username": f"user_{random.randint(1000, 9999)}",
            "email": f"test{random.randint(1000, 9999)}@example.com"
        })
```

## Interview Questions

### Design Questions
1. Design a rate limiting system for APIs
2. How would you version a public API?
3. Design an API gateway for microservices
4. Create an API for real-time collaboration

### Implementation Questions
1. Implement pagination for REST APIs
2. Handle API authentication and authorization
3. Design error handling for APIs
4. Implement request/response logging

### Troubleshooting
1. Debug slow API response times
2. Handle API versioning migration
3. Resolve CORS issues
4. Fix N+1 query problems in GraphQL

## Essential Resources

### Books
- 📚 [RESTful Web APIs](https://www.oreilly.com/library/view/restful-web-apis/9781449359713/)
- 📚 [Designing Web APIs](https://www.oreilly.com/library/view/designing-web-apis/9781492026914/)
- 📚 [API Design Patterns](https://www.manning.com/books/api-design-patterns)

### Documentation
- 📖 [OpenAPI Specification](https://swagger.io/specification/)
- 📖 [JSON:API Specification](https://jsonapi.org/)
- 📖 [GraphQL Specification](https://spec.graphql.org/)
- 📖 [gRPC Documentation](https://grpc.io/docs/)

### Tools
- 🔧 [Postman](https://www.postman.com/) - API testing
- 🔧 [Insomnia](https://insomnia.rest/) - API client
- 🔧 [Kong](https://konghq.com/) - API gateway
- 🔧 [Swagger](https://swagger.io/) - API documentation

Remember: Good API design is about creating interfaces that are intuitive, consistent, and scalable. Focus on developer experience while ensuring performance and security.