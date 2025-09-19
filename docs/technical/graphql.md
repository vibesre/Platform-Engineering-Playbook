# GraphQL

GraphQL is a query language and runtime for APIs that allows clients to request exactly the data they need. It provides a complete and understandable description of the data in your API and gives clients the power to ask for exactly what they need.

## Installation

### Node.js/JavaScript
```bash
# Core GraphQL library
npm install graphql

# Apollo Server (popular GraphQL server)
npm install apollo-server-express express

# GraphQL tools
npm install @graphql-tools/schema @graphql-tools/load-files

# Development tools
npm install --save-dev @graphql-codegen/cli @graphql-codegen/typescript

# Client libraries
npm install @apollo/client graphql
```

### Python
```bash
# Core GraphQL libraries
pip install graphql-core graphene

# FastAPI integration
pip install fastapi uvicorn

# GraphQL server frameworks
pip install strawberry-graphql
pip install ariadne

# Client libraries
pip install gql aiohttp
```

### Java
```xml
<!-- Maven dependencies -->
<dependencies>
    <dependency>
        <groupId>com.graphql-java</groupId>
        <artifactId>graphql-java</artifactId>
        <version>20.2</version>
    </dependency>
    <dependency>
        <groupId>com.graphql-java</groupId>
        <artifactId>graphql-java-tools</artifactId>
        <version>5.2.4</version>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-graphql</artifactId>
        <version>3.1.0</version>
    </dependency>
</dependencies>
```

### Go
```bash
# GraphQL Go libraries
go get github.com/graphql-go/graphql
go get github.com/99designs/gqlgen

# Generate GraphQL server
go run github.com/99designs/gqlgen generate
```

## Schema Definition

### Basic Schema
```graphql
# schema.graphql

# Scalar types
scalar DateTime
scalar Upload

# Enums
enum UserStatus {
  ACTIVE
  INACTIVE
  SUSPENDED
  PENDING
}

enum PostStatus {
  DRAFT
  PUBLISHED
  ARCHIVED
}

# Object types
type User {
  id: ID!
  username: String!
  email: String!
  firstName: String
  lastName: String
  avatar: String
  status: UserStatus!
  createdAt: DateTime!
  updatedAt: DateTime!
  posts: [Post!]!
  comments: [Comment!]!
  profile: UserProfile
}

type UserProfile {
  id: ID!
  bio: String
  website: String
  location: String
  birthday: DateTime
  user: User!
}

type Post {
  id: ID!
  title: String!
  content: String!
  excerpt: String
  slug: String!
  status: PostStatus!
  publishedAt: DateTime
  createdAt: DateTime!
  updatedAt: DateTime!
  author: User!
  comments: [Comment!]!
  tags: [Tag!]!
  likes: Int!
  views: Int!
}

type Comment {
  id: ID!
  content: String!
  createdAt: DateTime!
  updatedAt: DateTime!
  author: User!
  post: Post!
  parent: Comment
  replies: [Comment!]!
}

type Tag {
  id: ID!
  name: String!
  slug: String!
  description: String
  posts: [Post!]!
}

# Input types
input CreateUserInput {
  username: String!
  email: String!
  password: String!
  firstName: String
  lastName: String
}

input UpdateUserInput {
  username: String
  email: String
  firstName: String
  lastName: String
  avatar: Upload
}

input CreatePostInput {
  title: String!
  content: String!
  excerpt: String
  slug: String
  status: PostStatus = DRAFT
  tags: [String!]
}

input UpdatePostInput {
  title: String
  content: String
  excerpt: String
  slug: String
  status: PostStatus
  tags: [String!]
}

input PostFilters {
  status: PostStatus
  authorId: ID
  tags: [String!]
  publishedAfter: DateTime
  publishedBefore: DateTime
  search: String
}

input PaginationInput {
  page: Int = 1
  limit: Int = 10
}

input SortInput {
  field: String!
  direction: SortDirection = ASC
}

enum SortDirection {
  ASC
  DESC
}

# Response types
type PaginatedPosts {
  posts: [Post!]!
  totalCount: Int!
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  page: Int!
  totalPages: Int!
}

type AuthPayload {
  token: String!
  user: User!
  expiresAt: DateTime!
}

type MutationResponse {
  success: Boolean!
  message: String
  errors: [String!]
}

# Root types
type Query {
  # User queries
  me: User
  user(id: ID!): User
  users(filters: UserFilters, pagination: PaginationInput, sort: SortInput): [User!]!
  
  # Post queries
  post(id: ID, slug: String): Post
  posts(filters: PostFilters, pagination: PaginationInput, sort: SortInput): PaginatedPosts!
  
  # Tag queries
  tag(id: ID, slug: String): Tag
  tags: [Tag!]!
  
  # Search
  search(query: String!, type: SearchType): SearchResults!
}

type Mutation {
  # Authentication
  register(input: CreateUserInput!): AuthPayload!
  login(email: String!, password: String!): AuthPayload!
  logout: MutationResponse!
  
  # User mutations
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): MutationResponse!
  
  # Post mutations
  createPost(input: CreatePostInput!): Post!
  updatePost(id: ID!, input: UpdatePostInput!): Post!
  deletePost(id: ID!): MutationResponse!
  publishPost(id: ID!): Post!
  
  # Comment mutations
  createComment(postId: ID!, content: String!, parentId: ID): Comment!
  updateComment(id: ID!, content: String!): Comment!
  deleteComment(id: ID!): MutationResponse!
  
  # Interactions
  likePost(postId: ID!): Post!
  unlikePost(postId: ID!): Post!
}

type Subscription {
  # Real-time updates
  postCreated: Post!
  postUpdated(postId: ID): Post!
  commentAdded(postId: ID!): Comment!
  userStatusChanged: User!
  
  # Notifications
  notifications(userId: ID!): Notification!
}

# Additional types for subscriptions
type Notification {
  id: ID!
  type: NotificationType!
  title: String!
  message: String!
  data: String
  read: Boolean!
  createdAt: DateTime!
}

enum NotificationType {
  POST_LIKED
  POST_COMMENTED
  USER_FOLLOWED
  SYSTEM_ANNOUNCEMENT
}

enum SearchType {
  ALL
  POSTS
  USERS
  TAGS
}

union SearchResults = Post | User | Tag
```

