# gRPC

gRPC is a high-performance, language-agnostic remote procedure call (RPC) framework that uses HTTP/2 for transport and Protocol Buffers as the interface description language.

## Installation

### Protocol Buffers Compiler
```bash
# Install protoc compiler
# macOS
brew install protobuf

# Ubuntu/Debian
sudo apt update
sudo apt install protobuf-compiler

# CentOS/RHEL
sudo yum install protobuf-compiler

# Windows (using Chocolatey)
choco install protoc

# Verify installation
protoc --version
```

### Language-Specific Libraries

#### Python
```bash
# Install gRPC and tools
pip install grpcio grpcio-tools

# For async support
pip install grpcio-status grpcio-reflection

# Development tools
pip install grpcio-testing
```

#### Go
```bash
# Install gRPC
go install google.golang.org/grpc@latest

# Install protoc plugins
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest

# Add to PATH
export PATH="$PATH:$(go env GOPATH)/bin"
```

#### Java
```xml
<!-- Maven dependencies -->
<dependencies>
    <dependency>
        <groupId>io.grpc</groupId>
        <artifactId>grpc-netty-shaded</artifactId>
        <version>1.58.0</version>
    </dependency>
    <dependency>
        <groupId>io.grpc</groupId>
        <artifactId>grpc-protobuf</artifactId>
        <version>1.58.0</version>
    </dependency>
    <dependency>
        <groupId>io.grpc</groupId>
        <artifactId>grpc-stub</artifactId>
        <version>1.58.0</version>
    </dependency>
</dependencies>
```

#### Node.js
```bash
# Install gRPC for Node.js
npm install @grpc/grpc-js @grpc/proto-loader

# TypeScript support
npm install @types/google-protobuf

# Development tools
npm install grpc-tools
```

## Protocol Buffers Definition

### Basic Service Definition
```protobuf
// user_service.proto
syntax = "proto3";

package user;

option go_package = "github.com/example/user-service/pb";

import "google/protobuf/timestamp.proto";
import "google/protobuf/empty.proto";

// User service definition
service UserService {
  // Unary RPC
  rpc GetUser(GetUserRequest) returns (User);
  rpc CreateUser(CreateUserRequest) returns (User);
  rpc UpdateUser(UpdateUserRequest) returns (User);
  rpc DeleteUser(DeleteUserRequest) returns (google.protobuf.Empty);
  
  // Server streaming RPC
  rpc ListUsers(ListUsersRequest) returns (stream User);
  
  // Client streaming RPC
  rpc BulkCreateUsers(stream CreateUserRequest) returns (BulkCreateUsersResponse);
  
  // Bidirectional streaming RPC
  rpc Chat(stream ChatMessage) returns (stream ChatMessage);
}

// Message definitions
message User {
  string id = 1;
  string name = 2;
  string email = 3;
  int32 age = 4;
  repeated string roles = 5;
  google.protobuf.Timestamp created_at = 6;
  google.protobuf.Timestamp updated_at = 7;
  UserStatus status = 8;
  map<string, string> metadata = 9;
}

message GetUserRequest {
  string id = 1;
  repeated string fields = 2; // Field mask
}

message CreateUserRequest {
  string name = 1;
  string email = 2;
  int32 age = 3;
  repeated string roles = 4;
  map<string, string> metadata = 5;
}

message UpdateUserRequest {
  string id = 1;
  User user = 2;
  google.protobuf.FieldMask update_mask = 3;
}

message DeleteUserRequest {
  string id = 1;
}

message ListUsersRequest {
  int32 page_size = 1;
  string page_token = 2;
  string filter = 3;
  string order_by = 4;
}

message BulkCreateUsersResponse {
  repeated User users = 1;
  int32 created_count = 2;
  repeated string errors = 3;
}

message ChatMessage {
  string user_id = 1;
  string message = 2;
  google.protobuf.Timestamp timestamp = 3;
  MessageType type = 4;
}

enum UserStatus {
  UNKNOWN = 0;
  ACTIVE = 1;
  INACTIVE = 2;
  SUSPENDED = 3;
}

enum MessageType {
  TEXT = 0;
  IMAGE = 1;
  FILE = 2;
  SYSTEM = 3;
}
```

### Advanced Features
```protobuf
// advanced_service.proto
syntax = "proto3";

package advanced;

import "google/api/annotations.proto";
import "google/protobuf/field_mask.proto";
import "google/protobuf/wrappers.proto";

// Service with HTTP annotations
service AdvancedService {
  rpc GetResource(GetResourceRequest) returns (Resource) {
    option (google.api.http) = {
      get: "/v1/resources/{id}"
    };
  }
  
  rpc CreateResource(CreateResourceRequest) returns (Resource) {
    option (google.api.http) = {
      post: "/v1/resources"
      body: "*"
    };
  }
  
  rpc UpdateResource(UpdateResourceRequest) returns (Resource) {
    option (google.api.http) = {
      patch: "/v1/resources/{resource.id}"
      body: "resource"
    };
  }
}

message Resource {
  string id = 1;
  string name = 2;
  google.protobuf.StringValue description = 3; // Optional field
  repeated Tag tags = 4;
  oneof content {
    TextContent text = 5;
    ImageContent image = 6;
    FileContent file = 7;
  }
}

message Tag {
  string key = 1;
  string value = 2;
}

message TextContent {
  string text = 1;
  string format = 2; // markdown, html, plain
}

message ImageContent {
  string url = 1;
  int32 width = 2;
  int32 height = 3;
  string alt_text = 4;
}

message FileContent {
  string url = 1;
  string filename = 2;
  int64 size = 3;
  string mime_type = 4;
}

message GetResourceRequest {
  string id = 1;
}

message CreateResourceRequest {
  Resource resource = 1;
}

message UpdateResourceRequest {
  Resource resource = 1;
  google.protobuf.FieldMask update_mask = 2;
}
```

## Code Generation

### Makefile for Code Generation
```makefile
# Makefile
PROTO_DIR = proto
PROTO_FILES = $(wildcard $(PROTO_DIR)/*.proto)

# Go
GO_OUT_DIR = pkg/pb
PROTOC_GO_OPTS = --go_out=$(GO_OUT_DIR) --go_opt=paths=source_relative
PROTOC_GRPC_GO_OPTS = --go-grpc_out=$(GO_OUT_DIR) --go-grpc_opt=paths=source_relative

# Python
PYTHON_OUT_DIR = python/pb
PROTOC_PYTHON_OPTS = --python_out=$(PYTHON_OUT_DIR) --grpc_python_out=$(PYTHON_OUT_DIR)

# JavaScript/TypeScript
JS_OUT_DIR = js/pb
PROTOC_JS_OPTS = --js_out=import_style=commonjs:$(JS_OUT_DIR)
PROTOC_TS_OPTS = --ts_out=service=grpc-web:$(JS_OUT_DIR)

.PHONY: all clean go python js

all: go python js

go: $(GO_OUT_DIR)
	protoc $(PROTOC_GO_OPTS) $(PROTOC_GRPC_GO_OPTS) \
		--proto_path=$(PROTO_DIR) $(PROTO_FILES)

python: $(PYTHON_OUT_DIR)
	python -m grpc_tools.protoc $(PROTOC_PYTHON_OPTS) \
		--proto_path=$(PROTO_DIR) $(PROTO_FILES)

js: $(JS_OUT_DIR)
	protoc $(PROTOC_JS_OPTS) $(PROTOC_TS_OPTS) \
		--proto_path=$(PROTO_DIR) $(PROTO_FILES)

$(GO_OUT_DIR):
	mkdir -p $(GO_OUT_DIR)

$(PYTHON_OUT_DIR):
	mkdir -p $(PYTHON_OUT_DIR)

$(JS_OUT_DIR):
	mkdir -p $(JS_OUT_DIR)

clean:
	rm -rf $(GO_OUT_DIR) $(PYTHON_OUT_DIR) $(JS_OUT_DIR)

# Development helpers
watch:
	@echo "Watching for proto file changes..."
	@while inotifywait -e modify $(PROTO_DIR)/*.proto; do \
		echo "Regenerating code..."; \
		$(MAKE) all; \
	done

validate:
	@for proto in $(PROTO_FILES); do \
		echo "Validating $$proto"; \
		protoc --proto_path=$(PROTO_DIR) --descriptor_set_out=/dev/null $$proto; \
	done
```

