# Go

## Overview

Go (Golang) is a statically typed, compiled programming language designed by Google for building reliable, efficient software. It's become the language of choice for cloud-native infrastructure, with most CNCF projects written in Go.

## Key Features

- **Fast Compilation**: Compiles to single binary with no dependencies
- **Concurrency**: Built-in goroutines and channels for concurrent programming
- **Simple Syntax**: Easy to learn and read
- **Strong Standard Library**: Excellent support for networking, HTTP, and system programming
- **Cross-Platform**: Compile for multiple architectures and operating systems

## Common Use Cases

### HTTP Services
```go
package main

import (
    "encoding/json"
    "net/http"
    "log"
)

type HealthResponse struct {
    Status string `json:"status"`
    Version string `json:"version"`
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
    response := HealthResponse{
        Status:  "healthy",
        Version: "1.0.0",
    }
    
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

func main() {
    http.HandleFunc("/health", healthHandler)
    log.Fatal(http.ListenAndServe(":8080", nil))
}
```

### CLI Tools
```go
package main

import (
    "flag"
    "fmt"
    "os"
)

func main() {
    var name = flag.String("name", "World", "Name to greet")
    var verbose = flag.Bool("verbose", false, "Enable verbose output")
    flag.Parse()

    if *verbose {
        fmt.Printf("Greeting %s\n", *name)
    }
    fmt.Printf("Hello, %s!\n", *name)
}
```

### Container Management
```go
package main

import (
    "context"
    "fmt"
    "github.com/docker/docker/client"
)

func main() {
    cli, err := client.NewClientWithOpts(client.FromEnv)
    if err != nil {
        panic(err)
    }

    containers, err := cli.ContainerList(context.Background(), types.ContainerListOptions{})
    if err != nil {
        panic(err)
    }

    for _, container := range containers {
        fmt.Printf("Container: %s\n", container.Names[0])
    }
}
```

## Essential Libraries

- **cobra** - CLI application framework
- **gin** - HTTP web framework
- **kubernetes/client-go** - Kubernetes client
- **docker/docker** - Docker client
- **prometheus/client_golang** - Prometheus metrics
- **logrus** - Structured logging
- **testify** - Testing toolkit

## Popular Go Tools in Platform Engineering

- **Kubernetes** - Container orchestration
- **Docker** - Containerization platform
- **Terraform** - Infrastructure as code
- **Prometheus** - Monitoring system
- **etcd** - Distributed key-value store
- **Consul** - Service mesh and discovery

## Best Practices

- Follow Go conventions (gofmt, go vet)
- Use modules for dependency management
- Handle errors explicitly
- Write tests alongside code
- Use interfaces for abstraction
- Keep functions small and focused

## Great Resources

- [Go Official Documentation](https://golang.org/doc/) - Complete language guide and tutorials
- [Go by Example](https://gobyexample.com/) - Hands-on introduction with examples
- [Effective Go](https://golang.org/doc/effective_go.html) - Best practices and idioms
- [A Tour of Go](https://tour.golang.org/) - Interactive introduction to Go
- [Go Cloud Development Kit](https://gocloud.dev/) - Cloud-portable Go libraries
- [Awesome Go](https://awesome-go.com/) - Curated list of Go frameworks and libraries
- [Go Web Examples](https://gowebexamples.com/) - Web development patterns in Go