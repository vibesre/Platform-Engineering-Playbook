---
title: Distributed Systems
sidebar_position: 2
---

# Distributed Systems for Platform Engineers

<GitHubButtons />
Master distributed systems concepts essential for platform engineering interviews.

## 🎯 Interview Focus Areas

### Most Asked Topics
1. **CAP Theorem** - Trade-offs and real-world applications
2. **Consistency Models** - Strong, eventual, weak consistency
3. **Consensus Algorithms** - Raft, Paxos, Byzantine fault tolerance
4. **Distributed Transactions** - 2PC, saga patterns
5. **Failure Handling** - Fault tolerance, circuit breakers

## Core Concepts

### CAP Theorem

The CAP theorem states that a distributed system can only guarantee two of:
- **Consistency**: All nodes see the same data simultaneously
- **Availability**: System remains operational
- **Partition Tolerance**: System continues during network failures

```
During Network Partition:
┌─────────────┐     ✗     ┌─────────────┐
│   Node A    │ ────────► │   Node B    │
│ (Updated)   │           │ (Not Updated)│
└─────────────┘           └─────────────┘

Choose:
- CP: Refuse writes until partition heals (Consistency)
- AP: Accept writes, reconcile later (Availability)
```

### Real-World CAP Examples

| System | Choice | Trade-off |
|--------|--------|-----------|
| **Banking** | CP | Consistency over availability |
| **Social Media** | AP | Available but may show stale data |
| **Zookeeper** | CP | Coordination requires consistency |
| **Cassandra** | AP | Tunable consistency |
| **DynamoDB** | AP | Eventually consistent by default |

## Consistency Models

### Strong Consistency
All reads return the most recent write.

```python
# Example: Bank transfer must be strongly consistent
def transfer_money(from_account, to_account, amount):
    with distributed_transaction():
        from_balance = read_balance(from_account)
        if from_balance >= amount:
            write_balance(from_account, from_balance - amount)
            to_balance = read_balance(to_account)
            write_balance(to_account, to_balance + amount)
            commit()
        else:
            abort()
```

### Eventual Consistency
System will become consistent over time.

```python
# Example: Social media likes can be eventually consistent
def increment_likes(post_id):
    # Write to local replica
    local_db.increment(f"likes:{post_id}")
    
    # Async replicate to other regions
    async_replicate({
        'operation': 'increment',
        'key': f"likes:{post_id}",
        'timestamp': time.now()
    })
```

### Causal Consistency
Operations that are causally related are seen in the same order.

```
User A posts → User B comments → User C likes comment
Everyone must see these in this order
```

## Consensus Algorithms

### Raft Consensus

Raft ensures distributed systems agree on values through leader election.

```python
# Simplified Raft leader election
class RaftNode:
    def __init__(self, node_id):
        self.state = "FOLLOWER"
        self.current_term = 0
        self.voted_for = None
        self.log = []
    
    def start_election(self):
        self.state = "CANDIDATE"
        self.current_term += 1
        self.voted_for = self.node_id
        
        votes = 1  # Vote for self
        for node in other_nodes:
            if node.request_vote(self.current_term, self.node_id):
                votes += 1
        
        if votes > len(all_nodes) / 2:
            self.state = "LEADER"
            self.send_heartbeats()
```

### Two-Phase Commit (2PC)

Ensures all nodes commit or all abort.

```
Coordinator                 Participants
    │                           │
    ├──── PREPARE ─────────────►│
    │                           │
    │◄──── VOTE (YES/NO) ───────┤
    │                           │
    ├──── COMMIT/ABORT ────────►│
    │                           │
    │◄──── ACK ─────────────────┤
```

**Problems with 2PC:**
- Blocking if coordinator fails
- No fault tolerance
- Performance overhead

### Saga Pattern

Alternative to 2PC for long-running transactions.

```python
# Order processing saga
class OrderSaga:
    def __init__(self):
        self.steps = [
            (self.reserve_inventory, self.cancel_inventory),
            (self.charge_payment, self.refund_payment),
            (self.create_shipment, self.cancel_shipment)
        ]
    
    def execute(self, order):
        completed_steps = []
        
        try:
            for step, compensate in self.steps:
                result = step(order)
                completed_steps.append((compensate, result))
        except Exception as e:
            # Compensate in reverse order
            for compensate, result in reversed(completed_steps):
                compensate(result)
            raise
```

## Distributed System Patterns

### Circuit Breaker

Prevents cascading failures.

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = 'CLOSED'
    
    def call(self, func, *args, **kwargs):
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.timeout:
                self.state = 'HALF_OPEN'
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            if self.state == 'HALF_OPEN':
                self.state = 'CLOSED'
                self.failures = 0
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            
            if self.failures >= self.failure_threshold:
                self.state = 'OPEN'
            raise
```

### Bulkhead Pattern

Isolate resources to prevent total failure.

```python
# Thread pool bulkhead
from concurrent.futures import ThreadPoolExecutor

class BulkheadExecutor:
    def __init__(self):
        self.executors = {
            'critical': ThreadPoolExecutor(max_workers=10),
            'normal': ThreadPoolExecutor(max_workers=5),
            'batch': ThreadPoolExecutor(max_workers=2)
        }
    
    def submit(self, priority, func, *args):
        return self.executors[priority].submit(func, *args)
