# Lesson Outline: Episode 5 - StatefulSets & Persistent Storage

## Metadata
- **Course**: Kubernetes Production Mastery
- **Episode**: 5 of 10
- **Duration**: 15 minutes
- **Type**: Core Concept
- **Prerequisites**: Episode 1 (Production Mindset), Episode 4 (Health Checks), Basic understanding of Deployments
- **Template**: Core Concept (Template 2)

## Learning Objectives

By the end of this lesson, learners will be able to:
1. **Determine** when to use StatefulSets vs Deployments with PVCs based on application requirements
2. **Configure** dynamic volume provisioning using Storage Classes and understand CSI drivers
3. **Diagnose** common storage failures including PVC stuck Pending and volume mounting issues

Success criteria:
- Can explain the three key differences between StatefulSets and Deployments
- Can identify which storage pattern to use for a given workload (database, cache, queue, stateless app)
- Can troubleshoot PVC provisioning failures using kubectl commands
- Can configure a volumeClaimTemplate for a StatefulSet

## Spaced Repetition Plan

**Introduced** (concepts to repeat later):
- StatefulSets and stable network identity → Episode 6 (networking, DNS resolution)
- PersistentVolumes and Claims → Episode 7 (monitoring storage metrics)
- Storage Classes and dynamic provisioning → Episode 8 (cost optimization)
- Velero for backups → Episode 10 (disaster recovery at scale)
- Database operators → Episode 10 (multi-cluster data)

**Reinforced** (callbacks from earlier episodes):
- Pod lifecycle from Episode 1 → How StatefulSets manage pod ordering
- Resource constraints from Episode 2 → Storage quotas and PVC limits
- Health checks from Episode 4 → Stateful apps need careful probe config because of initialization time
- kubectl troubleshooting from Episode 4 → Apply same workflow to storage debugging

## Lesson Flow

### 1. Recall & Connection (1.5 min)

**Opening Callback**: "In Episode 4, we mastered health checks - startup, readiness, and liveness probes. We learned that stateful applications need careful probe configuration because they have state to protect. But here's the question we didn't answer: where DOES that state live? And what happens when a pod restarts?"

**Active Recall Prompt**: "Before we continue, try to recall: What happens to a pod's filesystem when it restarts?" [PAUSE 3 sec] "That's right - it's completely wiped. Containers are ephemeral by design. So how do we run databases in Kubernetes?"

**Today's Connection**: "That's exactly what we're exploring today - persistent storage and StatefulSets. By the end, you'll understand when you need StatefulSets versus regular Deployments, how Kubernetes storage actually works, and how to debug the most common storage failures."

### 2. Learning Objectives (30 sec)

Today you'll learn to:
- Decide between StatefulSets and Deployments based on your application's needs
- Configure dynamic storage provisioning with Storage Classes
- Troubleshoot PVCs stuck in Pending and volumes that won't mount
- Understand when to use Kubernetes-hosted databases versus cloud-managed options

### 3. Concept Introduction: When Persistence Matters (2 min)

**The Core Question**: "Most applications fall into two categories: stateless and stateful. Let's be crystal clear about what this means in production."

**Stateless Applications** (can use Deployments):
- No local state: web servers, API gateways, worker processes
- Identity doesn't matter: pod-abc-123 is interchangeable with pod-abc-456
- Can be killed and recreated instantly
- Scale up/down in any order
- Example: Your React frontend, REST API, background job processor

**Stateful Applications** (need StatefulSets):
- Maintain local state: databases, caches, message queues
- Identity DOES matter: postgres-0 is the leader, postgres-1 is a replica
- Need stable network identity: postgres-0.postgres.default.svc.cluster.local
- Must start/stop in order: leader before replicas
- Each instance needs its own persistent storage
- Example: PostgreSQL, Redis, Kafka, Elasticsearch

**Key Insight**: "Here's what trips people up: you CAN run a database in a Deployment with a PVC. It'll work... until it doesn't. When the pod moves to another node, the PVC might not follow. When you scale up, all replicas share the same PVC. When you need ordered startup, you have no control. StatefulSets solve all of this."

### 4. StatefulSets Deep Dive: The Three Guarantees (3 min)