### Automated Generation Script
```bash
#!/bin/bash
# generate.sh

set -e

PROTO_DIR="proto"
OUTPUT_DIR="generated"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Check dependencies
check_dependencies() {
    log "Checking dependencies..."
    
    if ! command -v protoc &> /dev/null; then
        error "protoc is not installed"
    fi
    
    if ! command -v protoc-gen-go &> /dev/null; then
        error "protoc-gen-go is not installed"
    fi
    
    if ! command -v protoc-gen-go-grpc &> /dev/null; then
        error "protoc-gen-go-grpc is not installed"
    fi
    
    log "All dependencies are available"
}

# Clean output directory
clean_output() {
    log "Cleaning output directory..."
    rm -rf "${OUTPUT_DIR}"
    mkdir -p "${OUTPUT_DIR}"/{go,python,js}
}

# Generate Go code
generate_go() {
    log "Generating Go code..."
    
    protoc \
        --proto_path="${PROTO_DIR}" \
        --go_out="${OUTPUT_DIR}/go" \
        --go_opt=paths=source_relative \
        --go-grpc_out="${OUTPUT_DIR}/go" \
        --go-grpc_opt=paths=source_relative \
        "${PROTO_DIR}"/*.proto
    
    log "Go code generated successfully"
}

# Generate Python code
generate_python() {
    log "Generating Python code..."
    
    python -m grpc_tools.protoc \
        --proto_path="${PROTO_DIR}" \
        --python_out="${OUTPUT_DIR}/python" \
        --grpc_python_out="${OUTPUT_DIR}/python" \
        "${PROTO_DIR}"/*.proto
    
    # Fix Python imports
    find "${OUTPUT_DIR}/python" -name "*_pb2_grpc.py" -exec sed -i 's/import.*_pb2/from . import &/' {} \;
    
    log "Python code generated successfully"
}

# Generate JavaScript code
generate_js() {
    log "Generating JavaScript code..."
    
    protoc \
        --proto_path="${PROTO_DIR}" \
        --js_out=import_style=commonjs:"${OUTPUT_DIR}/js" \
        --grpc-web_out=import_style=commonjs,mode=grpcwebtext:"${OUTPUT_DIR}/js" \
        "${PROTO_DIR}"/*.proto
    
    log "JavaScript code generated successfully"
}

# Main execution
main() {
    log "Starting code generation..."
    
    check_dependencies
    clean_output
    generate_go
    generate_python
    generate_js
    
    log "Code generation completed successfully!"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --proto-dir)
            PROTO_DIR="$2"
            shift 2
            ;;
        --output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --go-only)
            GENERATE_GO_ONLY=1
            shift
            ;;
        --python-only)
            GENERATE_PYTHON_ONLY=1
            shift
            ;;
        --js-only)
            GENERATE_JS_ONLY=1
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --proto-dir DIR     Proto files directory (default: proto)"
            echo "  --output-dir DIR    Output directory (default: generated)"
            echo "  --go-only          Generate only Go code"
            echo "  --python-only      Generate only Python code"
            echo "  --js-only          Generate only JavaScript code"
            echo "  -h, --help         Show this help message"
            exit 0
            ;;
        *)
            error "Unknown option: $1"
            ;;
    esac
done

main
```

## Server Implementation

