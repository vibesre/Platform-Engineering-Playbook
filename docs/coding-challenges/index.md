---
title: Platform Engineering Coding Challenges
sidebar_position: 1
---

# Platform Engineering Coding Challenges

This section contains coding challenges specifically tailored for platform engineering interviews. These problems focus on real-world scenarios you'll encounter when building and maintaining infrastructure.

## Challenge Categories

### 1. Infrastructure Automation
Build tools and scripts for automating infrastructure tasks.

### 2. Monitoring and Observability
Implement systems for tracking and analyzing metrics.

### 3. Distributed Systems
Solve problems related to coordination and communication in distributed environments.

### 4. Resource Management
Optimize resource allocation and scheduling.

### 5. Security and Compliance
Implement security controls and compliance checks.

## Difficulty Levels

- 🟢 **Easy**: 15-30 minutes, basic concepts
- 🟡 **Medium**: 30-45 minutes, moderate complexity
- 🔴 **Hard**: 45-60 minutes, advanced concepts

---

## Infrastructure Automation Challenges

### 🟢 Challenge 1: Configuration File Merger

**Problem:**
Write a function that merges configuration files with inheritance. Child configurations should override parent configurations, and arrays should be concatenated.

**Example:**
```python
base_config = {
    "server": {
        "port": 8080,
        "host": "localhost"
    },
    "features": ["logging", "metrics"],
    "database": {
        "host": "localhost",
        "port": 5432
    }
}

override_config = {
    "server": {
        "port": 9090
    },
    "features": ["tracing"],
    "database": {
        "host": "prod-db.example.com"
    }
}

# Result should be:
{
    "server": {
        "port": 9090,
        "host": "localhost"
    },
    "features": ["logging", "metrics", "tracing"],
    "database": {
        "host": "prod-db.example.com",
        "port": 5432
    }
}
```

**Solution:**
```python
def merge_configs(base, override):
    """
    Recursively merge configuration dictionaries.
    Arrays are concatenated, dictionaries are merged recursively.
    """
    result = base.copy()
    
    for key, value in override.items():
        if key in result:
            if isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = merge_configs(result[key], value)
            elif isinstance(result[key], list) and isinstance(value, list):
                result[key] = result[key] + value
            else:
                result[key] = value
        else:
            result[key] = value
    
    return result

# Test the function
def test_merge_configs():
    base = {
        "server": {"port": 8080, "host": "localhost"},
        "features": ["logging", "metrics"],
        "database": {"host": "localhost", "port": 5432}
    }
    
    override = {
        "server": {"port": 9090},
        "features": ["tracing"],
        "database": {"host": "prod-db.example.com"}
    }
    
    result = merge_configs(base, override)
    assert result["server"]["port"] == 9090
    assert result["server"]["host"] == "localhost"
    assert "tracing" in result["features"]
    assert len(result["features"]) == 3
    print("All tests passed!")

test_merge_configs()
```

### 🟡 Challenge 2: Service Dependency Resolver

**Problem:**
Given a list of services and their dependencies, return the order in which services should be started. Detect circular dependencies.

**Example:**
```python
services = {
    "api": ["database", "cache"],
    "database": [],
    "cache": ["database"],
    "worker": ["api", "queue"],
    "queue": []
}

# Result should be: ["database", "cache", "api", "queue", "worker"]
```

**Solution:**
```python
def resolve_dependencies(services):
    """
    Topological sort to resolve service dependencies.
    Returns ordered list or raises exception for circular dependencies.
    """
    # Build adjacency list and in-degree count
    in_degree = {service: 0 for service in services}
    adj_list = {service: [] for service in services}
    
    for service, deps in services.items():
        for dep in deps:
            if dep not in services:
                raise ValueError(f"Unknown dependency: {dep}")
            adj_list[dep].append(service)
            in_degree[service] += 1
    
    # Find all nodes with no dependencies
    queue = [service for service, degree in in_degree.items() if degree == 0]
    result = []
    
    while queue:
        # Process service with no remaining dependencies
        current = queue.pop(0)
        result.append(current)
        
        # Remove this service from dependencies
        for dependent in adj_list[current]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
    
    # Check for circular dependencies
    if len(result) != len(services):
        circular = [s for s, d in in_degree.items() if d > 0]
        raise ValueError(f"Circular dependency detected: {circular}")
    
    return result

# Test cases
def test_dependency_resolver():
    # Normal case
    services = {
        "api": ["database", "cache"],
        "database": [],
        "cache": ["database"],
        "worker": ["api", "queue"],
        "queue": []
    }
    order = resolve_dependencies(services)
    print(f"Start order: {order}")
    
    # Circular dependency
    circular_services = {
        "a": ["b"],
        "b": ["c"],
        "c": ["a"]
    }
    try:
        resolve_dependencies(circular_services)
    except ValueError as e:
        print(f"Caught expected error: {e}")

test_dependency_resolver()
```