```

### Retry with Backoff

Handle transient failures gracefully.

```python
def exponential_backoff_retry(func, max_retries=3, base_delay=1):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            time.sleep(delay)
```

## Clock Synchronization

### Logical Clocks (Lamport Timestamps)

Order events without synchronized physical clocks.

```python
class LamportClock:
    def __init__(self):
        self.time = 0
    
    def increment(self):
        self.time += 1
        return self.time
    
    def update(self, received_time):
        self.time = max(self.time, received_time) + 1
        return self.time
```

### Vector Clocks

Track causality between events.

```python
class VectorClock:
    def __init__(self, node_id, num_nodes):
        self.node_id = node_id
        self.clock = [0] * num_nodes
    
    def increment(self):
        self.clock[self.node_id] += 1
        return self.clock.copy()
    
    def update(self, other_clock):
        for i in range(len(self.clock)):
            self.clock[i] = max(self.clock[i], other_clock[i])
        self.increment()
```

## Distributed Storage

### Consistent Hashing

Distribute data across nodes with minimal reshuffling.

```python
import hashlib

class ConsistentHash:
    def __init__(self, nodes, virtual_nodes=150):
        self.nodes = nodes
        self.virtual_nodes = virtual_nodes
        self.ring = {}
        self._build_ring()
    
    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    def _build_ring(self):
        for node in self.nodes:
            for i in range(self.virtual_nodes):
                virtual_key = f"{node}:{i}"
                hash_value = self._hash(virtual_key)
                self.ring[hash_value] = node
    
    def get_node(self, key):
        if not self.ring:
            return None
        
        hash_value = self._hash(key)
        # Find the first node clockwise from the key
        for node_hash in sorted(self.ring.keys()):
            if node_hash >= hash_value:
                return self.ring[node_hash]
        
        # Wrap around
        return self.ring[min(self.ring.keys())]
```

### Replication Strategies

**Master-Slave Replication**
```
┌────────┐
│ Master │ ──────► Write
└───┬────┘
    │ Replicate
┌───▼────┐ ┌────────┐ ┌────────┐
│ Slave1 │ │ Slave2 │ │ Slave3 │ ──► Read
└────────┘ └────────┘ └────────┘
```

**Multi-Master Replication**
```
┌────────┐ ◄──► ┌────────┐
│Master1 │      │Master2 │
└────────┘ ◄──► └────────┘
     ▲              ▲
     └──────────────┘
    Conflict Resolution
```

## Common Interview Questions

### Q1: "Design a distributed cache"

```python
class DistributedCache:
    def __init__(self, nodes):
        self.consistent_hash = ConsistentHash(nodes)
        self.local_cache = {}
        self.replication_factor = 3
    
    def get(self, key):
        # Try local cache first
        if key in self.local_cache:
            return self.local_cache[key]
        
        # Find responsible nodes
        nodes = self.get_nodes_for_key(key)
        
        # Try each replica
        for node in nodes:
            try:
                value = node.get(key)
                if value:
                    self.local_cache[key] = value
                    return value
            except:
                continue
        
        return None
    
    def put(self, key, value):
        nodes = self.get_nodes_for_key(key)
        
        # Write to all replicas
        successful_writes = 0
        for node in nodes:
            try:
                node.put(key, value)
                successful_writes += 1
            except:
                pass
        
        # Require quorum
        if successful_writes < len(nodes) // 2 + 1:
            raise Exception("Failed to achieve write quorum")
```

### Q2: "How do you handle split-brain in distributed systems?"

**Solutions:**
1. **Quorum-based decisions**: Require majority for operations
2. **Fencing tokens**: Monotonically increasing tokens
3. **STONITH** (Shoot The Other Node In The Head)
4. **External arbitrator**: Zookeeper, etcd
5. **Witness nodes**: Lightweight tie-breakers

### Q3: "Explain distributed tracing"

```python
class DistributedTrace:
    def __init__(self, trace_id=None):
        self.trace_id = trace_id or generate_id()
        self.spans = []
    
    def start_span(self, operation):
        span = {
            'span_id': generate_id(),
            'trace_id': self.trace_id,
            'operation': operation,
            'start_time': time.time(),
            'parent_id': self.current_span_id if hasattr(self, 'current_span_id') else None
        }
        self.spans.append(span)
        self.current_span_id = span['span_id']
        return span
    
    def end_span(self, span):
        span['end_time'] = time.time()
        span['duration'] = span['end_time'] - span['start_time']
```

## Best Practices

### 1. Design for Failure
- Assume nodes will fail
- Assume network will partition
- Build in redundancy
- Test failure scenarios

### 2. Monitoring & Observability
- Distributed tracing
- Centralized logging
- Metrics aggregation
- Health checks

### 3. Gradual Rollouts
- Canary deployments
- Feature flags
- Blue-green deployments
- Rollback capabilities

## Resources

- 📚 [Designing Data-Intensive Applications](https://dataintensive.net/)
- 📚 [Distributed Systems: Principles and Paradigms](https://www.distributed-systems.net/)
- 📖 [The Google File System](https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf)
- 🎥 [MIT 6.824: Distributed Systems](https://www.youtube.com/playlist?list=PLrw6a1wE39_tb2fErI4-WkMbsvGQk9_UB)

---

*Interview tip: When discussing distributed systems, always acknowledge trade-offs. There's no perfect solution - explain why you chose specific approaches for given requirements.*