### Python Server
```python
import asyncio
import logging
from concurrent import futures
from datetime import datetime
from typing import AsyncIterator, List

import grpc
from grpc import aio
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.empty_pb2 import Empty

# Generated protobuf imports
from pb import user_service_pb2, user_service_pb2_grpc

class UserServiceImpl(user_service_pb2_grpc.UserServiceServicer):
    def __init__(self):
        self.users = {}
        self.next_id = 1
        
    async def GetUser(self, request: user_service_pb2.GetUserRequest, 
                     context: grpc.aio.ServicerContext) -> user_service_pb2.User:
        """Get a user by ID"""
        try:
            if request.id not in self.users:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f'User {request.id} not found')
                return user_service_pb2.User()
            
            user = self.users[request.id]
            
            # Apply field mask if specified
            if request.fields:
                filtered_user = user_service_pb2.User()
                for field in request.fields:
                    if hasattr(user, field):
                        setattr(filtered_user, field, getattr(user, field))
                return filtered_user
            
            return user
            
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_service_pb2.User()
    
    async def CreateUser(self, request: user_service_pb2.CreateUserRequest,
                        context: grpc.aio.ServicerContext) -> user_service_pb2.User:
        """Create a new user"""
        try:
            # Validate request
            if not request.name or not request.email:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details('Name and email are required')
                return user_service_pb2.User()
            
            # Check if email already exists
            for user in self.users.values():
                if user.email == request.email:
                    context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                    context.set_details('User with this email already exists')
                    return user_service_pb2.User()
            
            # Create user
            user_id = str(self.next_id)
            self.next_id += 1
            
            now = Timestamp()
            now.GetCurrentTime()
            
            user = user_service_pb2.User(
                id=user_id,
                name=request.name,
                email=request.email,
                age=request.age,
                roles=list(request.roles),
                created_at=now,
                updated_at=now,
                status=user_service_pb2.UserStatus.ACTIVE
            )
            
            # Copy metadata
            for key, value in request.metadata.items():
                user.metadata[key] = value
            
            self.users[user_id] = user
            logging.info(f"Created user: {user_id}")
            
            return user
            
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_service_pb2.User()
    
    async def UpdateUser(self, request: user_service_pb2.UpdateUserRequest,
                        context: grpc.aio.ServicerContext) -> user_service_pb2.User:
        """Update an existing user"""
        try:
            if request.id not in self.users:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f'User {request.id} not found')
                return user_service_pb2.User()
            
            user = self.users[request.id]
            
            # Update fields based on field mask
            if request.HasField('update_mask'):
                for path in request.update_mask.paths:
                    if hasattr(request.user, path):
                        setattr(user, path, getattr(request.user, path))
            else:
                # Update all fields if no mask specified
                user.CopyFrom(request.user)
                user.id = request.id  # Preserve ID
            
            # Update timestamp
            now = Timestamp()
            now.GetCurrentTime()
            user.updated_at.CopyFrom(now)
            
            logging.info(f"Updated user: {request.id}")
            return user
            
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_service_pb2.User()
    
    async def DeleteUser(self, request: user_service_pb2.DeleteUserRequest,
                        context: grpc.aio.ServicerContext) -> Empty:
        """Delete a user"""
        try:
            if request.id not in self.users:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f'User {request.id} not found')
                return Empty()
            
            del self.users[request.id]
            logging.info(f"Deleted user: {request.id}")
            
            return Empty()
            
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return Empty()
    
    async def ListUsers(self, request: user_service_pb2.ListUsersRequest,
                       context: grpc.aio.ServicerContext) -> AsyncIterator[user_service_pb2.User]:
        """Stream all users"""
        try:
            # Apply filtering and pagination
            users = list(self.users.values())
            
            # Simple filtering by name
            if request.filter:
                users = [u for u in users if request.filter.lower() in u.name.lower()]
            
            # Pagination
            page_size = request.page_size if request.page_size > 0 else 10
            start_idx = 0
            
            if request.page_token:
                try:
                    start_idx = int(request.page_token)
                except ValueError:
                    context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                    context.set_details('Invalid page token')
                    return
            
            end_idx = start_idx + page_size
            page_users = users[start_idx:end_idx]
            
            for user in page_users:
                yield user
                await asyncio.sleep(0.1)  # Simulate streaming delay
                
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
    
    async def BulkCreateUsers(self, request_iterator: AsyncIterator[user_service_pb2.CreateUserRequest],
                             context: grpc.aio.ServicerContext) -> user_service_pb2.BulkCreateUsersResponse:
        """Create multiple users from stream"""
        created_users = []
        errors = []
        
        async for request in request_iterator:
            try:
                # Create user (reuse logic from CreateUser)
                if not request.name or not request.email:
                    errors.append(f"Invalid user data: name={request.name}, email={request.email}")
                    continue
                
                # Check for duplicate email
                email_exists = any(u.email == request.email for u in self.users.values())
                if email_exists:
                    errors.append(f"Email {request.email} already exists")
                    continue
                
                user_id = str(self.next_id)
                self.next_id += 1
                
                now = Timestamp()
                now.GetCurrentTime()
                
                user = user_service_pb2.User(
                    id=user_id,
                    name=request.name,
                    email=request.email,
                    age=request.age,
                    roles=list(request.roles),
                    created_at=now,
                    updated_at=now,
                    status=user_service_pb2.UserStatus.ACTIVE
                )
                
                self.users[user_id] = user
                created_users.append(user)
                
            except Exception as e:
                errors.append(str(e))
        
        return user_service_pb2.BulkCreateUsersResponse(
            users=created_users,
            created_count=len(created_users),
            errors=errors
        )
    
    async def Chat(self, request_iterator: AsyncIterator[user_service_pb2.ChatMessage],
                  context: grpc.aio.ServicerContext) -> AsyncIterator[user_service_pb2.ChatMessage]:
        """Bidirectional streaming chat"""
        # In a real implementation, this would involve a message broker
        # For demo purposes, we'll echo messages back
        
        async for message in request_iterator:
            # Echo the message back with system response
            echo_message = user_service_pb2.ChatMessage(
                user_id="system",
                message=f"Echo: {message.message}",
                timestamp=message.timestamp,
                type=user_service_pb2.MessageType.SYSTEM
            )
            
            yield echo_message
            await asyncio.sleep(0.1)

async def serve():
    """Start the gRPC server"""
    server = aio.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Add services
    user_service_pb2_grpc.add_UserServiceServicer_to_server(UserServiceImpl(), server)
    
    # Configure server
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    
    logging.info(f"Starting server on {listen_addr}")
    await server.start()
    
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        logging.info("Shutting down server...")
        await server.stop(5)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
```

### Go Server
```go
package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"net"
	"sync"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
	"google.golang.org/protobuf/types/known/emptypb"
	"google.golang.org/protobuf/types/known/timestamppb"

	pb "github.com/example/user-service/pb"
)

type UserServer struct {
	pb.UnimplementedUserServiceServer
	mu      sync.RWMutex
	users   map[string]*pb.User
	nextID  int32
}

func NewUserServer() *UserServer {
	return &UserServer{
		users:  make(map[string]*pb.User),
		nextID: 1,
	}
}

func (s *UserServer) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.User, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()

	user, exists := s.users[req.Id]
	if !exists {
		return nil, status.Errorf(codes.NotFound, "user %s not found", req.Id)
	}

	// Apply field mask if specified
	if len(req.Fields) > 0 {
		// In a real implementation, you would use field masks properly
		// This is a simplified version
		filteredUser := &pb.User{Id: user.Id}
		for _, field := range req.Fields {
			switch field {
			case "name":
				filteredUser.Name = user.Name
			case "email":
				filteredUser.Email = user.Email
			case "age":
				filteredUser.Age = user.Age
			}
		}
		return filteredUser, nil
	}

	return user, nil
}

func (s *UserServer) CreateUser(ctx context.Context, req *pb.CreateUserRequest) (*pb.User, error) {
	if req.Name == "" || req.Email == "" {
		return nil, status.Error(codes.InvalidArgument, "name and email are required")
	}

	s.mu.Lock()
	defer s.mu.Unlock()

	// Check if email already exists
	for _, user := range s.users {
		if user.Email == req.Email {
			return nil, status.Error(codes.AlreadyExists, "user with this email already exists")
		}
	}

	// Create new user
	userID := fmt.Sprintf("%d", s.nextID)
	s.nextID++

	now := timestamppb.Now()
	user := &pb.User{
		Id:        userID,
		Name:      req.Name,
		Email:     req.Email,
		Age:       req.Age,
		Roles:     req.Roles,
		CreatedAt: now,
		UpdatedAt: now,
		Status:    pb.UserStatus_ACTIVE,
		Metadata:  req.Metadata,
	}

	s.users[userID] = user
	log.Printf("Created user: %s", userID)

	return user, nil
}

func (s *UserServer) UpdateUser(ctx context.Context, req *pb.UpdateUserRequest) (*pb.User, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	user, exists := s.users[req.Id]
	if !exists {
		return nil, status.Errorf(codes.NotFound, "user %s not found", req.Id)
	}

	// Update fields - in a real implementation, use proper field mask logic
	if req.User.Name != "" {
		user.Name = req.User.Name
	}
	if req.User.Email != "" {
		user.Email = req.User.Email
	}
	if req.User.Age != 0 {
		user.Age = req.User.Age
	}
	if len(req.User.Roles) > 0 {
		user.Roles = req.User.Roles
	}

	user.UpdatedAt = timestamppb.Now()
	log.Printf("Updated user: %s", req.Id)

	return user, nil
}

func (s *UserServer) DeleteUser(ctx context.Context, req *pb.DeleteUserRequest) (*emptypb.Empty, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	if _, exists := s.users[req.Id]; !exists {
		return nil, status.Errorf(codes.NotFound, "user %s not found", req.Id)
	}

	delete(s.users, req.Id)
	log.Printf("Deleted user: %s", req.Id)

	return &emptypb.Empty{}, nil
}

func (s *UserServer) ListUsers(req *pb.ListUsersRequest, stream pb.UserService_ListUsersServer) error {
	s.mu.RLock()
	users := make([]*pb.User, 0, len(s.users))
	for _, user := range s.users {
		users = append(users, user)
	}
	s.mu.RUnlock()

	// Apply filtering
	if req.Filter != "" {
		filteredUsers := make([]*pb.User, 0)
		for _, user := range users {
			if contains(user.Name, req.Filter) {
				filteredUsers = append(filteredUsers, user)
			}
		}
		users = filteredUsers
	}

	// Pagination
	pageSize := int(req.PageSize)
	if pageSize <= 0 {
		pageSize = 10
	}

	startIdx := 0
	// In a real implementation, decode page token properly

	endIdx := startIdx + pageSize
	if endIdx > len(users) {
		endIdx = len(users)
	}

	for i := startIdx; i < endIdx; i++ {
		if err := stream.Send(users[i]); err != nil {
			return err
		}
		time.Sleep(100 * time.Millisecond) // Simulate streaming delay
	}

	return nil
}

func (s *UserServer) BulkCreateUsers(stream pb.UserService_BulkCreateUsersServer) error {
	var createdUsers []*pb.User
	var errors []string

	for {
		req, err := stream.Recv()
		if err == io.EOF {
			// Client finished sending
			break
		}
		if err != nil {
			return err
		}

		// Validate request
		if req.Name == "" || req.Email == "" {
			errors = append(errors, fmt.Sprintf("Invalid user data: name=%s, email=%s", req.Name, req.Email))
			continue
		}

		s.mu.Lock()
		// Check for duplicate email
		emailExists := false
		for _, user := range s.users {
			if user.Email == req.Email {
				emailExists = true
				break
			}
		}

		if emailExists {
			errors = append(errors, fmt.Sprintf("Email %s already exists", req.Email))
			s.mu.Unlock()
			continue
		}

		// Create user
		userID := fmt.Sprintf("%d", s.nextID)
		s.nextID++

		now := timestamppb.Now()
		user := &pb.User{
			Id:        userID,
			Name:      req.Name,
			Email:     req.Email,
			Age:       req.Age,
			Roles:     req.Roles,
			CreatedAt: now,
			UpdatedAt: now,
			Status:    pb.UserStatus_ACTIVE,
			Metadata:  req.Metadata,
		}

		s.users[userID] = user
		createdUsers = append(createdUsers, user)
		s.mu.Unlock()
	}

	response := &pb.BulkCreateUsersResponse{
		Users:        createdUsers,
		CreatedCount: int32(len(createdUsers)),
		Errors:       errors,
	}

	return stream.SendAndClose(response)
}

func (s *UserServer) Chat(stream pb.UserService_ChatServer) error {
	for {
		message, err := stream.Recv()
		if err == io.EOF {
			return nil
		}
		if err != nil {
			return err
		}

		// Echo the message back
		echoMessage := &pb.ChatMessage{
			UserId:    "system",
			Message:   fmt.Sprintf("Echo: %s", message.Message),
			Timestamp: timestamppb.Now(),
			Type:      pb.MessageType_SYSTEM,
		}

		if err := stream.Send(echoMessage); err != nil {
			return err
		}
	}
}

func contains(s, substr string) bool {
	return len(s) >= len(substr) && s[:len(substr)] == substr
}

func main() {
	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("Failed to listen: %v", err)
	}

	server := grpc.NewServer()
	userServer := NewUserServer()

	pb.RegisterUserServiceServer(server, userServer)

	log.Println("Starting gRPC server on :50051")
	if err := server.Serve(lis); err != nil {
		log.Fatalf("Failed to serve: %v", err)
	}
}
```