### 🔴 Challenge 3: Container Scheduler

**Problem:**
Implement a simple container scheduler that assigns containers to nodes based on resource requirements and constraints.

**Requirements:**
- Each node has CPU and memory capacity
- Each container has CPU and memory requirements
- Support node affinity/anti-affinity
- Implement bin packing for optimal resource usage

**Solution:**
```python
class Node:
    def __init__(self, name, cpu, memory, labels=None):
        self.name = name
        self.total_cpu = cpu
        self.total_memory = memory
        self.available_cpu = cpu
        self.available_memory = memory
        self.labels = labels or {}
        self.containers = []
    
    def can_fit(self, container):
        return (self.available_cpu >= container.cpu and 
                self.available_memory >= container.memory)
    
    def add_container(self, container):
        if self.can_fit(container):
            self.containers.append(container)
            self.available_cpu -= container.cpu
            self.available_memory -= container.memory
            return True
        return False
    
    def score(self, container):
        """Score node for container placement (higher is better)"""
        if not self.can_fit(container):
            return -1
        
        # Prefer nodes with better resource fit
        cpu_utilization = (self.available_cpu - container.cpu) / self.total_cpu
        mem_utilization = (self.available_memory - container.memory) / self.total_memory
        
        # Balance between CPU and memory utilization
        return 1 - (cpu_utilization + mem_utilization) / 2

class Container:
    def __init__(self, name, cpu, memory, affinity=None, anti_affinity=None):
        self.name = name
        self.cpu = cpu
        self.memory = memory
        self.affinity = affinity or {}
        self.anti_affinity = anti_affinity or []
        self.node = None

class Scheduler:
    def __init__(self, nodes):
        self.nodes = nodes
    
    def schedule(self, containers):
        """Schedule containers to nodes"""
        scheduled = []
        failed = []
        
        # Sort containers by resource requirements (largest first)
        containers.sort(key=lambda c: c.cpu * c.memory, reverse=True)
        
        for container in containers:
            node = self._find_best_node(container)
            if node:
                node.add_container(container)
                container.node = node.name
                scheduled.append(container)
            else:
                failed.append(container)
        
        return scheduled, failed
    
    def _find_best_node(self, container):
        """Find the best node for a container"""
        eligible_nodes = []
        
        for node in self.nodes:
            # Check if node can fit container
            if not node.can_fit(container):
                continue
            
            # Check affinity constraints
            if container.affinity:
                if not all(node.labels.get(k) == v 
                          for k, v in container.affinity.items()):
                    continue
            
            # Check anti-affinity constraints
            if container.anti_affinity:
                conflicting = any(c.name in container.anti_affinity 
                                for c in node.containers)
                if conflicting:
                    continue
            
            eligible_nodes.append(node)
        
        if not eligible_nodes:
            return None
        
        # Return node with best score
        return max(eligible_nodes, key=lambda n: n.score(container))

# Test the scheduler
def test_scheduler():
    # Create nodes
    nodes = [
        Node("node1", cpu=4, memory=8, labels={"zone": "us-east"}),
        Node("node2", cpu=8, memory=16, labels={"zone": "us-west"}),
        Node("node3", cpu=2, memory=4, labels={"zone": "us-east", "gpu": "true"})
    ]
    
    # Create containers
    containers = [
        Container("web-1", cpu=1, memory=2, affinity={"zone": "us-east"}),
        Container("web-2", cpu=1, memory=2, anti_affinity=["web-1"]),
        Container("db-1", cpu=2, memory=4),
        Container("gpu-app", cpu=1, memory=2, affinity={"gpu": "true"}),
        Container("large-app", cpu=6, memory=12)
    ]
    
    # Schedule containers
    scheduler = Scheduler(nodes)
    scheduled, failed = scheduler.schedule(containers)
    
    # Print results
    print("Scheduling Results:")
    for container in scheduled:
        print(f"  {container.name} -> {container.node}")
    
    if failed:
        print("\nFailed to schedule:")
        for container in failed:
            print(f"  {container.name}")
    
    # Print node utilization
    print("\nNode Utilization:")
    for node in nodes:
        used_cpu = node.total_cpu - node.available_cpu
        used_mem = node.total_memory - node.available_memory
        print(f"  {node.name}: CPU {used_cpu}/{node.total_cpu}, "
              f"Memory {used_mem}/{node.total_memory}")

test_scheduler()
```

## Monitoring and Observability Challenges

### 🟢 Challenge 4: Log Rate Limiter

**Problem:**
Implement a rate limiter for log ingestion that limits logs per source per minute using a sliding window.

