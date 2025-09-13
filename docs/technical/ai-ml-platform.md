---
title: AI/ML Platform Engineering
sidebar_position: 5
---

# Platform Engineering for AI/ML Systems

The explosion of AI has created a new specialization: Platform Engineers who build and maintain infrastructure for machine learning workloads. This guide covers the unique challenges, tools, and skills needed for AI/ML platform engineering.

## Why AI Platform Engineering is Different

### Unique Challenges

1. **Resource Intensity**
   - GPU costs can be $1-4/hour per card
   - Training jobs can run for days or weeks
   - Memory requirements often exceed traditional apps
   - Data movement costs at scale

2. **Complexity**
   - Distributed training coordination
   - Mixed hardware environments (CPUs, GPUs, TPUs)
   - Data pipeline dependencies
   - Model versioning and reproducibility

3. **Dynamic Workloads**
   - Burst training jobs
   - Variable inference loads
   - Experimental vs production workloads
   - Resource sharing and prioritization

## Core Technical Skills

### GPU Infrastructure Management

**Understanding GPU Architecture:**
```bash
# Essential GPU monitoring commands
nvidia-smi                          # GPU utilization and memory
nvidia-smi dmon                     # Real-time monitoring
nvidia-smi -l 1                     # Continuous monitoring

# Detailed GPU information
nvidia-smi -q                       # Detailed query
nvidia-smi --query-gpu=gpu_name,memory.total,memory.free --format=csv

# Process management
nvidia-smi pmon                     # Process monitoring
fuser -v /dev/nvidia*              # Find GPU users
```

**GPU Resource Management in Kubernetes:**
```yaml
# GPU resource requests
apiVersion: v1
kind: Pod
metadata:
  name: gpu-pod
spec:
  containers:
  - name: cuda-container
    image: nvidia/cuda:11.0-base
    resources:
      limits:
        nvidia.com/gpu: 2  # requesting 2 GPUs
    env:
    - name: NVIDIA_VISIBLE_DEVICES
      value: "0,1"
```

**Multi-Instance GPU (MIG) Configuration:**
```bash
# Enable MIG mode
sudo nvidia-smi -mig 1

# Create GPU instances
sudo nvidia-smi mig -cgi 9,14,14,19,19 -C

# List MIG devices
nvidia-smi -L
```