## Client Implementation

### Python Client
```python
import asyncio
import logging
from typing import List, AsyncIterator

import grpc
from grpc import aio

from pb import user_service_pb2, user_service_pb2_grpc

class UserServiceClient:
    def __init__(self, server_address: str = 'localhost:50051'):
        self.server_address = server_address
        self.channel = None
        self.stub = None
    
    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    async def connect(self):
        """Connect to the gRPC server"""
        self.channel = aio.insecure_channel(self.server_address)
        self.stub = user_service_pb2_grpc.UserServiceStub(self.channel)
        logging.info(f"Connected to gRPC server at {self.server_address}")
    
    async def close(self):
        """Close the connection"""
        if self.channel:
            await self.channel.close()
            logging.info("Closed gRPC connection")
    
    async def get_user(self, user_id: str, fields: List[str] = None) -> user_service_pb2.User:
        """Get a user by ID"""
        request = user_service_pb2.GetUserRequest(
            id=user_id,
            fields=fields or []
        )
        
        try:
            response = await self.stub.GetUser(request)
            return response
        except grpc.RpcError as e:
            logging.error(f"Failed to get user {user_id}: {e.details()}")
            raise
    
    async def create_user(self, name: str, email: str, age: int = 0, 
                         roles: List[str] = None, metadata: dict = None) -> user_service_pb2.User:
        """Create a new user"""
        request = user_service_pb2.CreateUserRequest(
            name=name,
            email=email,
            age=age,
            roles=roles or [],
            metadata=metadata or {}
        )
        
        try:
            response = await self.stub.CreateUser(request)
            logging.info(f"Created user: {response.id}")
            return response
        except grpc.RpcError as e:
            logging.error(f"Failed to create user {name}: {e.details()}")
            raise
    
    async def update_user(self, user_id: str, **kwargs) -> user_service_pb2.User:
        """Update a user"""
        user = user_service_pb2.User(id=user_id)
        
        # Set fields that are provided
        for field, value in kwargs.items():
            if hasattr(user, field):
                setattr(user, field, value)
        
        request = user_service_pb2.UpdateUserRequest(
            id=user_id,
            user=user
        )
        
        try:
            response = await self.stub.UpdateUser(request)
            logging.info(f"Updated user: {user_id}")
            return response
        except grpc.RpcError as e:
            logging.error(f"Failed to update user {user_id}: {e.details()}")
            raise
    
    async def delete_user(self, user_id: str):
        """Delete a user"""
        request = user_service_pb2.DeleteUserRequest(id=user_id)
        
        try:
            await self.stub.DeleteUser(request)
            logging.info(f"Deleted user: {user_id}")
        except grpc.RpcError as e:
            logging.error(f"Failed to delete user {user_id}: {e.details()}")
            raise
    
    async def list_users(self, page_size: int = 10, filter_text: str = "") -> List[user_service_pb2.User]:
        """List users with streaming"""
        request = user_service_pb2.ListUsersRequest(
            page_size=page_size,
            filter=filter_text
        )
        
        users = []
        try:
            async for user in self.stub.ListUsers(request):
                users.append(user)
                logging.info(f"Received user: {user.name}")
            
            return users
        except grpc.RpcError as e:
            logging.error(f"Failed to list users: {e.details()}")
            raise
    
    async def bulk_create_users(self, users_data: List[dict]) -> user_service_pb2.BulkCreateUsersResponse:
        """Create multiple users using client streaming"""
        
        async def request_generator():
            for user_data in users_data:
                request = user_service_pb2.CreateUserRequest(
                    name=user_data['name'],
                    email=user_data['email'],
                    age=user_data.get('age', 0),
                    roles=user_data.get('roles', []),
                    metadata=user_data.get('metadata', {})
                )
                yield request
                await asyncio.sleep(0.1)  # Simulate delay between requests
        
        try:
            response = await self.stub.BulkCreateUsers(request_generator())
            logging.info(f"Bulk created {response.created_count} users")
            
            if response.errors:
                logging.warning(f"Errors during bulk creation: {response.errors}")
            
            return response
        except grpc.RpcError as e:
            logging.error(f"Failed to bulk create users: {e.details()}")
            raise
    
    async def chat(self, messages: List[str]) -> List[user_service_pb2.ChatMessage]:
        """Bidirectional streaming chat"""
        responses = []
        
        async def request_generator():
            for i, message in enumerate(messages):
                chat_message = user_service_pb2.ChatMessage(
                    user_id=f"client-{i}",
                    message=message,
                    timestamp=user_service_pb2.google_dot_protobuf_dot_timestamp__pb2.Timestamp(),
                    type=user_service_pb2.MessageType.TEXT
                )
                yield chat_message
                await asyncio.sleep(1)  # Send message every second
        
        try:
            async for response in self.stub.Chat(request_generator()):
                responses.append(response)
                logging.info(f"Received chat response: {response.message}")
            
            return responses
        except grpc.RpcError as e:
            logging.error(f"Chat failed: {e.details()}")
            raise

# Example usage
async def main():
    async with UserServiceClient() as client:
        # Create a user
        user = await client.create_user(
            name="John Doe",
            email="john@example.com",
            age=30,
            roles=["user", "admin"],
            metadata={"department": "engineering"}
        )
        print(f"Created user: {user}")
        
        # Get the user
        retrieved_user = await client.get_user(user.id)
        print(f"Retrieved user: {retrieved_user}")
        
        # Update the user
        updated_user = await client.update_user(user.id, age=31)
        print(f"Updated user: {updated_user}")
        
        # List users
        users = await client.list_users(page_size=5)
        print(f"Listed {len(users)} users")
        
        # Bulk create users
        bulk_users = [
            {"name": f"User {i}", "email": f"user{i}@example.com", "age": 20 + i}
            for i in range(5)
        ]
        bulk_response = await client.bulk_create_users(bulk_users)
        print(f"Bulk created {bulk_response.created_count} users")
        
        # Chat example
        chat_messages = ["Hello", "How are you?", "Goodbye"]
        chat_responses = await client.chat(chat_messages)
        print(f"Chat responses: {[r.message for r in chat_responses]}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
```