**Solution:**
```python
import time
from collections import defaultdict, deque

class LogRateLimiter:
    def __init__(self, max_logs_per_minute=100):
        self.max_logs_per_minute = max_logs_per_minute
        self.window_size = 60  # seconds
        self.logs = defaultdict(deque)
    
    def should_accept(self, source_id):
        """Check if log from source should be accepted"""
        current_time = time.time()
        source_logs = self.logs[source_id]
        
        # Remove old entries outside the window
        while source_logs and source_logs[0] < current_time - self.window_size:
            source_logs.popleft()
        
        # Check if under limit
        if len(source_logs) < self.max_logs_per_minute:
            source_logs.append(current_time)
            return True
        
        return False
    
    def get_stats(self):
        """Get current rate limiting stats"""
        current_time = time.time()
        stats = {}
        
        for source_id, timestamps in self.logs.items():
            # Clean old entries
            while timestamps and timestamps[0] < current_time - self.window_size:
                timestamps.popleft()
            
            if timestamps:
                stats[source_id] = {
                    'count': len(timestamps),
                    'rate': len(timestamps) / self.window_size * 60
                }
        
        return stats

# Test the rate limiter
def test_rate_limiter():
    limiter = LogRateLimiter(max_logs_per_minute=5)
    
    # Simulate log ingestion
    test_data = [
        ("app1", True),   # Should accept
        ("app1", True),   # Should accept
        ("app2", True),   # Should accept
        ("app1", True),   # Should accept
        ("app1", True),   # Should accept
        ("app1", True),   # Should accept
        ("app1", False),  # Should reject (over limit)
        ("app2", True),   # Should accept
    ]
    
    for source, expected in test_data:
        result = limiter.should_accept(source)
        status = "✓" if result == expected else "✗"
        print(f"{status} {source}: {'accepted' if result else 'rejected'}")
    
    print("\nStats:", limiter.get_stats())

test_rate_limiter()
```

### 🟡 Challenge 5: Metrics Aggregator

**Problem:**
Implement a system that aggregates metrics (p50, p95, p99) over sliding time windows.

**Solution:**
```python
import heapq
import time
from collections import defaultdict
import bisect

class MetricsAggregator:
    def __init__(self, window_size_seconds=60):
        self.window_size = window_size_seconds
        self.metrics = defaultdict(list)  # metric_name -> [(timestamp, value)]
    
    def record(self, metric_name, value, timestamp=None):
        """Record a metric value"""
        if timestamp is None:
            timestamp = time.time()
        
        # Insert in sorted order by timestamp
        metric_list = self.metrics[metric_name]
        bisect.insort(metric_list, (timestamp, value))
        
        # Remove old values outside window
        cutoff_time = timestamp - self.window_size
        while metric_list and metric_list[0][0] < cutoff_time:
            metric_list.pop(0)
    
    def get_percentiles(self, metric_name, percentiles=[50, 95, 99], 
                       current_time=None):
        """Calculate percentiles for a metric"""
        if current_time is None:
            current_time = time.time()
        
        # Get values within window
        cutoff_time = current_time - self.window_size
        values = [v for t, v in self.metrics[metric_name] 
                 if t >= cutoff_time]
        
        if not values:
            return {p: None for p in percentiles}
        
        values.sort()
        results = {}
        
        for p in percentiles:
            index = int((p / 100.0) * (len(values) - 1))
            results[p] = values[index]
        
        return results
    
    def get_stats(self, metric_name, current_time=None):
        """Get comprehensive stats for a metric"""
        if current_time is None:
            current_time = time.time()
        
        cutoff_time = current_time - self.window_size
        values = [v for t, v in self.metrics[metric_name] 
                 if t >= cutoff_time]
        
        if not values:
            return None
        
        return {
            'count': len(values),
            'min': min(values),
            'max': max(values),
            'avg': sum(values) / len(values),
            'p50': self.get_percentiles(metric_name, [50])[50],
            'p95': self.get_percentiles(metric_name, [95])[95],
            'p99': self.get_percentiles(metric_name, [99])[99]
        }

# Test the aggregator
def test_metrics_aggregator():
    agg = MetricsAggregator(window_size_seconds=10)
    
    # Simulate metric recording
    import random
    base_time = time.time()
    
    # Generate response times with some outliers
    for i in range(100):
        # Most requests are fast (20-50ms)
        if random.random() < 0.9:
            value = random.uniform(20, 50)
        else:
            # Some are slow (200-500ms)
            value = random.uniform(200, 500)
        
        agg.record("response_time", value, base_time + i * 0.1)
    
    # Get stats
    stats = agg.get_stats("response_time", base_time + 10)
    print("Response Time Stats:")
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}ms")
        else:
            print(f"  {key}: {value}")

test_metrics_aggregator()
```

### 🔴 Challenge 6: Distributed Tracing System

**Problem:**
Implement a basic distributed tracing system that can track requests across multiple services.