## Server Implementation

### Node.js with Apollo Server
```javascript
const { ApolloServer } = require('apollo-server-express');
const { gql } = require('apollo-server-express');
const { PubSub } = require('graphql-subscriptions');
const { createServer } = require('http');
const { execute, subscribe } = require('graphql');
const { SubscriptionServer } = require('subscriptions-transport-ws');
const { makeExecutableSchema } = require('@graphql-tools/schema');
const express = require('express');
const jwt = require('jsonwebtoken');

const pubsub = new PubSub();

// Type definitions
const typeDefs = gql`
  # ... (schema from above)
`;

// Resolvers
const resolvers = {
  Query: {
    me: async (parent, args, context) => {
      if (!context.user) {
        throw new Error('Not authenticated');
      }
      return await User.findById(context.user.id);
    },
    
    user: async (parent, { id }) => {
      return await User.findById(id).populate('posts comments profile');
    },
    
    users: async (parent, { filters, pagination, sort }) => {
      const query = User.find();
      
      // Apply filters
      if (filters?.status) {
        query.where('status', filters.status);
      }
      
      // Apply sorting
      if (sort) {
        const sortOrder = sort.direction === 'DESC' ? -1 : 1;
        query.sort({ [sort.field]: sortOrder });
      }
      
      // Apply pagination
      if (pagination) {
        const skip = (pagination.page - 1) * pagination.limit;
        query.skip(skip).limit(pagination.limit);
      }
      
      return await query.exec();
    },
    
    post: async (parent, { id, slug }) => {
      if (id) {
        return await Post.findById(id).populate('author comments tags');
      }
      if (slug) {
        return await Post.findOne({ slug }).populate('author comments tags');
      }
      throw new Error('Either id or slug must be provided');
    },
    
    posts: async (parent, { filters, pagination, sort }) => {
      const query = Post.find();
      
      // Apply filters
      if (filters) {
        if (filters.status) {
          query.where('status', filters.status);
        }
        if (filters.authorId) {
          query.where('author', filters.authorId);
        }
        if (filters.tags && filters.tags.length > 0) {
          query.where('tags').in(filters.tags);
        }
        if (filters.publishedAfter) {
          query.where('publishedAt').gte(filters.publishedAfter);
        }
        if (filters.publishedBefore) {
          query.where('publishedAt').lte(filters.publishedBefore);
        }
        if (filters.search) {
          query.where({
            $or: [
              { title: { $regex: filters.search, $options: 'i' } },
              { content: { $regex: filters.search, $options: 'i' } }
            ]
          });
        }
      }
      
      // Count total for pagination
      const totalCount = await Post.countDocuments(query.getQuery());
      
      // Apply sorting
      if (sort) {
        const sortOrder = sort.direction === 'DESC' ? -1 : 1;
        query.sort({ [sort.field]: sortOrder });
      }
      
      // Apply pagination
      const page = pagination?.page || 1;
      const limit = pagination?.limit || 10;
      const skip = (page - 1) * limit;
      
      query.skip(skip).limit(limit);
      
      const posts = await query.populate('author tags').exec();
      
      return {
        posts,
        totalCount,
        hasNextPage: skip + limit < totalCount,
        hasPreviousPage: page > 1,
        page,
        totalPages: Math.ceil(totalCount / limit)
      };
    },
    
    search: async (parent, { query, type }) => {
      const results = [];
      
      if (type === 'ALL' || type === 'POSTS') {
        const posts = await Post.find({
          $or: [
            { title: { $regex: query, $options: 'i' } },
            { content: { $regex: query, $options: 'i' } }
          ]
        }).limit(10);
        results.push(...posts);
      }
      
      if (type === 'ALL' || type === 'USERS') {
        const users = await User.find({
          $or: [
            { username: { $regex: query, $options: 'i' } },
            { firstName: { $regex: query, $options: 'i' } },
            { lastName: { $regex: query, $options: 'i' } }
          ]
        }).limit(10);
        results.push(...users);
      }
      
      if (type === 'ALL' || type === 'TAGS') {
        const tags = await Tag.find({
          name: { $regex: query, $options: 'i' }
        }).limit(10);
        results.push(...tags);
      }
      
      return results;
    }
  },
  
  Mutation: {
    register: async (parent, { input }) => {
      const existingUser = await User.findOne({
        $or: [{ email: input.email }, { username: input.username }]
      });
      
      if (existingUser) {
        throw new Error('User already exists');
      }
      
      const hashedPassword = await bcrypt.hash(input.password, 10);
      
      const user = new User({
        ...input,
        password: hashedPassword,
        status: 'ACTIVE'
      });
      
      await user.save();
      
      const token = jwt.sign(
        { id: user.id, email: user.email },
        process.env.JWT_SECRET,
        { expiresIn: '7d' }
      );
      
      return {
        token,
        user,
        expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
      };
    },
    
    login: async (parent, { email, password }) => {
      const user = await User.findOne({ email });
      
      if (!user) {
        throw new Error('Invalid credentials');
      }
      
      const valid = await bcrypt.compare(password, user.password);
      
      if (!valid) {
        throw new Error('Invalid credentials');
      }
      
      const token = jwt.sign(
        { id: user.id, email: user.email },
        process.env.JWT_SECRET,
        { expiresIn: '7d' }
      );
      
      return {
        token,
        user,
        expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
      };
    },
    
    createPost: async (parent, { input }, context) => {
      if (!context.user) {
        throw new Error('Not authenticated');
      }
      
      // Generate slug if not provided
      const slug = input.slug || generateSlug(input.title);
      
      // Check if slug already exists
      const existingPost = await Post.findOne({ slug });
      if (existingPost) {
        throw new Error('Post with this slug already exists');
      }
      
      const post = new Post({
        ...input,
        slug,
        author: context.user.id
      });
      
      await post.save();
      await post.populate('author tags');
      
      // Publish subscription
      pubsub.publish('POST_CREATED', { postCreated: post });
      
      return post;
    },
    
    updatePost: async (parent, { id, input }, context) => {
      if (!context.user) {
        throw new Error('Not authenticated');
      }
      
      const post = await Post.findById(id);
      
      if (!post) {
        throw new Error('Post not found');
      }
      
      if (post.author.toString() !== context.user.id && context.user.role !== 'ADMIN') {
        throw new Error('Not authorized');
      }
      
      Object.assign(post, input);
      post.updatedAt = new Date();
      
      await post.save();
      await post.populate('author tags');
      
      // Publish subscription
      pubsub.publish('POST_UPDATED', { postUpdated: post });
      
      return post;
    },
    
    createComment: async (parent, { postId, content, parentId }, context) => {
      if (!context.user) {
        throw new Error('Not authenticated');
      }
      
      const post = await Post.findById(postId);
      if (!post) {
        throw new Error('Post not found');
      }
      
      const comment = new Comment({
        content,
        author: context.user.id,
        post: postId,
        parent: parentId || null
      });
      
      await comment.save();
      await comment.populate('author post');
      
      // Publish subscription
      pubsub.publish('COMMENT_ADDED', { 
        commentAdded: comment,
        postId 
      });
      
      return comment;
    },
    
    likePost: async (parent, { postId }, context) => {
      if (!context.user) {
        throw new Error('Not authenticated');
      }
      
      const post = await Post.findByIdAndUpdate(
        postId,
        { $inc: { likes: 1 } },
        { new: true }
      ).populate('author tags');
      
      if (!post) {
        throw new Error('Post not found');
      }
      
      return post;
    }
  },
  
  Subscription: {
    postCreated: {
      subscribe: () => pubsub.asyncIterator('POST_CREATED')
    },
    
    postUpdated: {
      subscribe: (parent, { postId }) => {
        if (postId) {
          return pubsub.asyncIterator(`POST_UPDATED_${postId}`);
        }
        return pubsub.asyncIterator('POST_UPDATED');
      }
    },
    
    commentAdded: {
      subscribe: (parent, { postId }) => {
        return pubsub.asyncIterator(`COMMENT_ADDED_${postId}`);
      }
    }
  },
  
  // Field resolvers
  User: {
    posts: async (user) => {
      return await Post.find({ author: user.id }).populate('tags');
    },
    
    comments: async (user) => {
      return await Comment.find({ author: user.id }).populate('post');
    },
    
    profile: async (user) => {
      return await UserProfile.findOne({ user: user.id });
    }
  },
  
  Post: {
    author: async (post) => {
      return await User.findById(post.author);
    },
    
    comments: async (post) => {
      return await Comment.find({ post: post.id }).populate('author');
    },
    
    tags: async (post) => {
      return await Tag.find({ _id: { $in: post.tags } });
    }
  },
  
  Comment: {
    author: async (comment) => {
      return await User.findById(comment.author);
    },
    
    post: async (comment) => {
      return await Post.findById(comment.post);
    },
    
    replies: async (comment) => {
      return await Comment.find({ parent: comment.id }).populate('author');
    }
  },
  
  // Union resolver
  SearchResults: {
    __resolveType: (obj) => {
      if (obj.title && obj.content) {
        return 'Post';
      }
      if (obj.username && obj.email) {
        return 'User';
      }
      if (obj.name && !obj.username) {
        return 'Tag';
      }
      return null;
    }
  }
};

// Context function
const getContext = ({ req, connection }) => {
  // For subscriptions
  if (connection) {
    return connection.context;
  }
  
  // For queries and mutations
  const token = req.headers.authorization?.replace('Bearer ', '');
  
  if (token) {
    try {
      const decoded = jwt.verify(token, process.env.JWT_SECRET);
      return { user: decoded };
    } catch (error) {
      console.error('Invalid token:', error);
    }
  }
  
  return {};
};

// Create executable schema
const schema = makeExecutableSchema({
  typeDefs,
  resolvers
});

// Create Apollo Server
const server = new ApolloServer({
  schema,
  context: getContext,
  plugins: [
    {
      requestDidStart() {
        return {
          willSendResponse(requestContext) {
            console.log('GraphQL operation completed:', {
              operationName: requestContext.request.operationName,
              query: requestContext.request.query,
              variables: requestContext.request.variables
            });
          }
        };
      }
    }
  ]
});

// Setup Express app
const app = express();

async function startServer() {
  await server.start();
  server.applyMiddleware({ app, path: '/graphql' });
  
  const httpServer = createServer(app);
  
  // Setup subscription server
  const subscriptionServer = SubscriptionServer.create(
    {
      schema,
      execute,
      subscribe,
      onConnect: (connectionParams, webSocket, context) => {
        // Handle WebSocket authentication
        const token = connectionParams.authorization?.replace('Bearer ', '');
        
        if (token) {
          try {
            const decoded = jwt.verify(token, process.env.JWT_SECRET);
            return { user: decoded };
          } catch (error) {
            throw new Error('Invalid token');
          }
        }
        
        return {};
      }
    },
    {
      server: httpServer,
      path: server.graphqlPath
    }
  );
  
  const PORT = process.env.PORT || 4000;
  
  httpServer.listen(PORT, () => {
    console.log(`🚀 Server ready at http://localhost:${PORT}${server.graphqlPath}`);
    console.log(`🚀 Subscriptions ready at ws://localhost:${PORT}${server.graphqlPath}`);
  });
}