### Go Client
```go
package main

import (
	"context"
	"io"
	"log"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/protobuf/types/known/timestamppb"

	pb "github.com/example/user-service/pb"
)

type UserServiceClient struct {
	conn   *grpc.ClientConn
	client pb.UserServiceClient
}

func NewUserServiceClient(address string) (*UserServiceClient, error) {
	conn, err := grpc.Dial(address, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		return nil, err
	}

	client := pb.NewUserServiceClient(conn)

	return &UserServiceClient{
		conn:   conn,
		client: client,
	}, nil
}

func (c *UserServiceClient) Close() error {
	return c.conn.Close()
}

func (c *UserServiceClient) GetUser(ctx context.Context, userID string, fields []string) (*pb.User, error) {
	req := &pb.GetUserRequest{
		Id:     userID,
		Fields: fields,
	}

	return c.client.GetUser(ctx, req)
}

func (c *UserServiceClient) CreateUser(ctx context.Context, name, email string, age int32, roles []string, metadata map[string]string) (*pb.User, error) {
	req := &pb.CreateUserRequest{
		Name:     name,
		Email:    email,
		Age:      age,
		Roles:    roles,
		Metadata: metadata,
	}

	return c.client.CreateUser(ctx, req)
}

func (c *UserServiceClient) UpdateUser(ctx context.Context, userID string, user *pb.User) (*pb.User, error) {
	req := &pb.UpdateUserRequest{
		Id:   userID,
		User: user,
	}

	return c.client.UpdateUser(ctx, req)
}

func (c *UserServiceClient) DeleteUser(ctx context.Context, userID string) error {
	req := &pb.DeleteUserRequest{
		Id: userID,
	}

	_, err := c.client.DeleteUser(ctx, req)
	return err
}

func (c *UserServiceClient) ListUsers(ctx context.Context, pageSize int32, filter string) ([]*pb.User, error) {
	req := &pb.ListUsersRequest{
		PageSize: pageSize,
		Filter:   filter,
	}

	stream, err := c.client.ListUsers(ctx, req)
	if err != nil {
		return nil, err
	}

	var users []*pb.User
	for {
		user, err := stream.Recv()
		if err == io.EOF {
			break
		}
		if err != nil {
			return nil, err
		}
		users = append(users, user)
	}

	return users, nil
}

func (c *UserServiceClient) BulkCreateUsers(ctx context.Context, usersData []map[string]interface{}) (*pb.BulkCreateUsersResponse, error) {
	stream, err := c.client.BulkCreateUsers(ctx)
	if err != nil {
		return nil, err
	}

	// Send requests
	for _, userData := range usersData {
		req := &pb.CreateUserRequest{
			Name:  userData["name"].(string),
			Email: userData["email"].(string),
		}

		if age, ok := userData["age"].(int32); ok {
			req.Age = age
		}

		if roles, ok := userData["roles"].([]string); ok {
			req.Roles = roles
		}

		if metadata, ok := userData["metadata"].(map[string]string); ok {
			req.Metadata = metadata
		}

		if err := stream.Send(req); err != nil {
			return nil, err
		}

		time.Sleep(100 * time.Millisecond) // Simulate delay
	}

	return stream.CloseAndRecv()
}

func (c *UserServiceClient) Chat(ctx context.Context, messages []string) ([]*pb.ChatMessage, error) {
	stream, err := c.client.Chat(ctx)
	if err != nil {
		return nil, err
	}

	var responses []*pb.ChatMessage

	// Start receiving responses
	go func() {
		for {
			response, err := stream.Recv()
			if err == io.EOF {
				return
			}
			if err != nil {
				log.Printf("Error receiving chat message: %v", err)
				return
			}
			responses = append(responses, response)
			log.Printf("Received chat response: %s", response.Message)
		}
	}()

	// Send messages
	for i, message := range messages {
		chatMessage := &pb.ChatMessage{
			UserId:    fmt.Sprintf("client-%d", i),
			Message:   message,
			Timestamp: timestamppb.Now(),
			Type:      pb.MessageType_TEXT,
		}

		if err := stream.Send(chatMessage); err != nil {
			return nil, err
		}

		time.Sleep(1 * time.Second)
	}

	if err := stream.CloseSend(); err != nil {
		return nil, err
	}

	// Wait a bit for all responses
	time.Sleep(2 * time.Second)

	return responses, nil
}

func main() {
	client, err := NewUserServiceClient("localhost:50051")
	if err != nil {
		log.Fatalf("Failed to create client: %v", err)
	}
	defer client.Close()

	ctx := context.Background()

	// Create a user
	user, err := client.CreateUser(ctx, "John Doe", "john@example.com", 30, []string{"user", "admin"}, map[string]string{"department": "engineering"})
	if err != nil {
		log.Fatalf("Failed to create user: %v", err)
	}
	log.Printf("Created user: %v", user)

	// Get the user
	retrievedUser, err := client.GetUser(ctx, user.Id, nil)
	if err != nil {
		log.Fatalf("Failed to get user: %v", err)
	}
	log.Printf("Retrieved user: %v", retrievedUser)

	// List users
	users, err := client.ListUsers(ctx, 5, "")
	if err != nil {
		log.Fatalf("Failed to list users: %v", err)
	}
	log.Printf("Listed %d users", len(users))

	// Bulk create users
	bulkUsers := []map[string]interface{}{
		{"name": "User 1", "email": "user1@example.com", "age": int32(21)},
		{"name": "User 2", "email": "user2@example.com", "age": int32(22)},
		{"name": "User 3", "email": "user3@example.com", "age": int32(23)},
	}

	bulkResponse, err := client.BulkCreateUsers(ctx, bulkUsers)
	if err != nil {
		log.Fatalf("Failed to bulk create users: %v", err)
	}
	log.Printf("Bulk created %d users", bulkResponse.CreatedCount)

	// Chat example
	chatMessages := []string{"Hello", "How are you?", "Goodbye"}
	chatResponses, err := client.Chat(ctx, chatMessages)
	if err != nil {
		log.Fatalf("Chat failed: %v", err)
	}
	log.Printf("Chat completed with %d responses", len(chatResponses))
}
```