**Solution:**
```python
import uuid
import time
import json
from collections import defaultdict
from datetime import datetime

class Span:
    def __init__(self, trace_id, span_id, parent_id, service_name, 
                 operation_name):
        self.trace_id = trace_id
        self.span_id = span_id
        self.parent_id = parent_id
        self.service_name = service_name
        self.operation_name = operation_name
        self.start_time = time.time()
        self.end_time = None
        self.tags = {}
        self.logs = []
    
    def set_tag(self, key, value):
        self.tags[key] = value
    
    def log(self, message):
        self.logs.append({
            'timestamp': time.time(),
            'message': message
        })
    
    def finish(self):
        self.end_time = time.time()
        return self
    
    @property
    def duration(self):
        if self.end_time:
            return self.end_time - self.start_time
        return None
    
    def to_dict(self):
        return {
            'trace_id': self.trace_id,
            'span_id': self.span_id,
            'parent_id': self.parent_id,
            'service_name': self.service_name,
            'operation_name': self.operation_name,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration': self.duration,
            'tags': self.tags,
            'logs': self.logs
        }

class Tracer:
    def __init__(self, service_name):
        self.service_name = service_name
        self.active_spans = {}
        self.completed_spans = []
    
    def start_span(self, operation_name, parent_context=None):
        """Start a new span"""
        if parent_context:
            trace_id = parent_context.get('trace_id')
            parent_id = parent_context.get('span_id')
        else:
            trace_id = str(uuid.uuid4())
            parent_id = None
        
        span_id = str(uuid.uuid4())
        span = Span(trace_id, span_id, parent_id, 
                   self.service_name, operation_name)
        
        self.active_spans[span_id] = span
        return span
    
    def finish_span(self, span):
        """Finish a span and record it"""
        span.finish()
        if span.span_id in self.active_spans:
            del self.active_spans[span.span_id]
        self.completed_spans.append(span)
    
    def inject_context(self, span):
        """Create context for propagation"""
        return {
            'trace_id': span.trace_id,
            'span_id': span.span_id
        }
    
    def get_trace(self, trace_id):
        """Get all spans for a trace"""
        return [s for s in self.completed_spans 
                if s.trace_id == trace_id]

class DistributedTracingSystem:
    def __init__(self):
        self.tracers = {}
        self.all_spans = []
    
    def get_tracer(self, service_name):
        """Get or create tracer for service"""
        if service_name not in self.tracers:
            self.tracers[service_name] = Tracer(service_name)
        return self.tracers[service_name]
    
    def collect_spans(self):
        """Collect all spans from all tracers"""
        self.all_spans = []
        for tracer in self.tracers.values():
            self.all_spans.extend(tracer.completed_spans)
    
    def get_trace_tree(self, trace_id):
        """Build trace tree from spans"""
        self.collect_spans()
        spans = [s for s in self.all_spans if s.trace_id == trace_id]
        
        if not spans:
            return None
        
        # Build tree structure
        span_dict = {s.span_id: s for s in spans}
        root_spans = []
        
        for span in spans:
            if span.parent_id is None:
                root_spans.append(span)
        
        def build_tree(span):
            children = [s for s in spans if s.parent_id == span.span_id]
            return {
                'span': span.to_dict(),
                'children': [build_tree(child) for child in children]
            }
        
        return [build_tree(root) for root in root_spans]
    
    def print_trace(self, trace_id):
        """Pretty print a trace"""
        trees = self.get_trace_tree(trace_id)
        if not trees:
            print(f"No trace found for {trace_id}")
            return
        
        def print_span(node, indent=0):
            span = node['span']
            duration = span['duration'] * 1000 if span['duration'] else 0
            print(f"{'  ' * indent}├─ {span['service_name']}:"
                  f"{span['operation_name']} ({duration:.2f}ms)")
            
            for child in node['children']:
                print_span(child, indent + 1)
        
        for tree in trees:
            print_span(tree)

# Simulate a distributed system
def simulate_request():
    system = DistributedTracingSystem()
    
    # API Gateway receives request
    gateway_tracer = system.get_tracer("api-gateway")
    gateway_span = gateway_tracer.start_span("handle_request")
    gateway_span.set_tag("http.method", "GET")
    gateway_span.set_tag("http.path", "/api/users/123")
    
    # API Gateway calls User Service
    time.sleep(0.01)  # Simulate network latency
    user_tracer = system.get_tracer("user-service")
    user_context = gateway_tracer.inject_context(gateway_span)
    user_span = user_tracer.start_span("get_user", user_context)
    user_span.set_tag("user.id", "123")
    
    # User Service queries database
    time.sleep(0.02)  # Simulate DB query
    db_context = user_tracer.inject_context(user_span)
    db_span = user_tracer.start_span("db_query", db_context)
    db_span.set_tag("db.type", "postgresql")
    db_span.set_tag("db.statement", "SELECT * FROM users WHERE id = ?")
    time.sleep(0.015)
    user_tracer.finish_span(db_span)
    
    # User Service calls Auth Service
    auth_tracer = system.get_tracer("auth-service")
    auth_context = user_tracer.inject_context(user_span)
    auth_span = auth_tracer.start_span("check_permissions", auth_context)
    auth_span.set_tag("permissions", ["read", "write"])
    time.sleep(0.005)
    auth_tracer.finish_span(auth_span)
    
    # Complete the spans
    user_tracer.finish_span(user_span)
    gateway_tracer.finish_span(gateway_span)
    
    # Print the trace
    print("Distributed Trace:")
    system.print_trace(gateway_span.trace_id)
    
    return system

# Run simulation
simulate_request()
```