**Teaching Approach**: Three concrete guarantees with examples

**Guarantee #1: Stable Network Identity**
- Pods get predictable names: `postgres-0`, `postgres-1`, `postgres-2` (not random hashes)
- Stable DNS names that don't change: `postgres-0.postgres.default.svc.cluster.local`
- **Why this matters**: Your primary database is always `postgres-0`. Replicas can always find the leader at the same address.
- **Analogy**: "Like your home address. Even if you redecorate (pod restart), your address stays the same so mail reaches you."

**Guarantee #2: Ordered Deployment and Scaling**
- Pods created sequentially: 0 → 1 → 2
- Pod N must be Running and Ready before N+1 starts
- Scaling down: reverse order (2 → 1 → 0)
- **Why this matters**: Database leader must be up before replicas. Shutdown: replicas first, leader last.
- **Think-Aloud**: "Why this order? Imagine starting postgres-1 (replica) before postgres-0 (leader). Replica can't replicate from a leader that doesn't exist yet. Creates split-brain scenarios."

**Guarantee #3: Persistent Storage Per Pod**
- Each pod gets its own PVC from volumeClaimTemplate
- PVC persists even if pod deleted
- If pod rescheduled, reattaches to same PVC
- **Why this matters**: postgres-0 always gets postgres-0's data, never postgres-1's data
- **Visual**: "Three filing cabinets (PVCs), three employees (pods). Each employee has their own cabinet. If employee leaves and returns, they get their same cabinet back - not someone else's."

**Configuration Example**:
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: "postgres"  # Headless service for DNS
  replicas: 3
  selector:
    matchLabels:
      app: postgres
  template:
    spec:
      containers:
      - name: postgres
        image: postgres:15
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:  # Key difference from Deployment
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: "fast-ssd"
      resources:
        requests:
          storage: 100Gi
```

**Key Point**: "Notice `volumeClaimTemplates` (plural). This creates a SEPARATE PVC for each pod. Deployment would use `volumes` (singular) - same volume for all pods."

### 5. Storage Architecture: PV, PVC, and Storage Classes (3.5 min)

**Mental Model**: "Think of Kubernetes storage like a vending machine"

**StorageClass** (The Vending Machine Configuration):
- Defines: Which cloud provider? SSD or HDD? Replication? Encryption?
- Examples: `gp3-encrypted`, `fast-ssd`, `slow-hdd`, `replicated-storage`
- **Analogy**: "Like different vending machine types: snacks, drinks, hot food. Each type knows how to dispense different items."

**PersistentVolumeClaim (PVC)** (The Request):
- Your application says: "I need 100GB of fast-ssd storage"
- PVC is namespace-scoped, application-owned
- **Analogy**: "You insert money and press B3 for chips. This is your claim for chips."

**PersistentVolume (PV)** (The Actual Storage):
- The cloud provider creates actual EBS volume, GCP disk, or Azure disk
- Cluster-scoped, admin-managed (or dynamically provisioned)
- **Analogy**: "The actual bag of chips that drops down. Real, physical item."

**CSI Driver** (The Mechanism):
- Container Storage Interface - standardized plugin
- Each cloud has CSI driver: aws-ebs-csi-driver, gcp-pd-csi-driver, azure-disk-csi-driver
- **Why this matters**: "Before CSI, every storage vendor had custom integration. Now standardized. Like USB-C vs proprietary chargers."

**The Flow**:
1. You create PVC: "I need 100GB of StorageClass fast-ssd"
2. Kubernetes checks: Is there a StorageClass named "fast-ssd"?
3. StorageClass invokes CSI driver: "Create EBS gp3 volume, 100GB, encrypted"
4. Cloud provider creates volume → becomes PersistentVolume
5. PV binds to PVC → your pod can use it
6. **Total time**: Usually 30-60 seconds for dynamic provisioning

**Access Modes** (Critical concept):
- **ReadWriteOnce (RWO)**: Single node can mount read-write (most common, required for databases)
- **ReadOnlyMany (ROX)**: Multiple nodes read-only (rare, config files)
- **ReadWriteMany (RWX)**: Multiple nodes read-write (rare, needs NFS/EFS, slower)

**Common Confusion**: "RWO doesn't mean 'one pod'. Means one NODE. Multiple pods on same node can share RWO volume. But if pods on different nodes, RWO won't work."

### 6. Real-World Application: PostgreSQL with Persistent Storage (2.5 min)

**Scenario**: "You're deploying PostgreSQL for your e-commerce platform. 3-node cluster, primary-replica setup."

**Requirements**:
- Primary database at stable address
- 2 replicas for read scaling
- Each needs 200GB storage
- SSD for performance
- Ordered startup (primary → replicas)
- Survives pod restarts and node failures

**Implementation Walkthrough**:

**Step 1: Create StorageClass** (if not exists):
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: ebs.csi.aws.com  # AWS example
parameters:
  type: gp3
  encrypted: "true"
  iopsPerGB: "50"
volumeBindingMode: WaitForFirstConsumer  # Important for node affinity
```