## Middleware and Interceptors

### Python Interceptors
```python
import time
import logging
from typing import Callable, Any

import grpc
from grpc import aio

class LoggingInterceptor(aio.ServerInterceptor):
    """Server interceptor for logging requests"""
    
    async def intercept_service(self, continuation, handler_call_details):
        start_time = time.time()
        method = handler_call_details.method
        
        logging.info(f"Starting request: {method}")
        
        try:
            response = await continuation(handler_call_details)
            duration = time.time() - start_time
            logging.info(f"Completed request: {method} in {duration:.3f}s")
            return response
        except Exception as e:
            duration = time.time() - start_time
            logging.error(f"Failed request: {method} in {duration:.3f}s - {str(e)}")
            raise

class AuthenticationInterceptor(aio.ServerInterceptor):
    """Server interceptor for authentication"""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.public_methods = {
            '/user.UserService/GetUser',  # Allow unauthenticated access
        }
    
    async def intercept_service(self, continuation, handler_call_details):
        method = handler_call_details.method
        
        # Skip auth for public methods
        if method in self.public_methods:
            return await continuation(handler_call_details)
        
        # Get metadata
        metadata = dict(handler_call_details.invocation_metadata)
        auth_token = metadata.get('authorization', '').replace('Bearer ', '')
        
        if not auth_token:
            raise grpc.aio.AioRpcError(
                grpc.StatusCode.UNAUTHENTICATED,
                "Missing authentication token"
            )
        
        # Validate token (simplified)
        if not self.validate_token(auth_token):
            raise grpc.aio.AioRpcError(
                grpc.StatusCode.UNAUTHENTICATED,
                "Invalid authentication token"
            )
        
        return await continuation(handler_call_details)
    
    def validate_token(self, token: str) -> bool:
        # Simplified token validation
        return token == self.secret_key

class RateLimitInterceptor(aio.ServerInterceptor):
    """Server interceptor for rate limiting"""
    
    def __init__(self, max_requests_per_minute: int = 60):
        self.max_requests = max_requests_per_minute
        self.requests = {}  # client_id -> [timestamps]
    
    async def intercept_service(self, continuation, handler_call_details):
        # Get client identifier (simplified)
        metadata = dict(handler_call_details.invocation_metadata)
        client_id = metadata.get('client-id', 'unknown')
        
        current_time = time.time()
        minute_ago = current_time - 60
        
        # Clean old requests
        if client_id in self.requests:
            self.requests[client_id] = [
                ts for ts in self.requests[client_id] if ts > minute_ago
            ]
        else:
            self.requests[client_id] = []
        
        # Check rate limit
        if len(self.requests[client_id]) >= self.max_requests:
            raise grpc.aio.AioRpcError(
                grpc.StatusCode.RESOURCE_EXHAUSTED,
                "Rate limit exceeded"
            )
        
        # Record request
        self.requests[client_id].append(current_time)
        
        return await continuation(handler_call_details)

# Client interceptors
class ClientLoggingInterceptor(aio.UnaryUnaryClientInterceptor):
    """Client interceptor for logging"""
    
    async def intercept_unary_unary(self, continuation, client_call_details, request):
        start_time = time.time()
        method = client_call_details.method
        
        logging.info(f"Client calling: {method}")
        
        try:
            response = await continuation(client_call_details, request)
            duration = time.time() - start_time
            logging.info(f"Client completed: {method} in {duration:.3f}s")
            return response
        except Exception as e:
            duration = time.time() - start_time
            logging.error(f"Client failed: {method} in {duration:.3f}s - {str(e)}")
            raise

class ClientAuthInterceptor(aio.UnaryUnaryClientInterceptor):
    """Client interceptor for adding authentication"""
    
    def __init__(self, auth_token: str):
        self.auth_token = auth_token
    
    async def intercept_unary_unary(self, continuation, client_call_details, request):
        # Add authentication metadata
        metadata = list(client_call_details.metadata or [])
        metadata.append(('authorization', f'Bearer {self.auth_token}'))
        
        new_details = client_call_details._replace(metadata=metadata)
        return await continuation(new_details, request)

# Server setup with interceptors
async def serve_with_interceptors():
    interceptors = [
        LoggingInterceptor(),
        AuthenticationInterceptor("secret-key-123"),
        RateLimitInterceptor(max_requests_per_minute=100)
    ]
    
    server = aio.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=interceptors
    )
    
    user_service_pb2_grpc.add_UserServiceServicer_to_server(UserServiceImpl(), server)
    
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    
    await server.start()
    await server.wait_for_termination()

# Client setup with interceptors
async def create_client_with_interceptors():
    interceptors = [
        ClientLoggingInterceptor(),
        ClientAuthInterceptor("secret-key-123")
    ]
    
    channel = aio.insecure_channel(
        'localhost:50051',
        interceptors=interceptors
    )
    
    return user_service_pb2_grpc.UserServiceStub(channel)
```

