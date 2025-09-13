---
title: Vector Databases for AI
sidebar_position: 13
---

# Vector Databases for AI/ML Infrastructure

Master the specialized databases powering AI applications, from semantic search to recommendation systems. Learn how to build, scale, and optimize vector databases for production AI workloads.

## 📚 Essential Resources

### 📖 Must-Read Papers & Articles
- **[Faiss: A Library for Efficient Similarity Search](https://arxiv.org/abs/1702.08734)** - Facebook Research
- **[Billion-scale similarity search with GPUs](https://arxiv.org/abs/1702.08734)** - Johnson et al.
- **[HNSW: Hierarchical Navigable Small World](https://arxiv.org/abs/1603.09320)** - Malkov & Yashunin
- **[Product Quantization](https://hal.inria.fr/inria-00514462v2/document)** - Jegou et al.
- **[Vector Database Benchmarks](https://github.com/erikbern/ann-benchmarks)** - ANN comparison

### 🎥 Video Resources
- **[Vector Databases Explained](https://www.youtube.com/watch?v=klTvEwg3oJ4)** - Fireship
- **[Building RAG Applications](https://www.youtube.com/watch?v=sVcwVQRHIc8)** - DeepLearning.AI
- **[Pinecone Vector Database Course](https://www.youtube.com/playlist?list=PLRLVhGQeJDTLiw-ZJpgUtZW-bseS2gq9-)** - James Briggs
- **[Embeddings Workshop](https://www.youtube.com/watch?v=ySus5ZS0b94)** - Hugging Face
- **[Vector Search at Scale](https://www.youtube.com/watch?v=t5mQmKjXLKo)** - Weaviate

### 🎓 Courses & Training
- **[Vector Databases & Embeddings](https://www.deeplearning.ai/short-courses/vector-databases-embeddings-applications/)** - DeepLearning.AI
- **[LangChain for LLM Apps](https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/)** - Harrison Chase
- **[Building AI Applications](https://www.coursera.org/learn/building-ai-powered-applications)** - Coursera
- **[Semantic Search Course](https://www.pinecone.io/learn/)** - Pinecone Learning Center
- **[Vector Database Fundamentals](https://learn.milvus.io/)** - Milvus tutorials

### 📰 Blogs & Articles
- **[Pinecone Blog](https://www.pinecone.io/blog/)** - Vector DB insights
- **[Weaviate Blog](https://weaviate.io/blog)** - Vector search articles
- **[Qdrant Blog](https://qdrant.tech/blog/)** - Technical deep dives
- **[Milvus Blog](https://milvus.io/blog)** - Scalability focus
- **[Chroma Blog](https://www.trychroma.com/blog)** - Embedding database

### 🔧 Essential Tools & Platforms
- **[Pinecone](https://www.pinecone.io/)** - Managed vector database
- **[Weaviate](https://weaviate.io/)** - Open source vector DB
- **[Qdrant](https://qdrant.tech/)** - High-performance vector search
- **[Milvus](https://milvus.io/)** - Scalable vector database
- **[Chroma](https://www.trychroma.com/)** - Embedding database

### 💬 Communities & Forums
- **[Vector Database Community](https://discord.gg/vectordb)** - Discord
- **[r/VectorDatabases](https://reddit.com/r/VectorDatabases)** - Reddit
- **[Pinecone Community](https://community.pinecone.io/)** - Forum
- **[Weaviate Slack](https://weaviate.io/slack)** - Slack community
- **[AI Stack Exchange](https://ai.stackexchange.com/)** - Q&A

### 🏆 RAG & LLM Resources
- **[LangChain Docs](https://python.langchain.com/)** - LLM framework
- **[LlamaIndex Guide](https://gpt-index.readthedocs.io/)** - Data framework
- **[OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)** - API guide
- **[Semantic Kernel](https://github.com/microsoft/semantic-kernel)** - Microsoft's SDK
- **[Haystack](https://haystack.deepset.ai/)** - NLP framework



## Understanding Vector Databases

### Why Vector Databases Matter

**Traditional Database vs Vector Database:**
```
Traditional DB: WHERE name = 'John' AND age > 25
Vector DB: Find nearest neighbors to [0.2, -0.5, 0.8, ...]

Use Cases:
- Semantic search ("find similar documents")
- Recommendation systems
- Image/video similarity search
- RAG (Retrieval Augmented Generation) for LLMs
- Anomaly detection
- Clustering and classification
```

### Vector Embeddings Fundamentals

```python
# Understanding embeddings
import numpy as np
from sentence_transformers import SentenceTransformer
import torch

class EmbeddingPipeline:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        
    def encode_text(self, texts):
        """Convert text to vector embeddings"""
        # Batch encoding for efficiency
        embeddings = self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True  # L2 normalization
        )
        return embeddings
    
    def encode_multimodal(self, data):
        """Encode different data types"""
        if data['type'] == 'text':
            return self.encode_text([data['content']])[0]
        elif data['type'] == 'image':
            # Use CLIP or similar model
            return self.encode_image(data['content'])
        elif data['type'] == 'audio':
            # Use audio embedding model
            return self.encode_audio(data['content'])
    
    def compute_similarity(self, vec1, vec2):
        """Compute cosine similarity"""
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
```

## Production Vector Database Implementations

### Pinecone

```python
# Pinecone production implementation
import pinecone
from typing import List, Dict, Optional
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

class PineconeVectorStore:
    def __init__(self, api_key: str, environment: str):
        pinecone.init(api_key=api_key, environment=environment)
        self.index_name = None
        self.index = None
        
    def create_index(self, name: str, dimension: int, metric: str = 'cosine'):
        """Create a new Pinecone index with optimal settings"""
        if name not in pinecone.list_indexes():
            pinecone.create_index(
                name=name,
                dimension=dimension,
                metric=metric,
                pod_type='p2.x1',  # Performance-optimized
                replicas=2,  # High availability
                shards=1,
                metadata_config={
                    'indexed': ['category', 'timestamp', 'user_id']
                }
            )
        
        self.index_name = name
        self.index = pinecone.Index(name)
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def upsert_batch(self, vectors: List[Dict]):
        """Batch upsert with retry logic"""
        batch_size = 100  # Pinecone recommended batch size
        
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            
            # Format for Pinecone
            upsert_data = [
                (
                    vec['id'],
                    vec['embedding'],
                    vec.get('metadata', {})
                )
                for vec in batch
            ]
            
            self.index.upsert(vectors=upsert_data)
            
    async def hybrid_search(self, 
                          query_vector: List[float],
                          filter_dict: Optional[Dict] = None,
                          top_k: int = 10,
                          include_metadata: bool = True):
        """Hybrid search with metadata filtering"""
        results = self.index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=include_metadata,
            filter=filter_dict,  # e.g., {"category": "documentation"}
        )
        
        return self._process_results(results)
    
    def _process_results(self, results):
        """Process and enrich search results"""
        processed = []
        for match in results['matches']:
            processed.append({
                'id': match['id'],
                'score': match['score'],
                'metadata': match.get('metadata', {}),
                'distance': 1 - match['score']  # For cosine similarity
            })
        return processed
```

### Weaviate

```python
# Weaviate with GraphQL and modules
import weaviate
from weaviate.embedded import EmbeddedOptions
import json

class WeaviateVectorStore:
    def __init__(self, url: str = None):
        if url:
            self.client = weaviate.Client(url)
        else:
            # Embedded Weaviate for development
            self.client = weaviate.Client(
                embedded_options=EmbeddedOptions()
            )
    
    def create_schema(self):
        """Create schema with vectorizer and modules"""
        schema = {
            "classes": [{
                "class": "Document",
                "description": "A document with semantic search",
                "vectorizer": "text2vec-transformers",
                "moduleConfig": {
                    "text2vec-transformers": {
                        "model": "sentence-transformers/all-MiniLM-L6-v2",
                        "options": {
                            "waitForModel": True,
                            "useCache": True,
                            "useGPU": True
                        }
                    },
                    "qna-transformers": {
                        "model": "deepset/bert-base-cased-squad2"
                    }
                },
                "properties": [
                    {
                        "name": "content",
                        "dataType": ["text"],
                        "description": "Document content",
                        "moduleConfig": {
                            "text2vec-transformers": {
                                "skip": False,
                                "vectorizePropertyName": False
                            }
                        }
                    },
                    {
                        "name": "title",
                        "dataType": ["string"],
                        "description": "Document title"
                    },
                    {
                        "name": "category",
                        "dataType": ["string"],
                        "description": "Document category",
                        "moduleConfig": {
                            "text2vec-transformers": {
                                "skip": True
                            }
                        }
                    },
                    {
                        "name": "timestamp",
                        "dataType": ["date"],
                        "description": "Creation timestamp"
                    }
                ],
                "invertedIndexConfig": {
                    "bm25": {
                        "b": 0.75,
                        "k1": 1.2
                    },
                    "cleanupIntervalSeconds": 60,
                    "stopwords": {
                        "preset": "en"
                    }
                }
            }]
        }
        
        self.client.schema.create(schema)
    
    def semantic_search_with_qa(self, query: str, limit: int = 5):
        """Semantic search with Q&A capability"""
        # Semantic search
        search_results = (
            self.client.query
            .get("Document", ["content", "title", "_additional {distance}"])
            .with_near_text({"concepts": [query]})
            .with_limit(limit)
            .do()
        )
        
        # Q&A on results
        qa_results = (
            self.client.query
            .get("Document", ["content", "title"])
            .with_ask({
                "question": query,
                "properties": ["content"]
            })
            .with_limit(1)
            .do()
        )
        
        return {
            'semantic_results': search_results,
            'answer': qa_results
        }
```

### Qdrant

```python
# Qdrant with advanced features
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct,
    Filter, FieldCondition, MatchValue,
    SearchRequest, SearchParams
)

class QdrantVectorStore:
    def __init__(self, host="localhost", port=6333):
        self.client = QdrantClient(host=host, port=port)
        
    def create_collection(self, name: str, vector_size: int):
        """Create collection with custom configuration"""
        self.client.recreate_collection(
            collection_name=name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
                on_disk=True  # For large collections
            ),
            optimizers_config={
                "indexing_threshold": 20000,
                "memmap_threshold": 50000,
                "default_segment_number": 5
            },
            hnsw_config={
                "m": 16,
                "ef_construct": 100,
                "full_scan_threshold": 10000
            }
        )
    
    async def insert_with_payloads(self, collection: str, documents: List[Dict]):
        """Insert vectors with rich metadata"""
        points = []
        
        for idx, doc in enumerate(documents):
            point = PointStruct(
                id=doc.get('id', idx),
                vector=doc['embedding'],
                payload={
                    "text": doc['text'],
                    "metadata": doc.get('metadata', {}),
                    "timestamp": doc.get('timestamp', datetime.utcnow()),
                    "tags": doc.get('tags', [])
                }
            )
            points.append(point)
        
        # Batch upload with progress
        batch_size = 1000
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            self.client.upsert(
                collection_name=collection,
                points=batch,
                wait=True
            )
    
    def filtered_search(self, 
                       collection: str,
                       query_vector: List[float],
                       filters: Dict,
                       limit: int = 10):
        """Advanced filtered search"""
        # Build filter conditions
        must_conditions = []
        
        if 'category' in filters:
            must_conditions.append(
                FieldCondition(
                    key="metadata.category",
                    match=MatchValue(value=filters['category'])
                )
            )
        
        if 'date_range' in filters:
            must_conditions.append(
                FieldCondition(
                    key="timestamp",
                    range={
                        "gte": filters['date_range']['start'],
                        "lte": filters['date_range']['end']
                    }
                )
            )
        
        search_result = self.client.search(
            collection_name=collection,
            query_vector=query_vector,
            limit=limit,
            query_filter=Filter(must=must_conditions) if must_conditions else None,
            search_params=SearchParams(
                hnsw_ef=128,
                exact=False
            )
        )
        
        return search_result
```

### Milvus

```python
# Milvus for large-scale deployments
from pymilvus import (
    connections, Collection, CollectionSchema,
    FieldSchema, DataType, utility
)

class MilvusVectorStore:
    def __init__(self, host='localhost', port='19530'):
        connections.connect(host=host, port=port)
        
    def create_collection(self, name: str, dim: int):
        """Create collection with optimized settings"""
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="metadata", dtype=DataType.JSON)
        ]
        
        schema = CollectionSchema(
            fields=fields,
            description="Document embeddings with metadata"
        )
        
        collection = Collection(
            name=name,
            schema=schema,
            using='default',
            shards_num=2  # Distributed storage
        )
        
        # Create indexes for performance
        index_params = {
            "metric_type": "IP",  # Inner product
            "index_type": "IVF_FLAT",
            "params": {"nlist": 2048}
        }
        
        collection.create_index(
            field_name="embedding",
            index_params=index_params
        )
        
        # Load collection to memory
        collection.load()
        
        return collection
    
    def hybrid_search(self, collection_name: str, query: Dict):
        """Hybrid vector + keyword search"""
        collection = Collection(collection_name)
        
        # Vector search
        vector_results = collection.search(
            data=[query['vector']],
            anns_field="embedding",
            param={"metric_type": "IP", "params": {"nprobe": 64}},
            limit=query.get('limit', 10),
            expr=query.get('filter'),  # e.g., "metadata['category'] == 'tech'"
            output_fields=["text", "metadata"]
        )
        
        # Combine with keyword search if needed
        if 'keywords' in query:
            keyword_expr = " || ".join([
                f"text like '%{keyword}%'"
                for keyword in query['keywords']
            ])
            
            keyword_results = collection.query(
                expr=keyword_expr,
                limit=query.get('limit', 10),
                output_fields=["id", "text", "metadata"]
            )
            
            # Merge and rank results
            return self._merge_results(vector_results, keyword_results)
        
        return vector_results
```

## Vector Database Optimization

### Indexing Strategies

```python
# Advanced indexing for performance
class VectorIndexOptimizer:
    def __init__(self):
        self.index_types = {
            'flat': self.create_flat_index,
            'hnsw': self.create_hnsw_index,
            'ivf': self.create_ivf_index,
            'scann': self.create_scann_index
        }
    
    def select_index_type(self, num_vectors: int, dimensions: int, 
                         accuracy_requirement: float = 0.95):
        """Select optimal index type based on dataset"""
        if num_vectors < 10000:
            return 'flat'  # Exact search for small datasets
        elif num_vectors < 1000000 and accuracy_requirement > 0.9:
            return 'hnsw'  # High accuracy, moderate scale
        elif num_vectors < 10000000:
            return 'ivf'  # Good balance
        else:
            return 'scann'  # Large scale
    
    def create_hnsw_index(self, vectors, config=None):
        """Hierarchical Navigable Small World index"""
        import hnswlib
        
        config = config or {
            'M': 48,  # Number of connections
            'ef_construction': 200,  # Build time accuracy
            'ef': 100,  # Query time accuracy
            'seed': 42
        }
        
        dim = vectors.shape[1]
        num_elements = vectors.shape[0]
        
        # Initialize index
        index = hnswlib.Index(space='l2', dim=dim)
        index.init_index(
            max_elements=num_elements,
            ef_construction=config['ef_construction'],
            M=config['M'],
            random_seed=config['seed']
        )
        
        # Add vectors with progress tracking
        index.add_items(vectors, np.arange(num_elements))
        
        # Set query time parameters
        index.set_ef(config['ef'])
        
        return index
    
    def optimize_for_production(self, index, expected_qps: int):
        """Optimize index for production workload"""
        optimizations = {
            'cache_size': self._calculate_cache_size(expected_qps),
            'num_threads': self._calculate_thread_count(expected_qps),
            'batch_size': self._calculate_batch_size(expected_qps),
            'prefetch': expected_qps > 1000
        }
        
        return optimizations
```

### Sharding and Distribution

```python
# Distributed vector database implementation
class DistributedVectorStore:
    def __init__(self, nodes: List[str], replication_factor: int = 2):
        self.nodes = nodes
        self.replication_factor = replication_factor
        self.consistent_hash = ConsistentHash(nodes)
        self.shards = self._initialize_shards()
    
    def _initialize_shards(self):
        """Initialize sharded vector stores"""
        shards = {}
        for node in self.nodes:
            shards[node] = self._create_node_client(node)
        return shards
    
    async def distributed_insert(self, vector_id: str, vector: np.ndarray, 
                               metadata: Dict):
        """Insert with replication across shards"""
        # Determine primary and replica nodes
        primary_node = self.consistent_hash.get_node(vector_id)
        replica_nodes = self.consistent_hash.get_replicas(
            vector_id, 
            self.replication_factor - 1
        )
        
        # Async insert to all nodes
        tasks = []
        for node in [primary_node] + replica_nodes:
            task = self.shards[node].insert(vector_id, vector, metadata)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Verify successful replication
        successful = sum(1 for r in results if not isinstance(r, Exception))
        if successful < self.replication_factor // 2 + 1:
            raise ReplicationError(f"Only {successful} replicas succeeded")
        
        return results
    
    async def distributed_search(self, query_vector: np.ndarray, 
                               top_k: int = 10):
        """Distributed search across all shards"""
        # Fan out search to all nodes
        tasks = []
        for node, client in self.shards.items():
            task = client.search(query_vector, top_k * 2)  # Over-fetch
            tasks.append((node, task))
        
        # Gather results
        all_results = []
        for node, task in tasks:
            try:
                results = await task
                all_results.extend([
                    {**r, 'node': node} for r in results
                ])
            except Exception as e:
                print(f"Search failed on node {node}: {e}")
        
        # Merge and rank results
        all_results.sort(key=lambda x: x['score'], reverse=True)
        return all_results[:top_k]
```

## RAG (Retrieval Augmented Generation) Implementation

### Production RAG Pipeline

```python
# RAG system for LLM applications
class RAGPipeline:
    def __init__(self, vector_store, llm_client, embedding_model):
        self.vector_store = vector_store
        self.llm = llm_client
        self.embedder = embedding_model
        self.reranker = CrossEncoderReranker()
        
    async def process_query(self, query: str, context_config: Dict = None):
        """End-to-end RAG pipeline"""
        config = context_config or {
            'num_candidates': 20,
            'num_contexts': 5,
            'max_tokens': 2000,
            'temperature': 0.7
        }
        
        # 1. Query understanding and expansion
        expanded_queries = await self.expand_query(query)
        
        # 2. Retrieve candidates
        candidates = await self.retrieve_candidates(
            expanded_queries, 
            config['num_candidates']
        )
        
        # 3. Rerank candidates
        reranked = await self.reranker.rerank(
            query, 
            candidates, 
            top_k=config['num_contexts']
        )
        
        # 4. Build context
        context = self.build_context(reranked, config['max_tokens'])
        
        # 5. Generate response
        response = await self.generate_response(
            query, 
            context, 
            config['temperature']
        )
        
        # 6. Add citations
        response_with_citations = self.add_citations(response, reranked)
        
        return {
            'answer': response_with_citations,
            'sources': reranked,
            'confidence': self.calculate_confidence(reranked)
        }
    
    async def expand_query(self, query: str):
        """Query expansion for better retrieval"""
        # Use LLM to generate alternative phrasings
        prompt = f"""Generate 3 alternative ways to ask this question:
        Original: {query}
        
        Alternatives:
        1."""
        
        expansions = await self.llm.generate(prompt, max_tokens=100)
        
        # Also use semantic expansion
        query_embedding = self.embedder.encode(query)
        
        return {
            'original': query,
            'llm_expansions': self.parse_expansions(expansions),
            'embedding': query_embedding
        }
    
    def build_context(self, documents: List[Dict], max_tokens: int):
        """Build optimized context for LLM"""
        context_parts = []
        total_tokens = 0
        
        for doc in documents:
            # Estimate tokens (rough approximation)
            doc_tokens = len(doc['text'].split()) * 1.3
            
            if total_tokens + doc_tokens > max_tokens:
                # Truncate if necessary
                remaining_tokens = max_tokens - total_tokens
                truncated_text = self.truncate_to_tokens(
                    doc['text'], 
                    int(remaining_tokens / 1.3)
                )
                context_parts.append(truncated_text)
                break
            
            context_parts.append(doc['text'])
            total_tokens += doc_tokens
        
        return "\n\n---\n\n".join(context_parts)
```

### Hybrid Search Implementation

```python
# Combining vector and keyword search
class HybridSearchEngine:
    def __init__(self, vector_store, text_search_engine):
        self.vector_store = vector_store
        self.text_search = text_search_engine
        self.fusion_weights = {'vector': 0.7, 'keyword': 0.3}
    
    async def hybrid_search(self, query: str, filters: Dict = None):
        """Combine vector and keyword search results"""
        # Parallel search
        vector_task = self.vector_search(query, filters)
        keyword_task = self.keyword_search(query, filters)
        
        vector_results, keyword_results = await asyncio.gather(
            vector_task, keyword_task
        )
        
        # Reciprocal Rank Fusion
        fused_results = self.reciprocal_rank_fusion(
            [vector_results, keyword_results],
            weights=[self.fusion_weights['vector'], 
                    self.fusion_weights['keyword']]
        )
        
        return fused_results
    
    def reciprocal_rank_fusion(self, result_lists: List[List], 
                              weights: List[float], k: int = 60):
        """RRF algorithm for result fusion"""
        scores = {}
        
        for results, weight in zip(result_lists, weights):
            for rank, result in enumerate(results):
                doc_id = result['id']
                if doc_id not in scores:
                    scores[doc_id] = 0
                
                # RRF score
                scores[doc_id] += weight * (1 / (k + rank + 1))
        
        # Sort by fused score
        sorted_docs = sorted(
            scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        # Retrieve full documents
        return self.retrieve_documents([doc_id for doc_id, _ in sorted_docs])
```

## Performance and Scalability

### Benchmarking Vector Databases

```python
# Comprehensive benchmarking suite
class VectorDBBenchmark:
    def __init__(self):
        self.metrics = {
            'insert_throughput': [],
            'query_latency': [],
            'query_throughput': [],
            'recall': [],
            'memory_usage': []
        }
    
    async def benchmark_database(self, db_client, dataset, queries):
        """Run comprehensive benchmark"""
        print(f"Benchmarking {db_client.__class__.__name__}")
        
        # 1. Insertion benchmark
        insert_metrics = await self.benchmark_insertion(db_client, dataset)
        
        # 2. Query benchmark
        query_metrics = await self.benchmark_queries(db_client, queries)
        
        # 3. Recall benchmark
        recall_metrics = await self.benchmark_recall(db_client, queries)
        
        # 4. Resource usage
        resource_metrics = self.measure_resources(db_client)
        
        return {
            'insertion': insert_metrics,
            'query': query_metrics,
            'recall': recall_metrics,
            'resources': resource_metrics
        }
    
    async def benchmark_insertion(self, db_client, dataset):
        """Measure insertion performance"""
        batch_sizes = [100, 1000, 10000]
        results = {}
        
        for batch_size in batch_sizes:
            start_time = time.time()
            
            for i in range(0, len(dataset), batch_size):
                batch = dataset[i:i + batch_size]
                await db_client.insert_batch(batch)
            
            elapsed = time.time() - start_time
            throughput = len(dataset) / elapsed
            
            results[f'batch_{batch_size}'] = {
                'throughput': throughput,
                'latency_per_item': elapsed / len(dataset)
            }
        
        return results
```

### Caching Strategies

```python
# Multi-level caching for vector search
class VectorSearchCache:
    def __init__(self, vector_store, cache_size_mb=1024):
        self.vector_store = vector_store
        self.cache_size = cache_size_mb * 1024 * 1024
        self.query_cache = LRUCache(maxsize=10000)
        self.vector_cache = {}
        self.similarity_cache = SimilarityCache()
        
    async def cached_search(self, query_vector, top_k=10):
        """Multi-level cached search"""
        # Level 1: Exact query cache
        cache_key = self._hash_vector(query_vector)
        if cache_key in self.query_cache:
            return self.query_cache[cache_key]
        
        # Level 2: Similar query cache
        similar_results = self.similarity_cache.find_similar(
            query_vector, 
            threshold=0.95
        )
        if similar_results:
            return similar_results
        
        # Level 3: Perform actual search
        results = await self.vector_store.search(query_vector, top_k * 2)
        
        # Update caches
        self.query_cache[cache_key] = results[:top_k]
        self.similarity_cache.add(query_vector, results)
        
        return results[:top_k]
    
    def _hash_vector(self, vector):
        """Create hash key for vector"""
        # Quantize vector for better cache hit rate
        quantized = np.round(vector * 1000).astype(int)
        return hash(quantized.tobytes())
```

## Production Deployment

### Kubernetes Deployment

```yaml
# Vector database on Kubernetes
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: vector-db-cluster
spec:
  serviceName: vector-db
  replicas: 3
  selector:
    matchLabels:
      app: vector-db
  template:
    metadata:
      labels:
        app: vector-db
    spec:
      containers:
      - name: vector-db
        image: qdrant/qdrant:latest
        ports:
        - containerPort: 6333
          name: api
        - containerPort: 6334
          name: grpc
        env:
        - name: QDRANT__CLUSTER__ENABLED
          value: "true"
        - name: QDRANT__CLUSTER__P2P__PORT
          value: "6335"
        volumeMounts:
        - name: storage
          mountPath: /qdrant/storage
        resources:
          requests:
            memory: "4Gi"
            cpu: "2"
          limits:
            memory: "8Gi"
            cpu: "4"
        livenessProbe:
          httpGet:
            path: /health
            port: 6333
          initialDelaySeconds: 30
          periodSeconds: 10
  volumeClaimTemplates:
  - metadata:
      name: storage
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 100Gi

---
apiVersion: v1
kind: Service
metadata:
  name: vector-db
spec:
  clusterIP: None
  selector:
    app: vector-db
  ports:
  - name: api
    port: 6333
  - name: grpc
    port: 6334
```

### Monitoring and Observability

```python
# Vector database monitoring
class VectorDBMonitoring:
    def __init__(self):
        self.prometheus = PrometheusClient()
        self.metrics = {
            'search_latency': Histogram(
                'vector_search_duration_seconds',
                'Vector search latency'
            ),
            'index_size': Gauge(
                'vector_index_size_bytes',
                'Size of vector index'
            ),
            'query_recall': Gauge(
                'vector_search_recall',
                'Search recall metric'
            ),
            'insertion_rate': Counter(
                'vector_insertions_total',
                'Total vector insertions'
            )
        }
    
    def record_search(self, duration, recall_score):
        """Record search metrics"""
        self.metrics['search_latency'].observe(duration)
        self.metrics['query_recall'].set(recall_score)
    
    def create_dashboard_config(self):
        """Grafana dashboard configuration"""
        return {
            "dashboard": {
                "title": "Vector Database Metrics",
                "panels": [
                    {
                        "title": "Search Latency",
                        "targets": [{
                            "expr": "histogram_quantile(0.95, vector_search_duration_seconds_bucket)"
                        }]
                    },
                    {
                        "title": "Insertion Rate",
                        "targets": [{
                            "expr": "rate(vector_insertions_total[5m])"
                        }]
                    },
                    {
                        "title": "Recall Score",
                        "targets": [{
                            "expr": "vector_search_recall"
                        }]
                    }
                ]
            }
        }
```

## Interview Questions

### System Design
1. Design a distributed vector database for 1 billion embeddings
2. Build a real-time recommendation system using vectors
3. Create a semantic search engine for code
4. Design a multi-modal search system (text + images)

### Implementation
1. Implement approximate nearest neighbor search
2. Build a vector database shard rebalancer
3. Create a query optimizer for hybrid search
4. Implement vector quantization for compression

### Optimization
1. How to handle hot partitions in vector databases?
2. Optimize vector search for mobile devices
3. Reduce memory usage for large-scale deployment
4. Implement progressive vector indexing

## Essential Resources

### Documentation
- 📖 [Pinecone Documentation](https://docs.pinecone.io/)
- 📖 [Weaviate Documentation](https://weaviate.io/developers/weaviate)
- 📖 [Qdrant Documentation](https://qdrant.tech/documentation/)
- 📖 [Milvus Documentation](https://milvus.io/docs)

### Papers
- 📄 [Faiss: A Library for Efficient Similarity Search](https://arxiv.org/abs/1702.08734)
- 📄 [Billion-scale similarity search with GPUs](https://arxiv.org/abs/1702.08734)
- 📄 [HNSW: Hierarchical Navigable Small World](https://arxiv.org/abs/1603.09320)

### Tools
- 🔧 [VectorDBBench](https://github.com/zilliztech/VectorDBBench) - Benchmarking
- 🔧 [ANN Benchmarks](https://github.com/erikbern/ann-benchmarks) - Algorithm comparison
- 🔧 [Faiss](https://github.com/facebookresearch/faiss) - Vector similarity library

### Courses
- 🎓 [Vector Databases Course](https://www.deeplearning.ai/short-courses/vector-databases-embeddings-applications/)
- 🎓 [Building LLM Applications](https://www.coursera.org/learn/building-llm-powered-applications)

Remember: Vector databases are the backbone of modern AI applications. Understanding their internals, optimization techniques, and deployment patterns is crucial for building production AI systems.