## Resource Management Challenges

### 🟢 Challenge 7: CPU Throttling Calculator

**Problem:**
Calculate CPU throttling percentage given cgroup statistics.

**Solution:**
```python
def calculate_cpu_throttling(stats):
    """
    Calculate CPU throttling percentage from cgroup stats
    
    Args:
        stats: dict with 'nr_periods', 'nr_throttled', 'throttled_time'
    
    Returns:
        dict with throttling metrics
    """
    nr_periods = stats.get('nr_periods', 0)
    nr_throttled = stats.get('nr_throttled', 0)
    throttled_time = stats.get('throttled_time', 0)  # in nanoseconds
    
    if nr_periods == 0:
        return {
            'throttle_percentage': 0,
            'throttled_periods_percentage': 0,
            'avg_throttle_time_ms': 0
        }
    
    throttle_percentage = (nr_throttled / nr_periods) * 100
    avg_throttle_time_ms = (throttled_time / nr_throttled / 1_000_000 
                           if nr_throttled > 0 else 0)
    
    return {
        'throttle_percentage': round(throttle_percentage, 2),
        'throttled_periods_percentage': throttle_percentage,
        'avg_throttle_time_ms': round(avg_throttle_time_ms, 2),
        'total_throttled_seconds': throttled_time / 1_000_000_000
    }

# Test cases
test_stats = [
    {
        'nr_periods': 1000,
        'nr_throttled': 250,
        'throttled_time': 5_000_000_000  # 5 seconds in nanoseconds
    },
    {
        'nr_periods': 0,
        'nr_throttled': 0,
        'throttled_time': 0
    }
]

for stats in test_stats:
    result = calculate_cpu_throttling(stats)
    print(f"Stats: {stats}")
    print(f"Result: {result}\n")
```

### 🟡 Challenge 8: Memory Pool Allocator

**Problem:**
Implement a simple memory pool allocator that reduces fragmentation.

**Solution:**
```python
class MemoryBlock:
    def __init__(self, start, size):
        self.start = start
        self.size = size
        self.is_free = True
        self.next = None
        self.prev = None

class MemoryPool:
    def __init__(self, total_size, min_block_size=16):
        self.total_size = total_size
        self.min_block_size = min_block_size
        
        # Initialize with one large free block
        self.head = MemoryBlock(0, total_size)
        self.allocations = {}  # allocation_id -> block
    
    def allocate(self, size, allocation_id):
        """Allocate memory of given size"""
        # Round up to minimum block size
        size = max(size, self.min_block_size)
        
        # Find first fit
        current = self.head
        while current:
            if current.is_free and current.size >= size:
                # Found suitable block
                if current.size > size + self.min_block_size:
                    # Split block
                    new_block = MemoryBlock(
                        current.start + size,
                        current.size - size
                    )
                    new_block.next = current.next
                    new_block.prev = current
                    if current.next:
                        current.next.prev = new_block
                    current.next = new_block
                    current.size = size
                
                current.is_free = False
                self.allocations[allocation_id] = current
                return current.start
            
            current = current.next
        
        return None  # No suitable block found
    
    def free(self, allocation_id):
        """Free allocated memory"""
        if allocation_id not in self.allocations:
            return False
        
        block = self.allocations[allocation_id]
        block.is_free = True
        del self.allocations[allocation_id]
        
        # Coalesce with adjacent free blocks
        # Check next block
        if block.next and block.next.is_free:
            block.size += block.next.size
            block.next = block.next.next
            if block.next:
                block.next.prev = block
        
        # Check previous block
        if block.prev and block.prev.is_free:
            block.prev.size += block.size
            block.prev.next = block.next
            if block.next:
                block.next.prev = block.prev
        
        return True
    
    def get_stats(self):
        """Get memory pool statistics"""
        total_allocated = 0
        total_free = 0
        free_blocks = 0
        allocated_blocks = 0
        largest_free_block = 0
        
        current = self.head
        while current:
            if current.is_free:
                total_free += current.size
                free_blocks += 1
                largest_free_block = max(largest_free_block, current.size)
            else:
                total_allocated += current.size
                allocated_blocks += 1
            current = current.next
        
        return {
            'total_size': self.total_size,
            'allocated': total_allocated,
            'free': total_free,
            'allocated_blocks': allocated_blocks,
            'free_blocks': free_blocks,
            'largest_free_block': largest_free_block,
            'fragmentation': (free_blocks - 1) / allocated_blocks 
                           if allocated_blocks > 0 else 0
        }
    
    def visualize(self):
        """Simple visualization of memory pool"""
        current = self.head
        blocks = []
        while current:
            status = "FREE" if current.is_free else "USED"
            blocks.append(f"[{current.start}:{current.size} {status}]")
            current = current.next
        return " -> ".join(blocks)

# Test the memory pool
def test_memory_pool():
    pool = MemoryPool(1024)
    
    # Allocate some memory
    addr1 = pool.allocate(100, "app1")
    addr2 = pool.allocate(200, "app2")
    addr3 = pool.allocate(150, "app3")
    
    print(f"Allocated app1 at: {addr1}")
    print(f"Allocated app2 at: {addr2}")
    print(f"Allocated app3 at: {addr3}")
    print(f"Pool state: {pool.visualize()}")
    print(f"Stats: {pool.get_stats()}")
    
    # Free some memory
    pool.free("app2")
    print(f"\nAfter freeing app2:")
    print(f"Pool state: {pool.visualize()}")
    
    # Allocate again (should reuse freed space)
    addr4 = pool.allocate(180, "app4")
    print(f"\nAllocated app4 at: {addr4}")
    print(f"Pool state: {pool.visualize()}")
    print(f"Final stats: {pool.get_stats()}")

test_memory_pool()
```