### Go Interceptors
```go
package main

import (
	"context"
	"log"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/metadata"
	"google.golang.org/grpc/status"
)

// Server interceptors

func LoggingInterceptor(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
	start := time.Now()
	
	log.Printf("Starting request: %s", info.FullMethod)
	
	resp, err := handler(ctx, req)
	
	duration := time.Since(start)
	if err != nil {
		log.Printf("Failed request: %s in %v - %v", info.FullMethod, duration, err)
	} else {
		log.Printf("Completed request: %s in %v", info.FullMethod, duration)
	}
	
	return resp, err
}

func AuthenticationInterceptor(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
	// Public methods that don't require authentication
	publicMethods := map[string]bool{
		"/user.UserService/GetUser": true,
	}
	
	if publicMethods[info.FullMethod] {
		return handler(ctx, req)
	}
	
	// Get metadata
	md, ok := metadata.FromIncomingContext(ctx)
	if !ok {
		return nil, status.Error(codes.Unauthenticated, "missing metadata")
	}
	
	// Get authorization header
	authHeaders := md.Get("authorization")
	if len(authHeaders) == 0 {
		return nil, status.Error(codes.Unauthenticated, "missing authorization header")
	}
	
	authToken := authHeaders[0]
	if !validateToken(authToken) {
		return nil, status.Error(codes.Unauthenticated, "invalid token")
	}
	
	return handler(ctx, req)
}

func validateToken(token string) bool {
	// Simplified token validation
	return token == "Bearer secret-key-123"
}

type RateLimiter struct {
	maxRequests int
	requests    map[string][]time.Time
}

func NewRateLimiter(maxRequestsPerMinute int) *RateLimiter {
	return &RateLimiter{
		maxRequests: maxRequestsPerMinute,
		requests:    make(map[string][]time.Time),
	}
}

func (rl *RateLimiter) Interceptor(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
	// Get client identifier
	md, _ := metadata.FromIncomingContext(ctx)
	clientIDs := md.Get("client-id")
	clientID := "unknown"
	if len(clientIDs) > 0 {
		clientID = clientIDs[0]
	}
	
	now := time.Now()
	minuteAgo := now.Add(-time.Minute)
	
	// Clean old requests
	if requests, exists := rl.requests[clientID]; exists {
		var validRequests []time.Time
		for _, reqTime := range requests {
			if reqTime.After(minuteAgo) {
				validRequests = append(validRequests, reqTime)
			}
		}
		rl.requests[clientID] = validRequests
	}
	
	// Check rate limit
	if len(rl.requests[clientID]) >= rl.maxRequests {
		return nil, status.Error(codes.ResourceExhausted, "rate limit exceeded")
	}
	
	// Record request
	rl.requests[clientID] = append(rl.requests[clientID], now)
	
	return handler(ctx, req)
}

// Streaming interceptor
func LoggingStreamInterceptor(srv interface{}, stream grpc.ServerStream, info *grpc.StreamServerInfo, handler grpc.StreamHandler) error {
	start := time.Now()
	
	log.Printf("Starting stream: %s", info.FullMethod)
	
	err := handler(srv, stream)
	
	duration := time.Since(start)
	if err != nil {
		log.Printf("Failed stream: %s in %v - %v", info.FullMethod, duration, err)
	} else {
		log.Printf("Completed stream: %s in %v", info.FullMethod, duration)
	}
	
	return err
}

// Client interceptors

func ClientLoggingInterceptor(ctx context.Context, method string, req, reply interface{}, cc *grpc.ClientConn, invoker grpc.UnaryInvoker, opts ...grpc.CallOption) error {
	start := time.Now()
	
	log.Printf("Client calling: %s", method)
	
	err := invoker(ctx, method, req, reply, cc, opts...)
	
	duration := time.Since(start)
	if err != nil {
		log.Printf("Client failed: %s in %v - %v", method, duration, err)
	} else {
		log.Printf("Client completed: %s in %v", method, duration)
	}
	
	return err
}

func ClientAuthInterceptor(token string) grpc.UnaryClientInterceptor {
	return func(ctx context.Context, method string, req, reply interface{}, cc *grpc.ClientConn, invoker grpc.UnaryInvoker, opts ...grpc.CallOption) error {
		// Add authentication metadata
		ctx = metadata.AppendToOutgoingContext(ctx, "authorization", token)
		return invoker(ctx, method, req, reply, cc, opts...)
	}
}

// Server setup with interceptors
func NewServerWithInterceptors() *grpc.Server {
	rateLimiter := NewRateLimiter(100)
	
	unaryInterceptors := grpc.ChainUnaryInterceptor(
		LoggingInterceptor,
		AuthenticationInterceptor,
		rateLimiter.Interceptor,
	)
	
	streamInterceptors := grpc.ChainStreamInterceptor(
		LoggingStreamInterceptor,
	)
	
	return grpc.NewServer(
		unaryInterceptors,
		streamInterceptors,
	)
}

// Client setup with interceptors
func NewClientWithInterceptors(address string) (pb.UserServiceClient, error) {
	unaryInterceptors := grpc.WithChainUnaryInterceptor(
		ClientLoggingInterceptor,
		ClientAuthInterceptor("Bearer secret-key-123"),
	)
	
	conn, err := grpc.Dial(address, 
		grpc.WithTransportCredentials(insecure.NewCredentials()),
		unaryInterceptors,
	)
	if err != nil {
		return nil, err
	}
	
	return pb.NewUserServiceClient(conn), nil
}
```

## Testing

### Unit Testing
```python
import unittest
from unittest.mock import Mock, AsyncMock
import grpc
from grpc import aio
from grpc_testing import server_from_dictionary, strict_real_time

from pb import user_service_pb2, user_service_pb2_grpc
from server import UserServiceImpl

class TestUserService(unittest.IsolatedAsyncioTestCase):
    
    async def asyncSetUp(self):
        # Create test server
        self.servicer = UserServiceImpl()
        self.server = server_from_dictionary(
            {user_service_pb2.DESCRIPTOR.services_by_name['UserService']: self.servicer},
            strict_real_time()
        )
    
    async def test_create_user_success(self):
        """Test successful user creation"""
        request = user_service_pb2.CreateUserRequest(
            name="John Doe",
            email="john@example.com",
            age=30,
            roles=["user"]
        )
        
        method = self.server.invoke_unary_unary(
            user_service_pb2.DESCRIPTOR.services_by_name['UserService'].methods_by_name['CreateUser'],
            {},
            request,
            strict_real_time()
        )
        
        response, metadata, code, details = method.termination()
        
        self.assertEqual(code, grpc.StatusCode.OK)
        self.assertEqual(response.name, "John Doe")
        self.assertEqual(response.email, "john@example.com")
        self.assertIsNotNone(response.id)
    
    async def test_create_user_missing_fields(self):
        """Test user creation with missing required fields"""
        request = user_service_pb2.CreateUserRequest(
            name="",  # Missing name
            email="john@example.com"
        )
        
        method = self.server.invoke_unary_unary(
            user_service_pb2.DESCRIPTOR.services_by_name['UserService'].methods_by_name['CreateUser'],
            {},
            request,
            strict_real_time()
        )
        
        response, metadata, code, details = method.termination()
        
        self.assertEqual(code, grpc.StatusCode.INVALID_ARGUMENT)
        self.assertIn("required", details)
    
    async def test_get_user_not_found(self):
        """Test getting non-existent user"""
        request = user_service_pb2.GetUserRequest(id="nonexistent")
        
        method = self.server.invoke_unary_unary(
            user_service_pb2.DESCRIPTOR.services_by_name['UserService'].methods_by_name['GetUser'],
            {},
            request,
            strict_real_time()
        )
        
        response, metadata, code, details = method.termination()
        
        self.assertEqual(code, grpc.StatusCode.NOT_FOUND)
    
    async def test_list_users_streaming(self):
        """Test user listing with streaming"""
        # First create some users
        for i in range(3):
            await self.servicer.CreateUser(
                user_service_pb2.CreateUserRequest(
                    name=f"User {i}",
                    email=f"user{i}@example.com"
                ),
                Mock()
            )
        
        request = user_service_pb2.ListUsersRequest(page_size=10)
        
        method = self.server.invoke_unary_stream(
            user_service_pb2.DESCRIPTOR.services_by_name['UserService'].methods_by_name['ListUsers'],
            {},
            request,
            strict_real_time()
        )
        
        responses = []
        for response in method.responses():
            responses.append(response)
        
        metadata, code, details = method.termination()
        
        self.assertEqual(code, grpc.StatusCode.OK)
        self.assertEqual(len(responses), 3)

# Integration tests
class TestUserServiceIntegration(unittest.IsolatedAsyncioTestCase):
    
    async def asyncSetUp(self):
        # Start real server for integration tests
        self.server = aio.server()
        user_service_pb2_grpc.add_UserServiceServicer_to_server(UserServiceImpl(), self.server)
        
        listen_addr = '[::]:50052'  # Different port for tests
        self.server.add_insecure_port(listen_addr)
        await self.server.start()
        
        # Create client
        self.channel = aio.insecure_channel('localhost:50052')
        self.client = user_service_pb2_grpc.UserServiceStub(self.channel)
    
    async def asyncTearDown(self):
        await self.channel.close()
        await self.server.stop(5)
    
    async def test_full_user_lifecycle(self):
        """Test complete user lifecycle"""
        # Create user
        create_request = user_service_pb2.CreateUserRequest(
            name="Integration Test User",
            email="integration@example.com",
            age=25
        )
        
        user = await self.client.CreateUser(create_request)
        self.assertIsNotNone(user.id)
        
        # Get user
        get_request = user_service_pb2.GetUserRequest(id=user.id)
        retrieved_user = await self.client.GetUser(get_request)
        self.assertEqual(retrieved_user.email, "integration@example.com")
        
        # Update user
        update_request = user_service_pb2.UpdateUserRequest(
            id=user.id,
            user=user_service_pb2.User(age=26)
        )
        updated_user = await self.client.UpdateUser(update_request)
        self.assertEqual(updated_user.age, 26)
        
        # Delete user
        delete_request = user_service_pb2.DeleteUserRequest(id=user.id)
        await self.client.DeleteUser(delete_request)
        
        # Verify deletion
        with self.assertRaises(grpc.aio.AioRpcError) as context:
            await self.client.GetUser(get_request)
        
        self.assertEqual(context.exception.code(), grpc.StatusCode.NOT_FOUND)

if __name__ == '__main__':
    unittest.main()
```

