# Rust

## Overview

Rust is a systems programming language that focuses on safety, speed, and concurrency. It's increasingly adopted in platform engineering for building high-performance infrastructure tools, CLI utilities, and system-level components without sacrificing memory safety.

## Key Features

- **Memory Safety**: Prevents buffer overflows and memory leaks without garbage collection
- **Zero-Cost Abstractions**: High-level features with no runtime overhead
- **Concurrency**: Safe concurrent programming with ownership system
- **Performance**: Comparable to C and C++ in speed
- **Cross-Platform**: Excellent support for multiple architectures

## Common Use Cases

### CLI Tools
```rust
use clap::{App, Arg};
use std::fs;

fn main() {
    let matches = App::new("file-counter")
        .version("1.0")
        .about("Counts files in a directory")
        .arg(Arg::with_name("path")
            .help("Directory path to count files")
            .required(true)
            .index(1))
        .get_matches();

    let path = matches.value_of("path").unwrap();
    
    match count_files(path) {
        Ok(count) => println!("Found {} files in {}", count, path),
        Err(e) => eprintln!("Error: {}", e),
    }
}

fn count_files(path: &str) -> Result<usize, std::io::Error> {
    let entries = fs::read_dir(path)?;
    let count = entries.filter_map(|entry| entry.ok()).count();
    Ok(count)
}
```

### HTTP Services
```rust
use warp::Filter;
use serde::{Deserialize, Serialize};

#[derive(Serialize)]
struct HealthResponse {
    status: String,
    timestamp: String,
}

#[tokio::main]
async fn main() {
    let health = warp::path("health")
        .and(warp::get())
        .map(|| {
            warp::reply::json(&HealthResponse {
                status: "healthy".to_string(),
                timestamp: chrono::Utc::now().to_rfc3339(),
            })
        });

    warp::serve(health)
        .run(([127, 0, 0, 1], 3030))
        .await;
}
```

### System Monitoring
```rust
use sysinfo::{System, SystemExt, ProcessorExt};

fn get_system_metrics() {
    let mut system = System::new_all();
    system.refresh_all();

    println!("CPU usage: {:.2}%", system.global_processor_info().cpu_usage());
    println!("Memory usage: {}/{} MB", 
        system.used_memory() / 1024 / 1024,
        system.total_memory() / 1024 / 1024
    );
    
    for (pid, process) in system.processes() {
        if process.cpu_usage() > 10.0 {
            println!("High CPU process: {} ({}%)", 
                process.name(), process.cpu_usage());
        }
    }
}
```

## Essential Crates (Libraries)

- **tokio** - Asynchronous runtime
- **serde** - Serialization framework
- **clap** - Command line argument parser
- **reqwest** - HTTP client
- **warp** / **axum** - Web frameworks
- **anyhow** - Error handling
- **tracing** - Logging and diagnostics

## Popular Rust Tools in Infrastructure

- **ripgrep** - Fast text search
- **bat** - Enhanced cat command
- **exa** - Modern ls replacement
- **fd** - Simple find alternative
- **delta** - Better git diff viewer
- **starship** - Cross-shell prompt
- **zoxide** - Smarter cd command

## Package Management

Rust uses **Cargo** for package management and building:

```toml
# Cargo.toml
[package]
name = "my-tool"
version = "0.1.0"
edition = "2021"

[dependencies]
tokio = { version = "1.0", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
clap = "4.0"
```

## Best Practices

- Use `cargo fmt` for consistent formatting
- Run `cargo clippy` for linting and suggestions
- Write comprehensive tests with `cargo test`
- Use `Result<T, E>` for error handling
- Leverage the ownership system for memory safety
- Document public APIs with `///` comments

## Great Resources

- [The Rust Programming Language Book](https://doc.rust-lang.org/book/) - Official comprehensive guide
- [Rust by Example](https://doc.rust-lang.org/rust-by-example/) - Learn Rust with examples
- [Rustlings](https://github.com/rust-lang/rustlings) - Interactive Rust exercises
- [Crates.io](https://crates.io/) - Official Rust package registry
- [Awesome Rust](https://github.com/rust-unofficial/awesome-rust) - Curated list of Rust libraries
- [Rust Cookbook](https://rust-lang-nursery.github.io/rust-cookbook/) - Common programming tasks
- [Command Line Applications in Rust](https://rust-cli.github.io/book/) - Building CLI tools