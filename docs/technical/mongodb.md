# MongoDB

MongoDB is a popular NoSQL document database designed for scalability and developer productivity. It stores data in flexible, JSON-like documents and is widely used for modern applications requiring schema flexibility and horizontal scaling.

## 📚 Top Learning Resources

### 🎥 Video Courses

#### **MongoDB Tutorial for Beginners - Complete Course**
- **Channel**: freeCodeCamp
- **Link**: [YouTube - 2.5 hours](https://www.youtube.com/watch?v=c2M-rlkkT5o)
- **Why it's great**: Comprehensive introduction to MongoDB concepts and operations

#### **MongoDB Crash Course**
- **Channel**: Traversy Media
- **Link**: [YouTube - 1 hour](https://www.youtube.com/watch?v=-56x56UppqQ)
- **Why it's great**: Quick start guide with practical examples and CRUD operations

#### **MongoDB University - Complete Developer Course**
- **Channel**: MongoDB
- **Link**: [YouTube Playlist](https://www.youtube.com/playlist?list=PL4cUxeGkcC9jpvoYriLI0bY8DOgWZfi6u)
- **Why it's great**: Official training videos from MongoDB with hands-on exercises

### 📖 Essential Documentation

#### **MongoDB Official Documentation**
- **Link**: [docs.mongodb.com](https://docs.mongodb.com/)
- **Why it's great**: Comprehensive official documentation with tutorials and examples

#### **MongoDB Manual**
- **Link**: [docs.mongodb.com/manual/](https://docs.mongodb.com/manual/)
- **Why it's great**: Complete reference for MongoDB features and operations

#### **MongoDB Best Practices**
- **Link**: [docs.mongodb.com/manual/administration/production-notes/](https://docs.mongodb.com/manual/administration/production-notes/)
- **Why it's great**: Essential guide for production deployments and optimization

### 📝 Must-Read Blogs & Articles

#### **MongoDB Blog**
- **Source**: MongoDB Inc.
- **Link**: [mongodb.com/blog](https://www.mongodb.com/blog)
- **Why it's great**: Official updates, use cases, and technical insights

#### **MongoDB vs SQL Databases**
- **Source**: MongoDB
- **Link**: [mongodb.com/compare/mongodb-mysql](https://www.mongodb.com/compare/mongodb-mysql)
- **Why it's great**: Comprehensive comparison of NoSQL vs SQL approaches

#### **MongoDB Performance Tuning**
- **Source**: Studio 3T
- **Link**: [studio3t.com/knowledge-base/articles/mongodb-performance-tuning/](https://studio3t.com/knowledge-base/articles/mongodb-performance-tuning/)
- **Why it's great**: Practical performance optimization techniques

### 🎓 Structured Courses

#### **MongoDB University**
- **Platform**: MongoDB Inc.
- **Link**: [university.mongodb.com](https://university.mongodb.com/)
- **Cost**: Free
- **Why it's great**: Official MongoDB certification courses with hands-on labs

#### **Complete MongoDB Developer Course**
- **Platform**: Udemy
- **Link**: [udemy.com/course/the-complete-developers-guide-to-mongodb/](https://www.udemy.com/course/the-complete-developers-guide-to-mongodb/)
- **Cost**: Paid
- **Why it's great**: Comprehensive course with real-world application development

### 🛠️ Tools & Platforms

#### **MongoDB Atlas**
- **Link**: [cloud.mongodb.com](https://cloud.mongodb.com/)
- **Why it's great**: Fully managed MongoDB service with generous free tier

#### **MongoDB Compass**
- **Link**: [mongodb.com/products/compass](https://www.mongodb.com/products/compass)
- **Why it's great**: Official GUI for MongoDB with visual query building

#### **Studio 3T**
- **Link**: [studio3t.com](https://studio3t.com/)
- **Why it's great**: Professional MongoDB IDE with advanced query and management features

## Overview

MongoDB is a popular NoSQL document database designed for scalability and developer productivity. It stores data in flexible, JSON-like documents and is widely used for modern applications requiring schema flexibility and horizontal scaling.

## Key Features

- **Document-Oriented**: Store data in BSON (Binary JSON) documents
- **Schema Flexibility**: Dynamic schemas allow easy data model evolution
- **Horizontal Scaling**: Built-in sharding for distributed data
- **High Performance**: Optimized for both reads and writes
- **Rich Query Language**: Powerful aggregation framework

## Common Use Cases

### Basic Operations
```javascript
// Connect to MongoDB
const { MongoClient } = require('mongodb');
const client = new MongoClient('mongodb://localhost:27017');

// Insert documents
const db = client.db('myapp');
const users = db.collection('users');

await users.insertOne({
  username: 'john_doe',
  email: 'john@example.com',
  profile: {
    firstName: 'John',
    lastName: 'Doe',
    age: 30
  },
  tags: ['developer', 'nodejs'],
  createdAt: new Date()
});

// Query documents
const user = await users.findOne({ username: 'john_doe' });
const developers = await users.find({ tags: 'developer' }).toArray();
```

### Aggregation Pipeline
```javascript
// Complex data aggregation
const pipeline = [
  { $match: { 'profile.age': { $gte: 25 } } },
  { $group: {
      _id: '$department',
      avgAge: { $avg: '$profile.age' },
      count: { $sum: 1 }
    }
  },
  { $sort: { avgAge: -1 } },
  { $limit: 10 }
];

const results = await users.aggregate(pipeline).toArray();
```

### Indexing for Performance
```javascript
// Create indexes
await users.createIndex({ email: 1 });  // Single field
await users.createIndex({ 'profile.age': 1, department: -1 });  // Compound
await users.createIndex({ tags: 1 });  // Array field
await users.createIndex({ username: 'text', 'profile.firstName': 'text' });  // Text search

// Query with index hints
const result = await users.find({ email: 'john@example.com' })
  .hint({ email: 1 })
  .explain('executionStats');
```

## Configuration

### Production mongod.conf
```yaml
# Network settings
net:
  port: 27017
  bindIp: 0.0.0.0

# Storage settings
storage:
  dbPath: /var/lib/mongodb
  journal:
    enabled: true
  wiredTiger:
    engineConfig:
      cacheSizeGB: 2

# Security
security:
  authorization: enabled
  keyFile: /etc/mongodb/keyfile

# Replication
replication:
  replSetName: "rs0"

# Sharding
sharding:
  clusterRole: shardsvr
```

### Replica Set Setup
```javascript
// Initialize replica set
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongo1:27017" },
    { _id: 1, host: "mongo2:27017" },
    { _id: 2, host: "mongo3:27017" }
  ]
});

// Check replica set status
rs.status();
```

## Monitoring and Maintenance

### Performance Monitoring
```javascript
// Database statistics
db.stats();
db.users.stats();

// Current operations
db.currentOp();

// Profiler for slow operations
db.setProfilingLevel(2, { slowms: 100 });
db.system.profile.find().limit(5).sort({ ts: -1 });
```

### Backup and Recovery
```bash
# Backup with mongodump
mongodump --host localhost:27017 --db myapp --out /backup/

# Restore with mongorestore
mongorestore --host localhost:27017 --db myapp /backup/myapp/

# Replica set backup
mongodump --host rs0/mongo1:27017,mongo2:27017,mongo3:27017 --db myapp
```

## Best Practices

- Design schema for your query patterns
- Use appropriate indexes for better performance
- Implement proper sharding strategy for large datasets
- Use replica sets for high availability
- Monitor slow operations and optimize queries
- Regular backups and disaster recovery testing
- Security: authentication, authorization, and encryption

## Great Resources

- [MongoDB Official Documentation](https://docs.mongodb.com/) - Comprehensive MongoDB guide and reference
- [MongoDB University](https://university.mongodb.com/) - Free courses and certifications
- [MongoDB Compass](https://www.mongodb.com/products/compass) - Visual MongoDB database explorer
- [MongoDB Performance Best Practices](https://www.mongodb.com/basics/best-practices) - Official performance guide
- [Studio 3T](https://studio3t.com/) - Professional MongoDB IDE and client
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) - Fully managed MongoDB cloud service
- [awesome-mongodb](https://github.com/ramnes/awesome-mongodb) - Curated list of MongoDB resources