### Load Testing
```python
import asyncio
import time
import statistics
from concurrent.futures import ThreadPoolExecutor

import grpc
from grpc import aio

from pb import user_service_pb2, user_service_pb2_grpc

class LoadTester:
    def __init__(self, server_address='localhost:50051', concurrent_clients=10):
        self.server_address = server_address
        self.concurrent_clients = concurrent_clients
        self.results = []
    
    async def create_client(self):
        """Create a gRPC client"""
        channel = aio.insecure_channel(self.server_address)
        return user_service_pb2_grpc.UserServiceStub(channel), channel
    
    async def single_request_test(self, client_id: int, num_requests: int):
        """Run requests from a single client"""
        client, channel = await self.create_client()
        client_results = []
        
        try:
            for i in range(num_requests):
                start_time = time.time()
                
                try:
                    # Create user request
                    request = user_service_pb2.CreateUserRequest(
                        name=f"LoadTest User {client_id}-{i}",
                        email=f"loadtest{client_id}_{i}@example.com",
                        age=20 + (i % 50)
                    )
                    
                    response = await client.CreateUser(request)
                    
                    end_time = time.time()
                    latency = (end_time - start_time) * 1000  # Convert to ms
                    
                    client_results.append({
                        'client_id': client_id,
                        'request_id': i,
                        'latency_ms': latency,
                        'success': True,
                        'response_size': len(response.SerializeToString())
                    })
                    
                except grpc.aio.AioRpcError as e:
                    end_time = time.time()
                    latency = (end_time - start_time) * 1000
                    
                    client_results.append({
                        'client_id': client_id,
                        'request_id': i,
                        'latency_ms': latency,
                        'success': False,
                        'error_code': e.code().name,
                        'error_details': e.details()
                    })
                
                # Small delay between requests
                await asyncio.sleep(0.01)
        
        finally:
            await channel.close()
        
        return client_results
    
    async def run_load_test(self, requests_per_client=100, duration_seconds=None):
        """Run load test with multiple concurrent clients"""
        print(f"Starting load test with {self.concurrent_clients} clients")
        print(f"Requests per client: {requests_per_client}")
        
        start_time = time.time()
        
        # Create tasks for concurrent clients
        tasks = []
        for client_id in range(self.concurrent_clients):
            task = asyncio.create_task(
                self.single_request_test(client_id, requests_per_client)
            )
            tasks.append(task)
        
        # Wait for all clients to complete
        results = await asyncio.gather(*tasks)
        
        end_time = time.time()
        total_duration = end_time - start_time
        
        # Flatten results
        all_results = []
        for client_results in results:
            all_results.extend(client_results)
        
        self.results = all_results
        
        # Generate report
        self.generate_report(total_duration)
    
    def generate_report(self, total_duration: float):
        """Generate load test report"""
        successful_requests = [r for r in self.results if r['success']]
        failed_requests = [r for r in self.results if not r['success']]
        
        total_requests = len(self.results)
        success_rate = len(successful_requests) / total_requests * 100
        
        if successful_requests:
            latencies = [r['latency_ms'] for r in successful_requests]
            avg_latency = statistics.mean(latencies)
            median_latency = statistics.median(latencies)
            p95_latency = sorted(latencies)[int(len(latencies) * 0.95)]
            p99_latency = sorted(latencies)[int(len(latencies) * 0.99)]
            min_latency = min(latencies)
            max_latency = max(latencies)
        else:
            avg_latency = median_latency = p95_latency = p99_latency = min_latency = max_latency = 0
        
        requests_per_second = total_requests / total_duration
        
        print("\n" + "="*50)
        print("LOAD TEST REPORT")
        print("="*50)
        print(f"Total Duration: {total_duration:.2f}s")
        print(f"Total Requests: {total_requests}")
        print(f"Successful Requests: {len(successful_requests)}")
        print(f"Failed Requests: {len(failed_requests)}")
        print(f"Success Rate: {success_rate:.2f}%")
        print(f"Requests/Second: {requests_per_second:.2f}")
        print()
        print("LATENCY STATISTICS (ms):")
        print(f"  Average: {avg_latency:.2f}")
        print(f"  Median: {median_latency:.2f}")
        print(f"  95th Percentile: {p95_latency:.2f}")
        print(f"  99th Percentile: {p99_latency:.2f}")
        print(f"  Min: {min_latency:.2f}")
        print(f"  Max: {max_latency:.2f}")
        print()
        
        if failed_requests:
            print("ERRORS:")
            error_counts = {}
            for req in failed_requests:
                error = req.get('error_code', 'UNKNOWN')
                error_counts[error] = error_counts.get(error, 0) + 1
            
            for error, count in error_counts.items():
                print(f"  {error}: {count}")
        
        print("="*50)

# Run load test
async def main():
    tester = LoadTester(concurrent_clients=50)
    await tester.run_load_test(requests_per_client=100)

if __name__ == "__main__":
    asyncio.run(main())
```

## Resources

- [gRPC Documentation](https://grpc.io/docs/)
- [Protocol Buffers Guide](https://developers.google.com/protocol-buffers)
- [gRPC Python](https://grpc.github.io/grpc/python/)
- [gRPC Go](https://grpc.github.io/grpc-go/)
- [gRPC Java](https://grpc.github.io/grpc-java/)
- [gRPC Node.js](https://grpc.github.io/grpc-node/)
- [gRPC Best Practices](https://grpc.io/docs/guides/best-practices/)
- [gRPC Performance](https://grpc.io/docs/guides/performance/)
- [gRPC Security](https://grpc.io/docs/guides/auth/)
- [Community Examples](https://github.com/grpc/grpc/tree/master/examples)