## Security and Compliance Challenges

### 🟢 Challenge 9: Secret Scanner

**Problem:**
Scan configuration files for potential secrets and sensitive data.

**Solution:**
```python
import re

class SecretScanner:
    def __init__(self):
        # Common secret patterns
        self.patterns = {
            'aws_access_key': {
                'pattern': r'AKIA[0-9A-Z]{16}',
                'severity': 'critical'
            },
            'aws_secret_key': {
                'pattern': r'(?i)aws(.{0,20})?(?-i)['\"][0-9a-zA-Z/+=]{40}['\"]',
                'severity': 'critical'
            },
            'api_key': {
                'pattern': r'(?i)api[_\-\s]?key['\"]?\s*[:=]\s*['\"][a-zA-Z0-9_\-]{20,}['\"]',
                'severity': 'high'
            },
            'private_key': {
                'pattern': r'-----BEGIN (RSA |EC )?PRIVATE KEY-----',
                'severity': 'critical'
            },
            'password': {
                'pattern': r'(?i)password['\"]?\s*[:=]\s*['\"][^'\"]{8,}['\"]',
                'severity': 'high'
            },
            'github_token': {
                'pattern': r'ghp_[a-zA-Z0-9]{36}',
                'severity': 'critical'
            },
            'generic_secret': {
                'pattern': r'(?i)(secret|token|key)['\"]?\s*[:=]\s*['\"][a-zA-Z0-9_\-]{16,}['\"]',
                'severity': 'medium'
            }
        }
        
        # Whitelisted patterns (false positives)
        self.whitelist_patterns = [
            r'(?i)example',
            r'(?i)placeholder',
            r'(?i)your[_\-]?',
            r'(?i)my[_\-]?',
            r'<[^>]+>',  # Template variables
            r'\$\{[^}]+\}'  # Environment variables
        ]
    
    def scan_text(self, text, filename=''):
        """Scan text for secrets"""
        findings = []
        
        for line_num, line in enumerate(text.split('\n'), 1):
            # Skip comments
            if line.strip().startswith('#') or line.strip().startswith('//'):
                continue
            
            for secret_type, config in self.patterns.items():
                pattern = config['pattern']
                matches = re.finditer(pattern, line)
                
                for match in matches:
                    # Check if whitelisted
                    if self._is_whitelisted(match.group(0)):
                        continue
                    
                    finding = {
                        'type': secret_type,
                        'severity': config['severity'],
                        'file': filename,
                        'line': line_num,
                        'column': match.start() + 1,
                        'matched_text': self._redact(match.group(0)),
                        'line_content': line.strip()
                    }
                    findings.append(finding)
        
        return findings
    
    def _is_whitelisted(self, text):
        """Check if text matches whitelist patterns"""
        for pattern in self.whitelist_patterns:
            if re.search(pattern, text):
                return True
        return False
    
    def _redact(self, secret):
        """Redact sensitive part of secret"""
        if len(secret) <= 8:
            return '*' * len(secret)
        
        visible_chars = 4
        return (secret[:visible_chars] + 
                '*' * (len(secret) - visible_chars * 2) + 
                secret[-visible_chars:])
    
    def scan_file(self, filepath):
        """Scan a file for secrets"""
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            return self.scan_text(content, filepath)
        except Exception as e:
            return [{'error': str(e), 'file': filepath}]

# Test the scanner
def test_secret_scanner():
    scanner = SecretScanner()
    
    # Test configuration
    test_config = '''
# AWS Configuration
aws_access_key = "AKIAIOSFODNN7EXAMPLE"
aws_secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# API Configuration
api_key = "sk-1234567890abcdef1234567890abcdef"
database_password = "super_secret_password_123"

# This is safe (example)
example_key = "your-api-key-here"
password = "placeholder"

# GitHub
github_token = ghp_1234567890abcdef1234567890abcdef1234
'''
    
    findings = scanner.scan_text(test_config, 'config.yml')
    
    print("Security Scan Results:")
    print(f"Found {len(findings)} potential secrets\n")
    
    for finding in findings:
        print(f"[{finding['severity'].upper()}] {finding['type']}")
        print(f"  File: {finding['file']}:{finding['line']}:{finding['column']}")
        print(f"  Match: {finding['matched_text']}")
        print(f"  Line: {finding['line_content'][:50]}...")
        print()

test_secret_scanner()
```