startServer().catch(error => {
  console.error('Error starting server:', error);
});
```

### Python with Strawberry
```python
import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.subscriptions import GRAPHQL_TRANSPORT_WS_PROTOCOL
from typing import List, Optional, Union, AsyncGenerator
import asyncio
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import bcrypt

# Types
@strawberry.enum
class UserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"
    PENDING = "PENDING"

@strawberry.enum
class PostStatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"

@strawberry.type
class User:
    id: strawberry.ID
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar: Optional[str] = None
    status: UserStatus
    created_at: datetime
    updated_at: datetime
    
    @strawberry.field
    async def posts(self) -> List["Post"]:
        # Fetch user's posts from database
        return await get_user_posts(self.id)
    
    @strawberry.field
    async def comments(self) -> List["Comment"]:
        # Fetch user's comments from database
        return await get_user_comments(self.id)

@strawberry.type
class Post:
    id: strawberry.ID
    title: str
    content: str
    excerpt: Optional[str] = None
    slug: str
    status: PostStatus
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    likes: int = 0
    views: int = 0
    
    @strawberry.field
    async def author(self) -> User:
        return await get_user_by_id(self.author_id)
    
    @strawberry.field
    async def comments(self) -> List["Comment"]:
        return await get_post_comments(self.id)
    
    @strawberry.field
    async def tags(self) -> List["Tag"]:
        return await get_post_tags(self.id)