**Resources:**
- 📖 [NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/overview.html)
- 🎥 [GPU Sharing in Kubernetes](https://www.youtube.com/watch?v=MlJ2ffwtKLI)
- 📚 [CUDA Programming Guide](https://docs.nvidia.com/cuda/cuda-c-programming-guide/)

### ML Pipeline Infrastructure

**Data Pipeline Architecture:**
```python
# Example: Distributed data processing with Ray
import ray
from ray import data

@ray.remote
def preprocess_batch(batch):
    # GPU preprocessing
    return transformed_batch

# Distributed data loading
dataset = ray.data.read_parquet("s3://bucket/training-data")
processed = dataset.map_batches(
    preprocess_batch,
    batch_size=1000,
    num_gpus=0.5  # Fractional GPU allocation
)
```

**Training Pipeline Orchestration:**
```yaml
# Kubeflow Pipeline example
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: training-pipeline-
spec:
  entrypoint: ml-pipeline
  templates:
  - name: ml-pipeline
    dag:
      tasks:
      - name: data-prep
        template: preprocess-data
      - name: training
        dependencies: [data-prep]
        template: distributed-training
      - name: evaluation
        dependencies: [training]
        template: model-evaluation
      - name: deployment
        dependencies: [evaluation]
        template: model-deployment
```

**Feature Store Implementation:**
```python
# Feature store abstraction
class FeatureStore:
    def __init__(self, backend="redis"):
        self.backend = self._init_backend(backend)
    
    def get_features(self, entity_ids, feature_names):
        """Retrieve features with caching and fallback"""
        features = self.backend.get_batch(entity_ids, feature_names)
        return self._validate_features(features)
    
    def update_features(self, features_df):
        """Update features with versioning"""
        version = self._get_next_version()
        self.backend.write_batch(features_df, version)
```

**Resources:**
- 📖 [MLOps Principles](https://ml-ops.org/)
- 🎥 [Building ML Platforms](https://www.youtube.com/watch?v=I8dKvzPVDj4)
- 📚 [Designing Machine Learning Systems](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/)

### Model Serving Infrastructure

**High-Performance Model Serving:**
```python
# Triton Inference Server configuration
name: "bert_model"
platform: "pytorch_libtorch"
max_batch_size: 8
input [
  {
    name: "input_ids"
    data_type: TYPE_INT64
    dims: [ -1, 512 ]
  }
]
output [
  {
    name: "predictions"
    data_type: TYPE_FP32
    dims: [ -1, 2 ]
  }
]
instance_group [
  {
    count: 2
    kind: KIND_GPU
    gpus: [ 0, 1 ]
  }
]
```

**Auto-scaling for Inference:**
```yaml
# KEDA autoscaler for GPU workloads
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: gpu-inference-scaler
spec:
  scaleTargetRef:
    name: inference-deployment
  minReplicaCount: 1
  maxReplicaCount: 10
  triggers:
  - type: prometheus
    metadata:
      serverAddress: http://prometheus:9090
      metricName: gpu_utilization_percentage
      threshold: '70'
      query: |
        avg(
          DCGM_FI_DEV_GPU_UTIL{pod=~"inference-deployment-.*"}
        )
```

**Model A/B Testing:**
```python
# Traffic splitting for model comparison
class ModelRouter:
    def __init__(self, models_config):
        self.models = models_config
        self.metrics = MetricsCollector()
    
    def route_request(self, request):
        # Determine model based on routing rules
        if request.user_id in self.canary_users:
            model = self.models['canary']
            self.metrics.increment('canary_requests')
        else:
            # Weighted routing
            model = self._weighted_choice(self.models['stable'])
        
        return model.predict(request)
```

**Resources:**
- 📖 [NVIDIA Triton Inference Server](https://developer.nvidia.com/nvidia-triton-inference-server)
- 🎥 [Model Serving at Scale](https://www.youtube.com/watch?v=YnCmM8dWeCs)
- 📖 [Seldon Core Documentation](https://docs.seldon.io/)

## AI-Specific Platform Challenges

### Large-Scale Training Infrastructure

**Distributed Training Setup:**
```python
# Horovod distributed training configuration
import horovod.torch as hvd

hvd.init()

# Pin GPU to local rank
torch.cuda.set_device(hvd.local_rank())

# Scale learning rate by number of GPUs
optimizer = optim.SGD(model.parameters(),
                      lr=args.lr * hvd.size())

# Wrap optimizer with Horovod
optimizer = hvd.DistributedOptimizer(optimizer,
                                     named_parameters=model.named_parameters())

# Broadcast parameters from rank 0
hvd.broadcast_parameters(model.state_dict(), root_rank=0)
```

**Checkpointing and Recovery:**
```python
class TrainingCheckpointer:
    def __init__(self, storage_backend="s3"):
        self.storage = self._init_storage(storage_backend)
        
    def save_checkpoint(self, model, optimizer, epoch, metrics):
        checkpoint = {
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'metrics': metrics,
            'timestamp': datetime.now()
        }
        
        # Save to distributed storage
        path = f"checkpoints/epoch_{epoch}.pt"
        self.storage.save(checkpoint, path)
        
        # Maintain only last N checkpoints
        self._cleanup_old_checkpoints(keep_last=3)
```

**Resources:**
- 📖 [Distributed Training Best Practices](https://pytorch.org/tutorials/intermediate/ddp_tutorial.html)
- 🎥 [Large Scale Training Infrastructure](https://www.youtube.com/watch?v=6Ut_KxOHBDo)
- 📚 [High Performance Python](https://www.oreilly.com/library/view/high-performance-python/9781492055013/)

### Data Infrastructure for ML

**Data Lake Architecture:**
```python
# Delta Lake for ML data versioning
from delta import DeltaTable

# Create versioned feature table
feature_table = (
    spark.range(0, 1000000)
    .withColumn("features", generate_features_udf())
    .write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .save("/ml/features/user_embeddings")
)

# Time travel for reproducibility
df_v1 = spark.read.format("delta").option("versionAsOf", 1).load(path)
```

**Data Validation Pipeline:**
```python
# Great Expectations for data quality
import great_expectations as ge

def validate_training_data(df):
    # Create expectations suite
    expectation_suite = ge.dataset.PandasDataset(df)
    
    # Define expectations
    expectation_suite.expect_column_values_to_not_be_null("label")
    expectation_suite.expect_column_values_to_be_between(
        "feature_1", min_value=0, max_value=1
    )
    
    # Validate
    validation_result = expectation_suite.validate()
    
    if not validation_result.success:
        raise DataQualityError(validation_result)
```

**Resources:**
- 📖 [Data Engineering for ML](https://www.oreilly.com/library/view/data-engineering-for/9781098103545/)
- 🎥 [Building Feature Stores](https://www.youtube.com/watch?v=KV7z5zCvjvE)
- 📖 [Feast Feature Store](https://docs.feast.dev/)

### Cost Optimization for AI Workloads

**GPU Utilization Monitoring:**
```python
# Custom GPU metrics collector
class GPUMetricsCollector:
    def __init__(self):
        self.prometheus_client = PrometheusClient()
        
    def collect_metrics(self):
        metrics = {
            'gpu_utilization': [],
            'memory_usage': [],
            'power_draw': [],
            'temperature': []
        }
        
        # Collect from all GPUs
        for gpu_id in range(torch.cuda.device_count()):
            handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_id)
            
            util = pynvml.nvmlDeviceGetUtilizationRates(handle)
            metrics['gpu_utilization'].append(util.gpu)
            metrics['memory_usage'].append(util.memory)
            
        self.prometheus_client.push_metrics(metrics)
```

**Spot Instance Management:**
```yaml
# Spot instance configuration for training
apiVersion: v1
kind: ConfigMap
metadata:
  name: spot-training-config
data:
  spot-handler.sh: |
    #!/bin/bash
    # Check for spot instance termination notice
    while true; do
      if curl -s http://169.254.169.254/latest/meta-data/spot/termination-time | grep -q .*T.*Z; then
        echo "Spot instance termination notice detected"
        # Save checkpoint
        kubectl exec $POD_NAME -- python save_checkpoint.py
        # Gracefully shutdown
        kubectl delete pod $POD_NAME
      fi
      sleep 5
    done
```

**Resources:**
- 📖 [Cloud Cost Optimization for ML](https://aws.amazon.com/blogs/machine-learning/cost-optimization-best-practices-for-amazon-sagemaker/)
- 🎥 [Reducing ML Infrastructure Costs](https://www.youtube.com/watch?v=9-KgUqBATsU)
- 📖 [Kubernetes Cost Optimization](https://www.kubecost.com/kubernetes-cost-optimization/)

## Tools and Platforms

### ML Orchestration Platforms

**Kubeflow**
- Kubernetes-native ML platform
- Pipeline orchestration
- Multi-framework support
- Distributed training operators

```yaml
# Kubeflow PyTorch Operator example
apiVersion: kubeflow.org/v1
kind: PyTorchJob
metadata:
  name: distributed-training
spec:
  pytorchReplicaSpecs:
    Master:
      replicas: 1
      template:
        spec:
          containers:
          - name: pytorch
            image: training:latest
            resources:
              limits:
                nvidia.com/gpu: 1
    Worker:
      replicas: 3
      template:
        spec:
          containers:
          - name: pytorch
            image: training:latest
            resources:
              limits:
                nvidia.com/gpu: 2
```

**MLflow**
- Experiment tracking
- Model registry
- Model serving
- Multi-framework support

```python
# MLflow integration
import mlflow
import mlflow.pytorch

with mlflow.start_run():
    # Log parameters
    mlflow.log_param("learning_rate", lr)
    mlflow.log_param("batch_size", batch_size)
    
    # Train model
    for epoch in range(epochs):
        train_loss = train_epoch(model, train_loader)
        mlflow.log_metric("train_loss", train_loss, step=epoch)
    
    # Log model
    mlflow.pytorch.log_model(model, "model")
```

**Ray**
- Distributed computing framework
- Hyperparameter tuning (Ray Tune)
- Distributed training (Ray Train)
- Model serving (Ray Serve)

```python
# Ray distributed training
import ray
from ray import train
from ray.train import ScalingConfig

def train_func(config):
    model = create_model(config)
    # Training logic
    return model

trainer = train.TorchTrainer(
    train_func,
    scaling_config=ScalingConfig(
        num_workers=4,
        use_gpu=True,
        resources_per_worker={"GPU": 1}
    )
)
results = trainer.fit()
```

### Monitoring and Observability

**Model Performance Monitoring:**
```python
# Model drift detection
class ModelMonitor:
    def __init__(self, baseline_metrics):
        self.baseline = baseline_metrics
        self.alerting = AlertingSystem()
        
    def check_drift(self, current_predictions, ground_truth):
        # Statistical drift detection
        psi = self.calculate_psi(
            self.baseline.distribution,
            current_predictions
        )
        
        if psi > self.drift_threshold:
            self.alerting.send_alert(
                "Model drift detected",
                {"psi": psi, "threshold": self.drift_threshold}
            )
        
        # Performance drift
        current_accuracy = accuracy_score(ground_truth, current_predictions)
        if current_accuracy < self.baseline.accuracy * 0.95:
            self.alerting.send_alert(
                "Model performance degradation",
                {"current": current_accuracy, "baseline": self.baseline.accuracy}
            )
```

**Infrastructure Monitoring Stack:**
```yaml
# Prometheus configuration for ML metrics
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'gpu-metrics'
    static_configs:
      - targets: ['dcgm-exporter:9400']
    
  - job_name: 'training-metrics'
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names:
          - ml-training
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
```

**Resources:**
- 📖 [ML Monitoring Best Practices](https://www.oreilly.com/library/view/introducing-mlops/9781492083283/)
- 🎥 [Production ML Monitoring](https://www.youtube.com/watch?v=QaKpJO-KrmE)
- 📖 [Evidently AI Monitoring](https://docs.evidentlyai.com/)

## Career Path to AI Platform Engineering

### Coming from ML Engineering

**Skills to Develop:**
1. **Infrastructure Skills**
   - Kubernetes operations
   - Cloud platform expertise
   - Networking and storage

2. **SRE Practices**
   - Monitoring and alerting
   - Incident response
   - Capacity planning

3. **Platform Mindset**
   - Building for multiple teams
   - API design
   - Documentation

**Learning Path:**
```
ML Engineering Background
    ↓
Learn Kubernetes basics (2-4 weeks)
    ↓
Cloud platform certification (4-6 weeks)
    ↓
SRE fundamentals (2-4 weeks)
    ↓
ML platform tools (Kubeflow, MLflow) (4-6 weeks)
    ↓
Production ML systems (ongoing)
```

### Coming from Traditional Platform Engineering

**Skills to Develop:**
1. **ML Fundamentals**
   - Training vs inference
   - Model architectures
   - Data processing needs

2. **GPU Infrastructure**
   - CUDA environments
   - GPU scheduling
   - Distributed training

3. **ML-Specific Tools**
   - Experiment tracking
   - Model serving
   - Feature stores

**Learning Path:**
```
Platform Engineering Background
    ↓
ML fundamentals course (4-6 weeks)
    ↓
GPU/CUDA basics (2-3 weeks)
    ↓
ML tools and frameworks (4-6 weeks)
    ↓
ML platform projects (ongoing)
```

### Interview Preparation

**Common AI Platform Engineering Questions:**

1. **System Design**
   - "Design a distributed training platform"
   - "Build a real-time model serving system"
   - "Design a feature store"
   - "Create an ML experimentation platform"

2. **Technical Deep Dives**
   - GPU scheduling algorithms
   - Data pipeline optimization
   - Model versioning strategies
   - A/B testing for ML

3. **Troubleshooting Scenarios**
   - "Training job OOM errors"
   - "Model serving latency spikes"
   - "GPU underutilization"
   - "Data pipeline failures"

**Hands-On Projects:**
1. Build a Kubernetes operator for distributed training
2. Create a model serving pipeline with monitoring
3. Implement a feature store with versioning
4. Design a cost optimization system for GPU workloads

## Market Landscape

### Demand and Compensation

**2024 Market Stats:**
- **Demand**: 300% growth in ML platform engineering roles since 2022
- **Compensation**: 20-30% premium over traditional platform engineering
- **Top Companies**: OpenAI, Anthropic, Google DeepMind, Meta AI, Tesla

**Salary Ranges (US Market):**
| Level | Years | Base Salary | Total Comp |
|-------|-------|------------|------------|
| Junior | 0-2 | $130k-$160k | $160k-$220k |
| Mid | 2-5 | $160k-$200k | $220k-$350k |
| Senior | 5-8 | $200k-$250k | $350k-$500k |
| Staff | 8+ | $250k-$320k | $450k-$700k+ |

### Key Companies and Teams

**AI-First Companies:**
- OpenAI - ChatGPT infrastructure
- Anthropic - Claude infrastructure
- Stability AI - Stable Diffusion platform
- Hugging Face - Model hub infrastructure

**Big Tech AI Teams:**
- Google - Vertex AI, TPU infrastructure
- Meta - PyTorch, Research clusters
- Microsoft - Azure ML, OpenAI partnership
- Amazon - SageMaker, Bedrock

**AI Infrastructure Startups:**
- Weights & Biases - Experiment tracking
- Determined AI - Training platform
- Anyscale - Ray platform
- Modal - Serverless GPU compute

## Essential Resources

### Books
- 📚 [Designing Machine Learning Systems](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/) - Chip Huyen
- 📚 [Machine Learning Engineering](https://www.mlebook.com/wiki/doku.php) - Andriy Burkov
- 📚 [Building Machine Learning Powered Applications](https://www.oreilly.com/library/view/building-machine-learning/9781492045106/) - Emmanuel Ameisen

### Courses
- 🎓 [Full Stack Deep Learning](https://fullstackdeeplearning.com/) - Comprehensive MLOps
- 🎓 [Fast.ai Practical Deep Learning](https://course.fast.ai/) - Hands-on approach
- 🎓 [MLOps Specialization](https://www.coursera.org/specializations/machine-learning-engineering-for-production-mlops) - Andrew Ng

### Communities
- 💬 [MLOps Community](https://mlops.community/) - 20k+ members
- 💬 [Kubernetes ML Slack](https://kubeflow.slack.com/) - Kubeflow community
- 💬 [r/MachineLearning](https://reddit.com/r/MachineLearning) - Research and engineering

### Blogs and Newsletters
- 📖 [Google AI Blog](https://ai.googleblog.com/) - Latest from Google
- 📖 [OpenAI Blog](https://openai.com/blog) - GPT infrastructure insights
- 📖 [Neptune AI Blog](https://neptune.ai/blog) - MLOps best practices
- 📧 [The Batch](https://www.deeplearning.ai/the-batch/) - Weekly AI news

### Open Source Projects
- ⭐ [Kubeflow](https://github.com/kubeflow/kubeflow) - ML on Kubernetes
- ⭐ [MLflow](https://github.com/mlflow/mlflow) - ML lifecycle platform
- ⭐ [Ray](https://github.com/ray-project/ray) - Distributed AI
- ⭐ [Seldon Core](https://github.com/SeldonIO/seldon-core) - Model serving

### Certifications
- 🎓 [AWS ML Specialty](https://aws.amazon.com/certification/certified-machine-learning-specialty/)
- 🎓 [Google Cloud ML Engineer](https://cloud.google.com/certification/machine-learning-engineer)
- 🎓 [Azure AI Engineer](https://docs.microsoft.com/en-us/certifications/azure-ai-engineer/)

## Key Takeaways

1. **AI platform engineering is a high-growth specialization** with excellent career prospects
2. **Unique challenges** require both ML understanding and platform expertise
3. **GPU infrastructure** is a critical skill differentiator
4. **Cost optimization** is crucial given expensive compute resources
5. **Full-stack knowledge** from data pipelines to model serving is valuable
6. **The field is rapidly evolving** - continuous learning is essential

Remember: The intersection of AI and platform engineering offers exciting opportunities to work on cutting-edge infrastructure that powers the AI revolution. Focus on building robust, scalable platforms that enable data scientists and ML engineers to innovate faster.