### 🟡 Challenge 10: RBAC Policy Validator

**Problem:**
Validate and analyze Role-Based Access Control policies for security issues.

**Solution:**
```python
from collections import defaultdict

class RBACValidator:
    def __init__(self):
        self.roles = {}
        self.users = {}
        self.resources = set()
        self.dangerous_permissions = {
            '*': 'Wildcard permission - grants all access',
            'admin:*': 'Admin wildcard - full admin access',
            'delete:*': 'Delete wildcard - can delete anything',
            'iam:*': 'IAM wildcard - can modify permissions'
        }
    
    def add_role(self, role_name, permissions):
        """Add a role with permissions"""
        self.roles[role_name] = set(permissions)
        for perm in permissions:
            resource = perm.split(':')[0]
            self.resources.add(resource)
    
    def add_user(self, username, roles):
        """Assign roles to a user"""
        self.users[username] = set(roles)
    
    def validate(self):
        """Validate RBAC configuration"""
        issues = []
        
        # Check for overly permissive roles
        for role, perms in self.roles.items():
            dangerous = self._check_dangerous_permissions(perms)
            if dangerous:
                issues.append({
                    'type': 'dangerous_permission',
                    'severity': 'high',
                    'role': role,
                    'details': dangerous
                })
        
        # Check for privilege escalation paths
        escalation_paths = self._find_privilege_escalation()
        if escalation_paths:
            issues.append({
                'type': 'privilege_escalation',
                'severity': 'critical',
                'details': escalation_paths
            })
        
        # Check for unused roles
        used_roles = set()
        for user_roles in self.users.values():
            used_roles.update(user_roles)
        
        unused_roles = set(self.roles.keys()) - used_roles
        if unused_roles:
            issues.append({
                'type': 'unused_roles',
                'severity': 'low',
                'roles': list(unused_roles)
            })
        
        # Check for separation of duties violations
        sod_violations = self._check_separation_of_duties()
        if sod_violations:
            issues.append({
                'type': 'separation_of_duties',
                'severity': 'medium',
                'details': sod_violations
            })
        
        return issues
    
    def _check_dangerous_permissions(self, permissions):
        """Check for dangerous permission patterns"""
        dangerous = []
        for perm in permissions:
            if perm in self.dangerous_permissions:
                dangerous.append({
                    'permission': perm,
                    'reason': self.dangerous_permissions[perm]
                })
            # Check for overly broad patterns
            elif perm.endswith(':*'):
                dangerous.append({
                    'permission': perm,
                    'reason': 'Wildcard action on resource'
                })
        return dangerous
    
    def _find_privilege_escalation(self):
        """Find potential privilege escalation paths"""
        escalation_paths = []
        
        for role, perms in self.roles.items():
            # Check if role can modify IAM
            iam_perms = [p for p in perms if p.startswith('iam:')]
            if any('create' in p or 'update' in p or 'attach' in p 
                   for p in iam_perms):
                escalation_paths.append({
                    'role': role,
                    'reason': 'Can modify IAM permissions',
                    'permissions': iam_perms
                })
        
        return escalation_paths
    
    def _check_separation_of_duties(self):
        """Check for separation of duties violations"""
        violations = []
        
        # Define conflicting permission sets
        conflicts = [
            (['payment:create', 'payment:approve'], 
             'Can both create and approve payments'),
            (['audit:write', 'audit:delete'], 
             'Can both write and delete audit logs'),
            (['user:create', 'user:delete', 'user:modify'], 
             'Full user management capabilities')
        ]
        
        for user, user_roles in self.users.items():
            user_perms = set()
            for role in user_roles:
                if role in self.roles:
                    user_perms.update(self.roles[role])
            
            for conflict_perms, reason in conflicts:
                if all(perm in user_perms for perm in conflict_perms):
                    violations.append({
                        'user': user,
                        'reason': reason,
                        'permissions': conflict_perms
                    })
        
        return violations
    
    def get_user_permissions(self, username):
        """Get all permissions for a user"""
        if username not in self.users:
            return set()
        
        permissions = set()
        for role in self.users[username]:
            if role in self.roles:
                permissions.update(self.roles[role])
        
        return permissions
    
    def check_access(self, username, resource, action):
        """Check if user has access to perform action on resource"""
        user_perms = self.get_user_permissions(username)
        
        # Check exact match
        if f"{resource}:{action}" in user_perms:
            return True
        
        # Check wildcards
        if "*" in user_perms:
            return True
        if f"{resource}:*" in user_perms:
            return True
        if f"*:{action}" in user_perms:
            return True
        
        return False

# Test the RBAC validator
def test_rbac_validator():
    validator = RBACValidator()
    
    # Define roles
    validator.add_role('admin', ['*'])
    validator.add_role('developer', [
        'code:read', 'code:write', 'deploy:dev'
    ])
    validator.add_role('deployer', [
        'deploy:*', 'config:read'
    ])
    validator.add_role('finance', [
        'payment:create', 'payment:approve', 'report:read'
    ])
    validator.add_role('auditor', [
        'audit:write', 'audit:delete', 'report:read'
    ])
    validator.add_role('unused_role', ['temp:read'])
    
    # Assign roles to users
    validator.add_user('alice', ['admin'])
    validator.add_user('bob', ['developer', 'deployer'])
    validator.add_user('charlie', ['finance'])
    validator.add_user('david', ['auditor'])
    
    # Validate configuration
    issues = validator.validate()
    
    print("RBAC Validation Results:")
    print(f"Found {len(issues)} issues\n")
    
    for issue in issues:
        print(f"[{issue['severity'].upper()}] {issue['type']}")
        if issue['type'] == 'dangerous_permission':
            print(f"  Role: {issue['role']}")
            for detail in issue['details']:
                print(f"  - {detail['permission']}: {detail['reason']}")
        elif issue['type'] == 'separation_of_duties':
            for violation in issue['details']:
                print(f"  User: {violation['user']}")
                print(f"  Reason: {violation['reason']}")
        else:
            print(f"  Details: {issue}")
        print()
    
    # Test access checks
    print("\nAccess Check Examples:")
    test_cases = [
        ('alice', 'payment', 'create', True),
        ('bob', 'deploy', 'prod', True),
        ('charlie', 'audit', 'write', False),
        ('david', 'audit', 'delete', True)
    ]
    
    for user, resource, action, expected in test_cases:
        result = validator.check_access(user, resource, action)
        status = "✓" if result == expected else "✗"
        print(f"{status} {user} -> {resource}:{action} = {result}")

test_rbac_validator()
```