@strawberry.type
class Comment:
    id: strawberry.ID
    content: str
    created_at: datetime
    updated_at: datetime
    
    @strawberry.field
    async def author(self) -> User:
        return await get_user_by_id(self.author_id)
    
    @strawberry.field
    async def post(self) -> Post:
        return await get_post_by_id(self.post_id)
    
    @strawberry.field
    async def replies(self) -> List["Comment"]:
        return await get_comment_replies(self.id)

@strawberry.type
class Tag:
    id: strawberry.ID
    name: str
    slug: str
    description: Optional[str] = None

# Input types
@strawberry.input
class CreateUserInput:
    username: str
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

@strawberry.input
class UpdateUserInput:
    username: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

@strawberry.input
class CreatePostInput:
    title: str
    content: str
    excerpt: Optional[str] = None
    slug: Optional[str] = None
    status: PostStatus = PostStatus.DRAFT
    tags: Optional[List[str]] = None

@strawberry.input
class PostFilters:
    status: Optional[PostStatus] = None
    author_id: Optional[strawberry.ID] = None
    tags: Optional[List[str]] = None
    search: Optional[str] = None

@strawberry.input
class PaginationInput:
    page: int = 1
    limit: int = 10

# Response types
@strawberry.type
class PaginatedPosts:
    posts: List[Post]
    total_count: int
    has_next_page: bool
    has_previous_page: bool
    page: int
    total_pages: int

@strawberry.type
class AuthPayload:
    token: str
    user: User
    expires_at: datetime

@strawberry.type
class MutationResponse:
    success: bool
    message: Optional[str] = None
    errors: Optional[List[str]] = None

# Union types
@strawberry.union
class SearchResult:
    Post = Post
    User = User
    Tag = Tag

# Authentication
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Optional[User]:
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        if user_id:
            return await get_user_by_id(user_id)
    except jwt.PyJWTError:
        pass
    return None

# Context
@strawberry.type
class Context:
    user: Optional[User] = None

def get_context() -> Context:
    return Context()

# Queries
@strawberry.type
class Query:
    @strawberry.field
    async def me(self, info: strawberry.Info) -> Optional[User]:
        if not info.context.user:
            raise Exception("Not authenticated")
        return info.context.user
    
    @strawberry.field
    async def user(self, id: strawberry.ID) -> Optional[User]:
        return await get_user_by_id(id)
    
    @strawberry.field
    async def users(self, pagination: Optional[PaginationInput] = None) -> List[User]:
        return await get_users(pagination)
    
    @strawberry.field
    async def post(self, id: Optional[strawberry.ID] = None, slug: Optional[str] = None) -> Optional[Post]:
        if id:
            return await get_post_by_id(id)
        elif slug:
            return await get_post_by_slug(slug)
        else:
            raise Exception("Either id or slug must be provided")
    
    @strawberry.field
    async def posts(
        self,
        filters: Optional[PostFilters] = None,
        pagination: Optional[PaginationInput] = None
    ) -> PaginatedPosts:
        return await get_posts(filters, pagination)
    
    @strawberry.field
    async def search(self, query: str) -> List[SearchResult]:
        results = []
        
        # Search posts
        posts = await search_posts(query)
        results.extend(posts)
        
        # Search users
        users = await search_users(query)
        results.extend(users)
        
        # Search tags
        tags = await search_tags(query)
        results.extend(tags)
        
        return results