**Step 2: Create Headless Service** (for stable DNS):
```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres
spec:
  clusterIP: None  # Headless
  selector:
    app: postgres
  ports:
  - port: 5432
```

**Step 3: Create StatefulSet** (shown in section 4)

**Step 4: Verify Storage**:
```bash
kubectl get pvc
# Shows: data-postgres-0, data-postgres-1, data-postgres-2

kubectl get pv
# Shows: pvc-abc123, pvc-def456, pvc-ghi789 (bound to PVCs)
```

**What Happens During Failures**:
- **Pod restart**: Pod deleted, recreated with same name, reattaches to same PVC → data intact
- **Node failure**: Pod rescheduled to new node, PVC follows → data intact (if RWO and single replica)
- **StatefulSet deletion**: Pods deleted, but PVCs persist → manual cleanup required (safety feature)

**Best Practice**: "Always set retention policy on PVCs. Use `persistentVolumeReclaimPolicy: Retain` for production databases so you don't accidentally delete data."

### 7. Common Mistakes and Storage Failures (2.5 min)

**Failure #1: PVC Stuck in Pending**

**Symptoms**: `kubectl get pvc` shows STATUS = Pending for minutes

**Common Causes**:
1. **No matching StorageClass**: PVC requests `fast-ssd`, but no StorageClass exists with that name
   - **Fix**: `kubectl get sc` to list available classes, update PVC
2. **Quota exceeded**: Namespace has storage quota, request exceeds limit
   - **Fix**: `kubectl describe ns <namespace>` check ResourceQuota
3. **No available PVs** (static provisioning): PVC needs 100GB, all PVs are 50GB
   - **Fix**: Use dynamic provisioning or create matching PV

**Debug Command**: `kubectl describe pvc <name>` - Events section shows exact error

---

**Failure #2: Volume Not Mounting**

**Symptoms**: Pod stuck in ContainerCreating, events show "FailedMount"

**Common Causes**:
1. **CSI driver not installed**: Cluster missing EBS CSI driver
   - **Fix**: Install CSI driver (required in modern K8s versions)
2. **Node and volume in different zones**: EBS volume in us-east-1a, pod scheduled to node in us-east-1b (RWO volumes are zone-specific)
   - **Fix**: Use `volumeBindingMode: WaitForFirstConsumer` in StorageClass
3. **Volume already mounted elsewhere**: RWO volume attached to another node
   - **Fix**: Wait for node drain to complete, or force delete old pod

**Debug Commands**:
```bash
kubectl describe pod <name>  # Check Events
kubectl get pv <name> -o yaml  # Check nodeAffinity
kubectl get csinodes  # Verify CSI driver on nodes
```

---

**Failure #3: Can't Resize StatefulSet PVC**

**Problem**: "You created StatefulSet with 100GB per pod. Now need 200GB. Can't update volumeClaimTemplates."

**Why**: Kubernetes design limitation - volumeClaimTemplates are immutable

**Solutions**:
1. **Manual PVC expansion** (if StorageClass allows): Edit each PVC directly, increase size
   ```bash
   kubectl edit pvc data-postgres-0
   # Change: storage: 100Gi → 200Gi
   ```