## Interview Tips for Coding Challenges

### 1. Before You Start Coding
- **Clarify requirements**: Ask about edge cases, scale, and constraints
- **Discuss the approach**: Explain your solution before coding
- **Consider tradeoffs**: Time vs space complexity, accuracy vs performance

### 2. While Coding
- **Write clean code**: Use meaningful variable names and proper structure
- **Handle errors**: Show you think about production scenarios
- **Add comments**: Explain complex logic
- **Test as you go**: Write simple test cases

### 3. After Coding
- **Review your solution**: Look for bugs or optimizations
- **Discuss complexity**: Time and space complexity analysis
- **Suggest improvements**: Show you can iterate on solutions
- **Consider scale**: How would this work with millions of requests?

## Practice Resources

### Online Platforms
- 🎮 [LeetCode](https://leetcode.com/) - Filter by "System Design" tag
- 🎮 [HackerRank](https://www.hackerrank.com/) - DevOps and Linux Shell sections
- 🎮 [Exercism](https://exercism.io/) - Language-specific tracks
- 🎮 [CodeSignal](https://codesignal.com/) - Real company assessments

### Books for Practice
- 📚 [The Linux Programming Interface](https://man7.org/tlpi/)
- 📚 [Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/)
- 📚 [Designing Data-Intensive Applications](https://dataintensive.net/)

### GitHub Repositories
- 📖 [System Design Interview](https://github.com/checkcheckzz/system-design-interview)
- 📖 [DevOps Exercises](https://github.com/bregman-arie/devops-exercises)
- 📖 [SRE Interview Prep Guide](https://github.com/mxssl/sre-interview-prep-guide)

Remember: Platform engineering coding challenges are about demonstrating your ability to solve real infrastructure problems. Focus on reliability, scalability, and operational excellence in your solutions.