# Mutations
@strawberry.type
class Mutation:
    @strawberry.field
    async def register(self, input: CreateUserInput) -> AuthPayload:
        # Check if user exists
        existing_user = await get_user_by_email_or_username(input.email, input.username)
        if existing_user:
            raise Exception("User already exists")
        
        # Hash password
        hashed_password = bcrypt.hashpw(input.password.encode(), bcrypt.gensalt())
        
        # Create user
        user_data = {
            **input.__dict__,
            "password": hashed_password.decode(),
            "status": UserStatus.ACTIVE,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        user = await create_user(user_data)
        
        # Generate token
        token = jwt.encode(
            {"user_id": user.id, "exp": datetime.utcnow() + timedelta(days=7)},
            SECRET_KEY,
            algorithm="HS256"
        )
        
        return AuthPayload(
            token=token,
            user=user,
            expires_at=datetime.now() + timedelta(days=7)
        )
    
    @strawberry.field
    async def login(self, email: str, password: str) -> AuthPayload:
        user = await get_user_by_email(email)
        if not user:
            raise Exception("Invalid credentials")
        
        if not bcrypt.checkpw(password.encode(), user.password.encode()):
            raise Exception("Invalid credentials")
        
        token = jwt.encode(
            {"user_id": user.id, "exp": datetime.utcnow() + timedelta(days=7)},
            SECRET_KEY,
            algorithm="HS256"
        )
        
        return AuthPayload(
            token=token,
            user=user,
            expires_at=datetime.now() + timedelta(days=7)
        )
    
    @strawberry.field
    async def create_post(self, input: CreatePostInput, info: strawberry.Info) -> Post:
        if not info.context.user:
            raise Exception("Not authenticated")
        
        # Generate slug if not provided
        slug = input.slug or generate_slug(input.title)
        
        # Check if slug exists
        existing_post = await get_post_by_slug(slug)
        if existing_post:
            raise Exception("Post with this slug already exists")
        
        post_data = {
            **input.__dict__,
            "slug": slug,
            "author_id": info.context.user.id,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        post = await create_post(post_data)
        
        # Publish subscription
        await publish_post_created(post)
        
        return post
    
    @strawberry.field
    async def update_post(
        self, 
        id: strawberry.ID, 
        input: UpdatePostInput, 
        info: strawberry.Info
    ) -> Post:
        if not info.context.user:
            raise Exception("Not authenticated")
        
        post = await get_post_by_id(id)
        if not post:
            raise Exception("Post not found")
        
        if post.author_id != info.context.user.id:
            raise Exception("Not authorized")
        
        updated_post = await update_post(id, input.__dict__)
        
        # Publish subscription
        await publish_post_updated(updated_post)
        
        return updated_post
    
    @strawberry.field
    async def create_comment(
        self,
        post_id: strawberry.ID,
        content: str,
        parent_id: Optional[strawberry.ID] = None,
        info: strawberry.Info = None
    ) -> Comment:
        if not info.context.user:
            raise Exception("Not authenticated")
        
        post = await get_post_by_id(post_id)
        if not post:
            raise Exception("Post not found")
        
        comment_data = {
            "content": content,
            "author_id": info.context.user.id,
            "post_id": post_id,
            "parent_id": parent_id,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        comment = await create_comment(comment_data)
        
        # Publish subscription
        await publish_comment_added(comment, post_id)
        
        return comment

# Subscriptions
@strawberry.type
class Subscription:
    @strawberry.subscription
    async def post_created(self) -> AsyncGenerator[Post, None]:
        async for post in subscribe_to_post_created():
            yield post
    
    @strawberry.subscription
    async def post_updated(self, post_id: Optional[strawberry.ID] = None) -> AsyncGenerator[Post, None]:
        async for post in subscribe_to_post_updated(post_id):
            yield post
    
    @strawberry.subscription
    async def comment_added(self, post_id: strawberry.ID) -> AsyncGenerator[Comment, None]:
        async for comment in subscribe_to_comment_added(post_id):
            yield comment

# Create schema
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription
)

# FastAPI app
app = FastAPI()

# GraphQL router
graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,
    subscription_protocols=[GRAPHQL_TRANSPORT_WS_PROTOCOL]
)

app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Client Implementation

### React with Apollo Client
```jsx
import React from 'react';
import { 
  ApolloClient, 
  InMemoryCache, 
  ApolloProvider, 
  useQuery, 
  useMutation,
  useSubscription,
  gql 
} from '@apollo/client';
import { createUploadLink } from 'apollo-upload-client';
import { setContext } from '@apollo/client/link/context';
import { split } from '@apollo/client';
import { getMainDefinition } from '@apollo/client/utilities';
import { GraphQLWsLink } from '@apollo/client/link/subscriptions';
import { createClient } from 'graphql-ws';

// GraphQL queries
const GET_POSTS = gql`
  query GetPosts($filters: PostFilters, $pagination: PaginationInput) {
    posts(filters: $filters, pagination: $pagination) {
      posts {
        id
        title
        excerpt
        slug
        status
        publishedAt
        likes
        views
        author {
          id
          username
          avatar
        }
        tags {
          id
          name
          slug
        }
      }
      totalCount
      hasNextPage
      hasPreviousPage
      page
      totalPages
    }
  }
`;

const GET_POST = gql`
  query GetPost($id: ID, $slug: String) {
    post(id: $id, slug: $slug) {
      id
      title
      content
      excerpt
      slug
      status
      publishedAt
      createdAt
      updatedAt
      likes
      views
      author {
        id
        username
        firstName
        lastName
        avatar
      }
      comments {
        id
        content
        createdAt
        author {
          id
          username
          avatar
        }
        replies {
          id
          content
          createdAt
          author {
            id
            username
            avatar
          }
        }
      }
      tags {
        id
        name
        slug
      }
    }
  }
`;

const CREATE_POST = gql`
  mutation CreatePost($input: CreatePostInput!) {
    createPost(input: $input) {
      id
      title
      content
      slug
      status
      author {
        id
        username
      }
    }
  }
`;

const UPDATE_POST = gql`
  mutation UpdatePost($id: ID!, $input: UpdatePostInput!) {
    updatePost(id: $id, input: $input) {
      id
      title
      content
      slug
      status
      updatedAt
    }
  }
`;

const CREATE_COMMENT = gql`
  mutation CreateComment($postId: ID!, $content: String!, $parentId: ID) {
    createComment(postId: $postId, content: $content, parentId: $parentId) {
      id
      content
      createdAt
      author {
        id
        username
        avatar
      }
    }
  }
`;

const LOGIN = gql`
  mutation Login($email: String!, $password: String!) {
    login(email: $email, password: $password) {
      token
      user {
        id
        username
        email
        firstName
        lastName
      }
      expiresAt
    }
  }
`;

// Subscriptions
const POST_CREATED_SUBSCRIPTION = gql`
  subscription PostCreated {
    postCreated {
      id
      title
      excerpt
      author {
        id
        username
      }
    }
  }
`;

const COMMENT_ADDED_SUBSCRIPTION = gql`
  subscription CommentAdded($postId: ID!) {
    commentAdded(postId: $postId) {
      id
      content
      createdAt
      author {
        id
        username
        avatar
      }
    }
  }
`;

// Apollo Client setup
const httpLink = createUploadLink({
  uri: 'http://localhost:4000/graphql',
});

const authLink = setContext((_, { headers }) => {
  const token = localStorage.getItem('authToken');
  return {
    headers: {
      ...headers,
      authorization: token ? `Bearer ${token}` : "",
    }
  };
});

const wsLink = new GraphQLWsLink(
  createClient({
    url: 'ws://localhost:4000/graphql',
    connectionParams: () => {
      const token = localStorage.getItem('authToken');
      return {
        authorization: token ? `Bearer ${token}` : "",
      };
    },
  })
);

const splitLink = split(
  ({ query }) => {
    const definition = getMainDefinition(query);
    return (
      definition.kind === 'OperationDefinition' &&
      definition.operation === 'subscription'
    );
  },
  wsLink,
  authLink.concat(httpLink),
);

const client = new ApolloClient({
  link: splitLink,
  cache: new InMemoryCache({
    typePolicies: {
      Post: {
        fields: {
          comments: {
            merge(existing = [], incoming) {
              return [...existing, ...incoming];
            }
          }
        }
      }
    }
  }),
});

// Components
const PostList = () => {
  const [page, setPage] = React.useState(1);
  const [filters, setFilters] = React.useState({});
  
  const { loading, error, data, refetch } = useQuery(GET_POSTS, {
    variables: {
      pagination: { page, limit: 10 },
      filters
    },
    notifyOnNetworkStatusChange: true
  });
  
  useSubscription(POST_CREATED_SUBSCRIPTION, {
    onSubscriptionData: ({ subscriptionData }) => {
      if (subscriptionData.data) {
        refetch();
      }
    }
  });
  
  if (loading) return <div>Loading posts...</div>;
  if (error) return <div>Error: {error.message}</div>;
  
  const { posts, totalPages, hasNextPage, hasPreviousPage } = data.posts;
  
  return (
    <div className="post-list">
      <div className="filters">
        <select onChange={(e) => setFilters({ ...filters, status: e.target.value })}>
          <option value="">All Status</option>
          <option value="PUBLISHED">Published</option>
          <option value="DRAFT">Draft</option>
        </select>
        <input
          type="text"
          placeholder="Search posts..."
          onChange={(e) => setFilters({ ...filters, search: e.target.value })}
        />
      </div>
      
      <div className="posts">
        {posts.map(post => (
          <div key={post.id} className="post-card">
            <h3>
              <a href={`/posts/${post.slug}`}>{post.title}</a>
            </h3>
            <p>{post.excerpt}</p>
            <div className="post-meta">
              <span>By {post.author.username}</span>
              <span>{post.likes} likes</span>
              <span>{post.views} views</span>
            </div>
            <div className="tags">
              {post.tags.map(tag => (
                <span key={tag.id} className="tag">{tag.name}</span>
              ))}
            </div>
          </div>
        ))}
      </div>
      
      <div className="pagination">
        <button 
          disabled={!hasPreviousPage} 
          onClick={() => setPage(p => p - 1)}
        >
          Previous
        </button>
        <span>Page {page} of {totalPages}</span>
        <button 
          disabled={!hasNextPage} 
          onClick={() => setPage(p => p + 1)}
        >
          Next
        </button>
      </div>
    </div>
  );
};

const PostDetail = ({ postId, slug }) => {
  const { loading, error, data } = useQuery(GET_POST, {
    variables: { id: postId, slug },
    skip: !postId && !slug
  });
  
  const [createComment] = useMutation(CREATE_COMMENT, {
    refetchQueries: [{ query: GET_POST, variables: { id: postId, slug } }]
  });
  
  const [newComment, setNewComment] = React.useState('');
  
  useSubscription(COMMENT_ADDED_SUBSCRIPTION, {
    variables: { postId: data?.post?.id },
    skip: !data?.post?.id,
    onSubscriptionData: ({ subscriptionData, client }) => {
      if (subscriptionData.data) {
        const newComment = subscriptionData.data.commentAdded;
        
        // Update cache
        client.cache.modify({
          id: client.cache.identify(data.post),
          fields: {
            comments(existingComments = []) {
              return [...existingComments, newComment];
            }
          }
        });
      }
    }
  });
  
  if (loading) return <div>Loading post...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!data?.post) return <div>Post not found</div>;
  
  const { post } = data;
  
  const handleSubmitComment = async (e) => {
    e.preventDefault();
    if (!newComment.trim()) return;
    
    try {
      await createComment({
        variables: {
          postId: post.id,
          content: newComment
        }
      });
      setNewComment('');
    } catch (error) {
      console.error('Error creating comment:', error);
    }
  };
  
  return (
    <article className="post-detail">
      <header>
        <h1>{post.title}</h1>
        <div className="post-meta">
          <span>By {post.author.username}</span>
          <span>Published: {new Date(post.publishedAt).toLocaleDateString()}</span>
          <span>{post.likes} likes</span>
          <span>{post.views} views</span>
        </div>
        <div className="tags">
          {post.tags.map(tag => (
            <span key={tag.id} className="tag">{tag.name}</span>
          ))}
        </div>
      </header>
      
      <div className="post-content">
        {post.content}
      </div>
      
      <section className="comments">
        <h3>Comments ({post.comments.length})</h3>
        
        <form onSubmit={handleSubmitComment} className="comment-form">
          <textarea
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            placeholder="Write a comment..."
            rows={4}
          />
          <button type="submit">Submit Comment</button>
        </form>
        
        <div className="comments-list">
          {post.comments.map(comment => (
            <div key={comment.id} className="comment">
              <div className="comment-author">
                <img src={comment.author.avatar} alt={comment.author.username} />
                <span>{comment.author.username}</span>
                <span>{new Date(comment.createdAt).toLocaleDateString()}</span>
              </div>
              <div className="comment-content">{comment.content}</div>
              
              {comment.replies.length > 0 && (
                <div className="replies">
                  {comment.replies.map(reply => (
                    <div key={reply.id} className="reply">
                      <div className="reply-author">
                        <span>{reply.author.username}</span>
                        <span>{new Date(reply.createdAt).toLocaleDateString()}</span>
                      </div>
                      <div className="reply-content">{reply.content}</div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </section>
    </article>
  );
};

const CreatePostForm = () => {
  const [createPost, { loading, error }] = useMutation(CREATE_POST);
  const [formData, setFormData] = React.useState({
    title: '',
    content: '',
    excerpt: '',
    status: 'DRAFT',
    tags: []
  });
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const { data } = await createPost({
        variables: { input: formData }
      });
      
      // Redirect to new post
      window.location.href = `/posts/${data.createPost.slug}`;
    } catch (error) {
      console.error('Error creating post:', error);
    }
  };
  
  return (
    <form onSubmit={handleSubmit} className="create-post-form">
      <div className="form-group">
        <label>Title</label>
        <input
          type="text"
          value={formData.title}
          onChange={(e) => setFormData({ ...formData, title: e.target.value })}
          required
        />
      </div>
      
      <div className="form-group">
        <label>Content</label>
        <textarea
          value={formData.content}
          onChange={(e) => setFormData({ ...formData, content: e.target.value })}
          rows={10}
          required
        />
      </div>
      
      <div className="form-group">
        <label>Excerpt</label>
        <textarea
          value={formData.excerpt}
          onChange={(e) => setFormData({ ...formData, excerpt: e.target.value })}
          rows={3}
        />
      </div>
      
      <div className="form-group">
        <label>Status</label>
        <select
          value={formData.status}
          onChange={(e) => setFormData({ ...formData, status: e.target.value })}
        >
          <option value="DRAFT">Draft</option>
          <option value="PUBLISHED">Published</option>
        </select>
      </div>
      
      <button type="submit" disabled={loading}>
        {loading ? 'Creating...' : 'Create Post'}
      </button>
      
      {error && <div className="error">Error: {error.message}</div>}
    </form>
  );
};

const LoginForm = () => {
  const [login, { loading, error }] = useMutation(LOGIN);
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const { data } = await login({
        variables: { email, password }
      });
      
      // Store token
      localStorage.setItem('authToken', data.login.token);
      
      // Redirect to dashboard
      window.location.href = '/dashboard';
    } catch (error) {
      console.error('Login error:', error);
    }
  };
  
  return (
    <form onSubmit={handleSubmit} className="login-form">
      <div className="form-group">
        <label>Email</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>
      
      <div className="form-group">
        <label>Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      
      <button type="submit" disabled={loading}>
        {loading ? 'Logging in...' : 'Login'}
      </button>
      
      {error && <div className="error">Error: {error.message}</div>}
    </form>
  );
};

// Main App
const App = () => {
  return (
    <ApolloProvider client={client}>
      <div className="app">
        <header>
          <nav>
            <a href="/">Home</a>
            <a href="/posts">Posts</a>
            <a href="/create">Create Post</a>
            <a href="/login">Login</a>
          </nav>
        </header>
        
        <main>
          {/* Router would go here */}
          <PostList />
        </main>
      </div>
    </ApolloProvider>
  );
};

export default App;
```

## Testing

### Unit Testing with Jest
```javascript
import { ApolloServer } from 'apollo-server-express';
import { createTestClient } from 'apollo-server-testing';
import { gql } from 'apollo-server-express';
import { typeDefs, resolvers } from '../src/schema';

describe('GraphQL API', () => {
  let server;
  let query, mutate;
  
  beforeAll(() => {
    server = new ApolloServer({
      typeDefs,
      resolvers,
      context: () => ({
        user: { id: '1', email: 'test@example.com' }
      })
    });
    
    const testClient = createTestClient(server);
    query = testClient.query;
    mutate = testClient.mutate;
  });
  
  describe('User queries', () => {
    it('should fetch current user', async () => {
      const GET_ME = gql`
        query {
          me {
            id
            email
            username
          }
        }
      `;
      
      const { data, errors } = await query({ query: GET_ME });
      
      expect(errors).toBeUndefined();
      expect(data.me).toMatchObject({
        id: expect.any(String),
        email: expect.any(String),
        username: expect.any(String)
      });
    });
    
    it('should fetch user by ID', async () => {
      const GET_USER = gql`
        query GetUser($id: ID!) {
          user(id: $id) {
            id
            username
            email
          }
        }
      `;
      
      const { data, errors } = await query({
        query: GET_USER,
        variables: { id: '1' }
      });
      
      expect(errors).toBeUndefined();
      expect(data.user).toMatchObject({
        id: '1',
        username: expect.any(String),
        email: expect.any(String)
      });
    });
  });
  
  describe('Post mutations', () => {
    it('should create a new post', async () => {
      const CREATE_POST = gql`
        mutation CreatePost($input: CreatePostInput!) {
          createPost(input: $input) {
            id
            title
            content
            slug
            status
            author {
              id
              username
            }
          }
        }
      `;
      
      const input = {
        title: 'Test Post',
        content: 'This is a test post content',
        status: 'PUBLISHED'
      };
      
      const { data, errors } = await mutate({
        mutation: CREATE_POST,
        variables: { input }
      });
      
      expect(errors).toBeUndefined();
      expect(data.createPost).toMatchObject({
        id: expect.any(String),
        title: 'Test Post',
        content: 'This is a test post content',
        slug: expect.any(String),
        status: 'PUBLISHED',
        author: {
          id: expect.any(String),
          username: expect.any(String)
        }
      });
    });
    
    it('should handle validation errors', async () => {
      const CREATE_POST = gql`
        mutation CreatePost($input: CreatePostInput!) {
          createPost(input: $input) {
            id
            title
          }
        }
      `;
      
      const input = {
        title: '', // Invalid empty title
        content: 'Content without title'
      };
      
      const { errors } = await mutate({
        mutation: CREATE_POST,
        variables: { input }
      });
      
      expect(errors).toBeDefined();
      expect(errors[0].message).toContain('title');
    });
  });
  
  describe('Complex queries with relationships', () => {
    it('should fetch posts with author and comments', async () => {
      const GET_POSTS = gql`
        query {
          posts {
            posts {
              id
              title
              author {
                id
                username
              }
              comments {
                id
                content
                author {
                  id
                  username
                }
              }
            }
          }
        }
      `;
      
      const { data, errors } = await query({ query: GET_POSTS });
      
      expect(errors).toBeUndefined();
      expect(data.posts.posts).toBeInstanceOf(Array);
      
      if (data.posts.posts.length > 0) {
        const post = data.posts.posts[0];
        expect(post).toMatchObject({
          id: expect.any(String),
          title: expect.any(String),
          author: {
            id: expect.any(String),
            username: expect.any(String)
          }
        });
      }
    });
  });
  
  describe('Error handling', () => {
    it('should handle authentication errors', async () => {
      // Create server without user context
      const unauthenticatedServer = new ApolloServer({
        typeDefs,
        resolvers,
        context: () => ({}) // No user
      });
      
      const { query: unauthQuery } = createTestClient(unauthenticatedServer);
      
      const GET_ME = gql`
        query {
          me {
            id
            email
          }
        }
      `;
      
      const { errors } = await unauthQuery({ query: GET_ME });
      
      expect(errors).toBeDefined();
      expect(errors[0].message).toContain('Not authenticated');
    });
  });
});

// Integration tests
describe('GraphQL Integration Tests', () => {
  let server;
  
  beforeAll(async () => {
    // Setup test database
    await setupTestDatabase();
    
    server = new ApolloServer({
      typeDefs,
      resolvers,
      context: ({ req }) => {
        // Real authentication logic
        return getContextFromRequest(req);
      }
    });
  });
  
  afterAll(async () => {
    await cleanupTestDatabase();
  });
  
  it('should handle complete user workflow', async () => {
    const { query, mutate } = createTestClient(server);
    
    // 1. Register user
    const REGISTER = gql`
      mutation Register($input: CreateUserInput!) {
        register(input: $input) {
          token
          user {
            id
            username
            email
          }
        }
      }
    `;
    
    const registerInput = {
      username: 'testuser',
      email: 'test@example.com',
      password: 'password123',
      firstName: 'Test',
      lastName: 'User'
    };
    
    const { data: registerData } = await mutate({
      mutation: REGISTER,
      variables: { input: registerInput }
    });
    
    expect(registerData.register.user.username).toBe('testuser');
    
    // 2. Create post
    const CREATE_POST = gql`
      mutation CreatePost($input: CreatePostInput!) {
        createPost(input: $input) {
          id
          title
          slug
        }
      }
    `;
    
    const postInput = {
      title: 'Integration Test Post',
      content: 'This is an integration test post'
    };
    
    // Set authorization header
    const authHeaders = {
      authorization: `Bearer ${registerData.register.token}`
    };
    
    const { data: postData } = await mutate({
      mutation: CREATE_POST,
      variables: { input: postInput },
      context: { headers: authHeaders }
    });
    
    expect(postData.createPost.title).toBe('Integration Test Post');
    
    // 3. Fetch the created post
    const GET_POST = gql`
      query GetPost($id: ID!) {
        post(id: $id) {
          id
          title
          content
          author {
            id
            username
          }
        }
      }
    `;
    
    const { data: fetchedPost } = await query({
      query: GET_POST,
      variables: { id: postData.createPost.id }
    });
    
    expect(fetchedPost.post.author.username).toBe('testuser');
  });
});
```

### Performance Testing
```javascript
import { performance } from 'perf_hooks';
import { ApolloServer } from 'apollo-server-express';
import { createTestClient } from 'apollo-server-testing';
import { gql } from 'apollo-server-express';

class GraphQLPerformanceTester {
  constructor(server) {
    this.server = server;
    this.testClient = createTestClient(server);
    this.results = [];
  }
  
  async measureQuery(query, variables = {}, iterations = 100) {
    const times = [];
    
    for (let i = 0; i < iterations; i++) {
      const start = performance.now();
      
      try {
        await this.testClient.query({ query, variables });
        const end = performance.now();
        times.push(end - start);
      } catch (error) {
        console.error(`Query failed on iteration ${i}:`, error);
      }
    }
    
    return this.calculateStats(times);
  }
  
  async measureMutation(mutation, variables = {}, iterations = 50) {
    const times = [];
    
    for (let i = 0; i < iterations; i++) {
      const start = performance.now();
      
      try {
        await this.testClient.mutate({ mutation, variables });
        const end = performance.now();
        times.push(end - start);
      } catch (error) {
        console.error(`Mutation failed on iteration ${i}:`, error);
      }
    }
    
    return this.calculateStats(times);
  }
  
  calculateStats(times) {
    const sorted = times.sort((a, b) => a - b);
    
    return {
      min: sorted[0],
      max: sorted[sorted.length - 1],
      mean: times.reduce((a, b) => a + b, 0) / times.length,
      median: sorted[Math.floor(sorted.length / 2)],
      p95: sorted[Math.floor(sorted.length * 0.95)],
      p99: sorted[Math.floor(sorted.length * 0.99)],
      samples: times.length
    };
  }
  
  async runPerformanceTests() {
    console.log('Running GraphQL Performance Tests...\n');
    
    // Test simple query
    const SIMPLE_QUERY = gql`
      query {
        posts {
          posts {
            id
            title
          }
        }
      }
    `;
    
    const simpleStats = await this.measureQuery(SIMPLE_QUERY);
    console.log('Simple Query Performance:', simpleStats);
    
    // Test complex query with relationships
    const COMPLEX_QUERY = gql`
      query {
        posts {
          posts {
            id
            title
            content
            author {
              id
              username
              profile {
                bio
                website
              }
            }
            comments {
              id
              content
              author {
                id
                username
              }
              replies {
                id
                content
                author {
                  id
                  username
                }
              }
            }
            tags {
              id
              name
            }
          }
        }
      }
    `;
    
    const complexStats = await this.measureQuery(COMPLEX_QUERY);
    console.log('Complex Query Performance:', complexStats);
    
    // Test mutation
    const CREATE_POST = gql`
      mutation CreatePost($input: CreatePostInput!) {
        createPost(input: $input) {
          id
          title
          slug
        }
      }
    `;
    
    const mutationStats = await this.measureMutation(CREATE_POST, {
      input: {
        title: 'Performance Test Post',
        content: 'This is a performance test post'
      }
    });
    console.log('Mutation Performance:', mutationStats);
    
    // Test with varying query depths
    await this.testQueryDepth();
  }
  
  async testQueryDepth() {
    console.log('\nTesting Query Depth Performance...');
    
    for (let depth = 1; depth <= 5; depth++) {
      const query = this.generateNestedQuery(depth);
      const stats = await this.measureQuery(query, {}, 50);
      
      console.log(`Depth ${depth}:`, {
        mean: stats.mean.toFixed(2) + 'ms',
        p95: stats.p95.toFixed(2) + 'ms'
      });
    }
  }
  
  generateNestedQuery(depth) {
    let queryString = `
      query {
        posts {
          posts {
            id
            title
    `;
    
    let currentNesting = '';
    for (let i = 0; i < depth; i++) {
      currentNesting += `
        comments {
          id
          content
          author {
            id
            username
          }
      `;
    }
    
    // Close all nested levels
    for (let i = 0; i < depth; i++) {
      currentNesting += '}';
    }
    
    queryString += currentNesting + `
          }
        }
      }
    `;
    
    return gql(queryString);
  }
}

// Run performance tests
async function runTests() {
  const server = new ApolloServer({
    typeDefs,
    resolvers,
    context: () => ({
      user: { id: '1', email: 'test@example.com' }
    })
  });
  
  const tester = new GraphQLPerformanceTester(server);
  await tester.runPerformanceTests();
}

runTests().catch(console.error);
```

## Resources

- [GraphQL Documentation](https://graphql.org/learn/)
- [Apollo Server](https://www.apollographql.com/docs/apollo-server/)
- [Apollo Client](https://www.apollographql.com/docs/react/)
- [GraphQL Tools](https://www.graphql-tools.com/)
- [Strawberry GraphQL](https://strawberry.rocks/)
- [Graphene Python](https://graphene-python.org/)
- [GraphQL Java](https://www.graphql-java.com/)
- [Best Practices](https://graphql.org/learn/best-practices/)
- [Community Forum](https://community.apollographql.com/)
- [Awesome GraphQL](https://github.com/chentsulin/awesome-graphql)