2. **Recreate StatefulSet**: Delete StatefulSet (keep PVCs), create new one with larger size (advanced, requires zero-downtime strategy)
3. **Use database operator**: Operators handle PVC resizing automatically

**Lesson**: "Plan storage sizes carefully. Expansion is possible but manual. Shrinking is NOT possible."

---

**Mistake #4: Using Deployment Instead of StatefulSet**

**Symptom**: "I have a Deployment with a PVC. When I scale to 3 replicas, all pods try to write to same PVC. Database corruption."

**Fix**: Use StatefulSet with volumeClaimTemplates

**When Deployment + PVC IS okay**: ReadOnly workloads (config files, static assets)

---

**Mistake #5: No Backup Strategy**

**Problem**: "Persistent storage ≠ backed up. Node failure? Data survives. Accidental `DROP DATABASE`? Data GONE."

**Solution**: Use Velero for cluster backups
```bash
# Install Velero
velero backup create postgres-backup --selector app=postgres

# Schedule daily backups
velero schedule create daily-backup --schedule="0 2 * * *"
```

**Best Practice**: "Test restores monthly. Untested backups = no backups."

### 8. Decision Framework: StatefulSet vs Deployment vs Managed Service (1 min)

**Use StatefulSet when**:
- Need stable network identity (databases, distributed systems)
- Require ordered deployment/scaling (primary-replica, leader election)
- Each instance needs separate persistent storage
- Examples: PostgreSQL, MySQL, Kafka, Zookeeper, Elasticsearch

**Use Deployment + PVC when**:
- Single instance needing persistence (logs, cache, temp files)
- ReadOnly shared storage
- Application handles clustering without K8s help
- Examples: Single-node Redis, log aggregator, file server

**Use Cloud-Managed Database when**:
- Want automated backups, patching, HA
- Don't want to manage database operations
- Cost is acceptable (usually 2-3x more than self-hosted)
- Examples: RDS, Cloud SQL, Azure Database
- **Trade-off**: Simplicity vs control vs cost

**Think-Aloud**: "My decision process: Can I afford managed? → Yes → Use RDS. No → Do I need HA? → Yes → Use database operator (handles complexity). No → StatefulSet with Velero backups."

### 9. Active Recall Practice (1 min)

**Pause and answer these questions**:

1. "Your PVC is stuck in Pending for 5 minutes. What are the three most common causes?" [PAUSE 5 sec]

2. "You're deploying Redis - single instance for caching. Do you need a StatefulSet or Deployment?" [PAUSE 3 sec]

3. "You're deploying a 5-node Kafka cluster. StatefulSet or Deployment? Why?" [PAUSE 5 sec]

**Answers**:
1. No matching StorageClass, quota exceeded, or no available PVs. Check with `kubectl describe pvc <name>`.

2. Deployment is fine. Single instance, no replicas, doesn't need stable identity. If adding replicas later for HA, then StatefulSet.

3. StatefulSet. Kafka needs: (a) stable network identity for broker discovery, (b) ordered startup, (c) separate storage per broker. Classic StatefulSet use case.

### 10. Recap & Synthesis (1.5 min)

**Key Takeaways**:
1. **StatefulSets provide three guarantees**: Stable network identity (predictable DNS), ordered deployment/scaling, persistent storage per pod
2. **Storage architecture has three layers**: StorageClass (configuration) → PVC (request) → PV (actual storage), connected by CSI drivers
3. **Most common failures**: PVC pending (no StorageClass, quota, zone mismatch), volume not mounting (CSI driver, zone affinity)
4. **Decision framework**: StatefulSet for distributed systems needing identity/order, Deployment for single instances, managed services for simplicity

**Connection to Episode 4**: "Remember health checks from last episode? StatefulSets need careful probe configuration. Databases take time to initialize, so startup probes are critical. Use longer timeouts for liveness probes."

**Connection to Episode 2**: "Resource management matters even more with storage. Set storage requests/limits in PVCs. Monitor disk usage - running out of space can't be fixed with pod restart."

**Spaced Repetition Callback**: "Episode 1's production mindset checklist included 'Backup and DR strategy'. Today you learned Velero - that's checklist item #5 in action."

**Looking Ahead**: "In Episode 6, we're tackling networking. You'll learn how those stable DNS names from StatefulSets actually work, how services route traffic, and why pods sometimes can't reach each other. The networking knowledge builds directly on today's StatefulSet DNS concepts."

### 11. Next Episode Preview (30 sec)

"Next time: **Kubernetes Networking & Ingress**. You'll learn:
- Why pods can't reach each other and how to debug it
- The difference between ClusterIP, NodePort, and LoadBalancer services
- How to configure Ingress controllers with TLS termination
- When to use service mesh (Istio vs Linkerd)

This builds on today's lesson - those StatefulSet DNS names like `postgres-0.postgres.default.svc.cluster.local`? Next episode, you'll understand exactly how that DNS resolution works and what happens when it breaks."

---

## Supporting Materials

### Code Examples
1. **Example 1**: Complete PostgreSQL StatefulSet with StorageClass, headless service, and volumeClaimTemplate
2. **Example 2**: PVC troubleshooting commands and common error messages
3. **Example 3**: Velero backup configuration for StatefulSet

### Technical References
- **Kubernetes StatefulSets Documentation**: Core concepts and guarantees
- **CSI Driver List**: Available drivers for different cloud providers
- **Storage Class Parameters**: Provider-specific options (AWS gp3, Azure Premium SSD)
- **Velero Documentation**: Backup best practices

### Analogies Used
1. **Vending Machine**: StorageClass = machine type, PVC = request, PV = actual item
2. **Home Address**: Stable network identity persists through pod restarts
3. **Filing Cabinets**: Each pod (employee) gets their own persistent storage (cabinet)

### Diagrams Needed
1. StatefulSet pod ordering diagram (0 → 1 → 2 creation)
2. PV/PVC/StorageClass relationship flow
3. CSI driver architecture (Kubernetes ↔ CSI ↔ Cloud Provider)

---

## Quality Checklist

### Structure
- [x] Clear beginning (recall from Episode 4) / middle (core content) / end (synthesis)
- [x] Logical flow: intro → concepts → architecture → examples → failures → decisions → practice
- [x] Time allocations realistic (total: 15 minutes)
- [x] All sections specific with concrete examples, not vague

### Pedagogy
- [x] Objectives specific/measurable (determine, configure, diagnose - all action verbs)
- [x] Spaced repetition integrated (callbacks to Ep 1, 2, 4; previews to Ep 6, 7, 10)
- [x] Active recall included (3 practice questions with pauses)
- [x] Signposting clear (numbered guarantees, step-by-step walkthrough)
- [x] 3 analogies/metaphors (vending machine, home address, filing cabinets)
- [x] Pitfalls addressed (5 common mistakes with fixes)

### Content
- [x] Addresses pain points (PVC pending, volume mounting, sizing)
- [x] Production-relevant examples (PostgreSQL deployment, backup strategy)
- [x] Decision frameworks (StatefulSet vs Deployment vs managed service)
- [x] Troubleshooting included (kubectl commands for debugging)
- [x] Appropriate depth for senior engineers (CSI drivers, zone affinity, immutable templates)

### Engagement
- [x] Strong hook (Episode 4 callback + core question about state persistence)
- [x] Practice/pause moments (3 active recall questions)
- [x] Variety in techniques (analogy, think-aloud, comparison tables, real scenario)
- [x] Preview builds anticipation (DNS resolution mystery in networking episode)

---

## Notes for Script Writing

**Tone**: Conversational but authoritative. "Here's what trips people up" rather than "Users often struggle."

**Pacing**:
- Slow down for three guarantees (critical concept)
- Speed up for kubectl commands (assume familiarity)
- Pause before active recall questions (give thinking time)

**Emphasis Points**:
- "This is CRITICAL" → StatefulSet guarantees
- "Here's what trips people up" → Common confusions
- "Let me be crystal clear" → Important distinctions

**Callback Phrases**:
- "Remember Episode 4 when we learned..."
- "This connects to Episode 2's resource management..."
- "In Episode 6, you'll see how this..."

**Troubleshooting Mindset**: Model the debugging process with think-alouds, not just commands.
