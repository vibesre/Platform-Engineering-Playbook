# TypeScript

TypeScript is a typed superset of JavaScript that compiles to plain JavaScript, providing static type checking and enhanced developer experience for large-scale applications.

## 📚 Top Learning Resources

### 🎥 Video Courses

#### **TypeScript Tutorial for Beginners - Complete Course**
- **Channel**: Programming with Mosh
- **Link**: [YouTube - 5 hours](https://www.youtube.com/watch?v=d56mG7DezGs)
- **Why it's great**: Comprehensive tutorial covering TypeScript fundamentals to advanced features

#### **TypeScript Crash Course**
- **Channel**: Traversy Media
- **Link**: [YouTube - 1.5 hours](https://www.youtube.com/watch?v=BCg4U1FzODs)
- **Why it's great**: Quick start guide with practical examples and project setup

#### **TypeScript Course for Beginners**
- **Channel**: freeCodeCamp
- **Link**: [YouTube - 2 hours](https://www.youtube.com/watch?v=gp5H0Vw39yw)
- **Why it's great**: Hands-on course with real-world TypeScript applications

### 📖 Essential Documentation

#### **TypeScript Official Documentation**
- **Link**: [typescriptlang.org/docs](https://www.typescriptlang.org/docs/)
- **Why it's great**: Comprehensive official documentation with examples and best practices

#### **TypeScript Handbook**
- **Link**: [typescriptlang.org/docs/handbook/intro.html](https://www.typescriptlang.org/docs/handbook/intro.html)
- **Why it's great**: Complete guide covering all TypeScript concepts and features

#### **TypeScript Deep Dive**
- **Author**: Basarat Ali Syed
- **Link**: [basarat.gitbook.io/typescript/](https://basarat.gitbook.io/typescript/)
- **Why it's great**: Free comprehensive book covering advanced TypeScript patterns

### 📝 Must-Read Blogs & Articles

#### **TypeScript Blog**
- **Source**: Microsoft TypeScript Team
- **Link**: [devblogs.microsoft.com/typescript/](https://devblogs.microsoft.com/typescript/)
- **Why it's great**: Official updates and insights from TypeScript core team

#### **TypeScript Best Practices**
- **Source**: Matt Pocock
- **Link**: [github.com/total-typescript/beginners-typescript-tutorial](https://github.com/total-typescript/beginners-typescript-tutorial)
- **Why it's great**: Practical TypeScript patterns and advanced techniques

#### **TypeScript vs JavaScript**
- **Source**: Various
- **Link**: [typescriptlang.org/why-create-typescript](https://www.typescriptlang.org/why-create-typescript)
- **Why it's great**: Understanding the benefits and migration strategies

### 🎓 Structured Courses

#### **Understanding TypeScript**
- **Platform**: Udemy (Maximilian Schwarzmüller)
- **Link**: [udemy.com/course/understanding-typescript/](https://www.udemy.com/course/understanding-typescript/)
- **Cost**: Paid
- **Why it's great**: Comprehensive course with practical projects and advanced concepts

#### **Total TypeScript**
- **Platform**: Matt Pocock
- **Link**: [totaltypescript.com](https://www.totaltypescript.com/)
- **Cost**: Paid
- **Why it's great**: Advanced TypeScript workshops and practical exercises

### 🛠️ Tools & Platforms

#### **TypeScript Playground**
- **Link**: [typescriptlang.org/play](https://www.typescriptlang.org/play)
- **Why it's great**: Online TypeScript editor with instant compilation and sharing

#### **TS Node**
- **Link**: [typestrong.org/ts-node/](https://typestrong.org/ts-node/)
- **Why it's great**: Execute TypeScript directly in Node.js without compilation

#### **TypeScript ESLint**
- **Link**: [typescript-eslint.io](https://typescript-eslint.io/)
- **Why it's great**: ESLint and Prettier configurations for TypeScript projects

## Installation and Setup

### Node.js Project Setup
```bash
# Initialize new project
npm init -y

# Install TypeScript
npm install -D typescript @types/node ts-node nodemon

# Create tsconfig.json
npx tsc --init

# Install popular type definitions
npm install -D @types/express @types/jest @types/lodash
```

### tsconfig.json Configuration
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "moduleResolution": "node",
    "lib": ["ES2020", "DOM"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "removeComments": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "noImplicitReturns": true,
    "noImplicitThis": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "exactOptionalPropertyTypes": true,
    "paths": {
      "@/*": ["./src/*"],
      "@/types/*": ["./src/types/*"],
      "@/utils/*": ["./src/utils/*"]
    }
  },
  "include": [
    "src/**/*"
  ],
  "exclude": [
    "node_modules",
    "dist",
    "**/*.test.ts",
    "**/*.spec.ts"
  ]
}
```

### Package.json Scripts
```json
{
  "scripts": {
    "build": "tsc",
    "build:watch": "tsc --watch",
    "start": "node dist/index.js",
    "dev": "nodemon --exec ts-node src/index.ts",
    "test": "jest",
    "test:watch": "jest --watch",
    "lint": "eslint src/**/*.ts",
    "lint:fix": "eslint src/**/*.ts --fix",
    "type-check": "tsc --noEmit",
    "clean": "rm -rf dist"
  }
}
```

## Core TypeScript Concepts

### Type Definitions and Interfaces
```typescript
// Basic types
let age: number = 25;
let name: string = "John";
let isActive: boolean = true;
let items: string[] = ["item1", "item2"];
let coordinates: [number, number] = [10, 20];

// Interface definitions
interface User {
  readonly id: string;
  name: string;
  email: string;
  age?: number; // Optional property
  roles: string[];
  createdAt: Date;
}

interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  errors?: string[];
}

interface UserRepository {
  findById(id: string): Promise<User | null>;
  create(user: Omit<User, 'id' | 'createdAt'>): Promise<User>;
  update(id: string, updates: Partial<User>): Promise<User>;
  delete(id: string): Promise<void>;
}

// Extending interfaces
interface AdminUser extends User {
  permissions: string[];
  lastLogin?: Date;
}

// Union and intersection types
type Status = 'pending' | 'approved' | 'rejected';
type UserWithStatus = User & { status: Status };

// Generic types
type Repository<T> = {
  findById(id: string): Promise<T | null>;
  create(entity: Omit<T, 'id'>): Promise<T>;
  update(id: string, updates: Partial<T>): Promise<T>;
  delete(id: string): Promise<void>;
  findMany(filter?: Partial<T>): Promise<T[]>;
};

// Utility types
type CreateUserDto = Pick<User, 'name' | 'email' | 'roles'>;
type UpdateUserDto = Partial<Pick<User, 'name' | 'email' | 'age'>>;
type UserResponse = Omit<User, 'password'>;
```

### Advanced Type Patterns
```typescript
// Mapped types
type Optional<T> = {
  [P in keyof T]?: T[P];
};

type Required<T> = {
  [P in keyof T]-?: T[P];
};

// Conditional types
type ApiResult<T> = T extends string 
  ? { message: T } 
  : T extends object 
    ? { data: T } 
    : { value: T };

// Template literal types
type EventType = 'user' | 'order' | 'product';
type Action = 'create' | 'update' | 'delete';
type EventName = `${EventType}_${Action}`; // 'user_create' | 'user_update' | etc.

// Recursive types
type TreeNode<T> = {
  value: T;
  children?: TreeNode<T>[];
};

// Function overloads
function processData(data: string): string;
function processData(data: number): number;
function processData(data: boolean): boolean;
function processData(data: string | number | boolean): string | number | boolean {
  if (typeof data === 'string') {
    return data.toUpperCase();
  }
  if (typeof data === 'number') {
    return data * 2;
  }
  return !data;
}
```

## Express.js with TypeScript

### Server Setup
```typescript
// src/index.ts
import express, { Application, Request, Response, NextFunction } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import { userRoutes } from './routes/userRoutes';
import { errorHandler } from './middleware/errorHandler';
import { logger } from './utils/logger';

const app: Application = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Routes
app.use('/api/users', userRoutes);

// Health check
app.get('/health', (req: Request, res: Response) => {
  res.status(200).json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// Error handling
app.use(errorHandler);

// 404 handler
app.use('*', (req: Request, res: Response) => {
  res.status(404).json({
    success: false,
    message: `Route ${req.originalUrl} not found`
  });
});

app.listen(PORT, () => {
  logger.info(`Server running on port ${PORT}`);
});

export default app;
```

### Service Layer with Dependency Injection
```typescript
// src/services/UserService.ts
import { inject, injectable } from 'inversify';
import { User, CreateUserDto, UpdateUserDto } from '../types/User';
import { UserRepository } from '../repositories/UserRepository';
import { ValidationError, NotFoundError } from '../errors/CustomErrors';
import { logger } from '../utils/logger';

@injectable()
export class UserService {
  constructor(
    @inject('UserRepository') private userRepository: UserRepository
  ) {}

  async createUser(userData: CreateUserDto): Promise<User> {
    await this.validateCreateUser(userData);
    
    const user = await this.userRepository.create({
      ...userData,
      id: this.generateId(),
      createdAt: new Date()
    });

    logger.info(`User created: ${user.id}`);
    return this.sanitizeUser(user);
  }

  async getUserById(id: string): Promise<User> {
    if (!this.isValidId(id)) {
      throw new ValidationError('Invalid user ID format');
    }

    const user = await this.userRepository.findById(id);
    if (!user) {
      throw new NotFoundError(`User with ID ${id} not found`);
    }

    return this.sanitizeUser(user);
  }

  async updateUser(id: string, updates: UpdateUserDto): Promise<User> {
    await this.getUserById(id); // Ensures user exists
    await this.validateUpdateUser(updates);

    const updatedUser = await this.userRepository.update(id, {
      ...updates,
      updatedAt: new Date()
    });

    logger.info(`User updated: ${id}`);
    return this.sanitizeUser(updatedUser);
  }

  async deleteUser(id: string): Promise<void> {
    await this.getUserById(id); // Ensures user exists
    await this.userRepository.delete(id);
    logger.info(`User deleted: ${id}`);
  }

  async getUsersByRole(role: string): Promise<User[]> {
    const users = await this.userRepository.findMany({ roles: [role] });
    return users.map(user => this.sanitizeUser(user));
  }

  private async validateCreateUser(userData: CreateUserDto): Promise<void> {
    if (!userData.email || !this.isValidEmail(userData.email)) {
      throw new ValidationError('Valid email is required');
    }

    const existingUser = await this.userRepository.findByEmail(userData.email);
    if (existingUser) {
      throw new ValidationError('Email already exists');
    }
  }

  private async validateUpdateUser(updates: UpdateUserDto): Promise<void> {
    if (updates.email && !this.isValidEmail(updates.email)) {
      throw new ValidationError('Invalid email format');
    }
  }

  private sanitizeUser(user: User): User {
    const { password, ...sanitized } = user as any;
    return sanitized;
  }

  private isValidId(id: string): boolean {
    return /^[0-9a-fA-F]{24}$/.test(id);
  }

  private isValidEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  private generateId(): string {
    return Math.random().toString(36).substr(2, 9);
  }
}
```

### Controllers with Type Safety
```typescript
// src/controllers/UserController.ts
import { Request, Response, NextFunction } from 'express';
import { inject, injectable } from 'inversify';
import { UserService } from '../services/UserService';
import { CreateUserDto, UpdateUserDto } from '../types/User';
import { ApiResponse } from '../types/ApiResponse';
import { logger } from '../utils/logger';

interface TypedRequest<T> extends Request {
  body: T;
}

interface UserParamsRequest extends Request {
  params: {
    id: string;
  };
}

@injectable()
export class UserController {
  constructor(
    @inject('UserService') private userService: UserService
  ) {}

  createUser = async (
    req: TypedRequest<CreateUserDto>,
    res: Response<ApiResponse<User>>,
    next: NextFunction
  ): Promise<void> => {
    try {
      const user = await this.userService.createUser(req.body);
      
      res.status(201).json({
        success: true,
        data: user,
        message: 'User created successfully'
      });
    } catch (error) {
      next(error);
    }
  };

  getUserById = async (
    req: UserParamsRequest,
    res: Response<ApiResponse<User>>,
    next: NextFunction
  ): Promise<void> => {
    try {
      const user = await this.userService.getUserById(req.params.id);
      
      res.json({
        success: true,
        data: user
      });
    } catch (error) {
      next(error);
    }
  };

  updateUser = async (
    req: TypedRequest<UpdateUserDto> & UserParamsRequest,
    res: Response<ApiResponse<User>>,
    next: NextFunction
  ): Promise<void> => {
    try {
      const user = await this.userService.updateUser(req.params.id, req.body);
      
      res.json({
        success: true,
        data: user,
        message: 'User updated successfully'
      });
    } catch (error) {
      next(error);
    }
  };

  deleteUser = async (
    req: UserParamsRequest,
    res: Response<ApiResponse<null>>,
    next: NextFunction
  ): Promise<void> => {
    try {
      await this.userService.deleteUser(req.params.id);
      
      res.status(204).json({
        success: true,
        data: null,
        message: 'User deleted successfully'
      });
    } catch (error) {
      next(error);
    }
  };

  getUsersByRole = async (
    req: Request<{}, {}, {}, { role: string }>,
    res: Response<ApiResponse<User[]>>,
    next: NextFunction
  ): Promise<void> => {
    try {
      const { role } = req.query;
      const users = await this.userService.getUsersByRole(role);
      
      res.json({
        success: true,
        data: users
      });
    } catch (error) {
      next(error);
    }
  };
}
```

## Database Integration with TypeScript

### Prisma ORM Setup
```typescript
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String
  age       Int?
  roles     String[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  
  orders    Order[]
  
  @@map("users")
}

model Order {
  id        String   @id @default(cuid())
  userId    String
  amount    Decimal  @db.Decimal(10, 2)
  status    OrderStatus @default(PENDING)
  createdAt DateTime @default(now())
  
  user      User     @relation(fields: [userId], references: [id])
  
  @@map("orders")
}

enum OrderStatus {
  PENDING
  PROCESSING
  SHIPPED
  DELIVERED
  CANCELLED
}
```

### Repository Pattern with Prisma
```typescript
// src/repositories/PrismaUserRepository.ts
import { PrismaClient, User as PrismaUser } from '@prisma/client';
import { injectable } from 'inversify';
import { UserRepository } from '../interfaces/UserRepository';
import { User, CreateUserDto, UpdateUserDto } from '../types/User';
import { logger } from '../utils/logger';

@injectable()
export class PrismaUserRepository implements UserRepository {
  constructor(private prisma: PrismaClient) {}

  async findById(id: string): Promise<User | null> {
    try {
      const user = await this.prisma.user.findUnique({
        where: { id },
        include: {
          orders: {
            orderBy: { createdAt: 'desc' },
            take: 10
          }
        }
      });

      return user ? this.mapToUser(user) : null;
    } catch (error) {
      logger.error(`Error finding user by ID ${id}:`, error);
      throw error;
    }
  }

  async findByEmail(email: string): Promise<User | null> {
    try {
      const user = await this.prisma.user.findUnique({
        where: { email }
      });

      return user ? this.mapToUser(user) : null;
    } catch (error) {
      logger.error(`Error finding user by email ${email}:`, error);
      throw error;
    }
  }

  async create(userData: CreateUserDto): Promise<User> {
    try {
      const user = await this.prisma.user.create({
        data: userData,
        include: {
          orders: true
        }
      });

      return this.mapToUser(user);
    } catch (error) {
      logger.error('Error creating user:', error);
      throw error;
    }
  }

  async update(id: string, updates: UpdateUserDto): Promise<User> {
    try {
      const user = await this.prisma.user.update({
        where: { id },
        data: updates,
        include: {
          orders: true
        }
      });

      return this.mapToUser(user);
    } catch (error) {
      logger.error(`Error updating user ${id}:`, error);
      throw error;
    }
  }

  async delete(id: string): Promise<void> {
    try {
      await this.prisma.user.delete({
        where: { id }
      });
    } catch (error) {
      logger.error(`Error deleting user ${id}:`, error);
      throw error;
    }
  }

  async findMany(filter?: Partial<User>): Promise<User[]> {
    try {
      const users = await this.prisma.user.findMany({
        where: filter,
        include: {
          orders: {
            orderBy: { createdAt: 'desc' },
            take: 5
          }
        },
        orderBy: { createdAt: 'desc' }
      });

      return users.map(user => this.mapToUser(user));
    } catch (error) {
      logger.error('Error finding users:', error);
      throw error;
    }
  }

  private mapToUser(prismaUser: PrismaUser & { orders?: any[] }): User {
    return {
      id: prismaUser.id,
      email: prismaUser.email,
      name: prismaUser.name,
      age: prismaUser.age || undefined,
      roles: prismaUser.roles,
      createdAt: prismaUser.createdAt,
      updatedAt: prismaUser.updatedAt,
      orders: prismaUser.orders || []
    };
  }
}
```

## Testing with TypeScript

### Jest Configuration
```typescript
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  testMatch: ['**/__tests__/**/*.ts', '**/?(*.)+(spec|test).ts'],
  transform: {
    '^.+\\.ts$': 'ts-jest',
  },
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
    '!src/index.ts',
    '!src/**/__tests__/**',
  ],
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  setupFilesAfterEnv: ['<rootDir>/src/__tests__/setup.ts'],
  testTimeout: 10000,
  clearMocks: true,
  restoreMocks: true,
};
```

### Unit Testing with Mocks
```typescript
// src/__tests__/services/UserService.test.ts
import { UserService } from '../../services/UserService';
import { UserRepository } from '../../interfaces/UserRepository';
import { User, CreateUserDto } from '../../types/User';
import { ValidationError, NotFoundError } from '../../errors/CustomErrors';

describe('UserService', () => {
  let userService: UserService;
  let mockUserRepository: jest.Mocked<UserRepository>;

  beforeEach(() => {
    mockUserRepository = {
      findById: jest.fn(),
      findByEmail: jest.fn(),
      create: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
      findMany: jest.fn(),
    };

    userService = new UserService(mockUserRepository);
  });

  describe('createUser', () => {
    const validUserData: CreateUserDto = {
      name: 'John Doe',
      email: 'john@example.com',
      roles: ['user']
    };

    it('should create a user successfully', async () => {
      const expectedUser: User = {
        id: '123',
        ...validUserData,
        createdAt: new Date(),
        updatedAt: new Date()
      };

      mockUserRepository.findByEmail.mockResolvedValue(null);
      mockUserRepository.create.mockResolvedValue(expectedUser);

      const result = await userService.createUser(validUserData);

      expect(mockUserRepository.findByEmail).toHaveBeenCalledWith(validUserData.email);
      expect(mockUserRepository.create).toHaveBeenCalledWith(
        expect.objectContaining({
          name: validUserData.name,
          email: validUserData.email,
          roles: validUserData.roles
        })
      );
      expect(result).toEqual(expectedUser);
    });

    it('should throw ValidationError if email is invalid', async () => {
      const invalidUserData = {
        ...validUserData,
        email: 'invalid-email'
      };

      await expect(userService.createUser(invalidUserData))
        .rejects
        .toThrow(ValidationError);
    });

    it('should throw ValidationError if email already exists', async () => {
      const existingUser: User = {
        id: '456',
        ...validUserData,
        createdAt: new Date(),
        updatedAt: new Date()
      };

      mockUserRepository.findByEmail.mockResolvedValue(existingUser);

      await expect(userService.createUser(validUserData))
        .rejects
        .toThrow(ValidationError);
    });
  });

  describe('getUserById', () => {
    it('should return user when found', async () => {
      const user: User = {
        id: '123',
        name: 'John Doe',
        email: 'john@example.com',
        roles: ['user'],
        createdAt: new Date(),
        updatedAt: new Date()
      };

      mockUserRepository.findById.mockResolvedValue(user);

      const result = await userService.getUserById('123');

      expect(mockUserRepository.findById).toHaveBeenCalledWith('123');
      expect(result).toEqual(user);
    });

    it('should throw NotFoundError when user not found', async () => {
      mockUserRepository.findById.mockResolvedValue(null);

      await expect(userService.getUserById('nonexistent'))
        .rejects
        .toThrow(NotFoundError);
    });

    it('should throw ValidationError for invalid ID format', async () => {
      await expect(userService.getUserById('invalid-id'))
        .rejects
        .toThrow(ValidationError);
    });
  });
});
```

### Integration Testing
```typescript
// src/__tests__/integration/userRoutes.test.ts
import request from 'supertest';
import app from '../../index';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

describe('User Routes Integration', () => {
  beforeAll(async () => {
    // Setup test database
    await prisma.$connect();
  });

  afterAll(async () => {
    // Cleanup
    await prisma.user.deleteMany();
    await prisma.$disconnect();
  });

  beforeEach(async () => {
    // Clean database before each test
    await prisma.user.deleteMany();
  });

  describe('POST /api/users', () => {
    it('should create a new user', async () => {
      const userData = {
        name: 'John Doe',
        email: 'john@example.com',
        roles: ['user']
      };

      const response = await request(app)
        .post('/api/users')
        .send(userData)
        .expect(201);

      expect(response.body).toMatchObject({
        success: true,
        data: expect.objectContaining({
          id: expect.any(String),
          name: userData.name,
          email: userData.email,
          roles: userData.roles
        }),
        message: 'User created successfully'
      });
    });

    it('should return 400 for invalid email', async () => {
      const userData = {
        name: 'John Doe',
        email: 'invalid-email',
        roles: ['user']
      };

      const response = await request(app)
        .post('/api/users')
        .send(userData)
        .expect(400);

      expect(response.body).toMatchObject({
        success: false,
        message: expect.stringContaining('email')
      });
    });
  });

  describe('GET /api/users/:id', () => {
    it('should return user by ID', async () => {
      // Create a user first
      const user = await prisma.user.create({
        data: {
          name: 'John Doe',
          email: 'john@example.com',
          roles: ['user']
        }
      });

      const response = await request(app)
        .get(`/api/users/${user.id}`)
        .expect(200);

      expect(response.body).toMatchObject({
        success: true,
        data: expect.objectContaining({
          id: user.id,
          name: user.name,
          email: user.email
        })
      });
    });

    it('should return 404 for non-existent user', async () => {
      const response = await request(app)
        .get('/api/users/nonexistent')
        .expect(404);

      expect(response.body).toMatchObject({
        success: false,
        message: expect.stringContaining('not found')
      });
    });
  });
});
```

## Build and Deployment

### Docker Configuration
```dockerfile
# Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY tsconfig.json ./

# Install dependencies
RUN npm ci --only=production && npm cache clean --force

# Copy source code
COPY src ./src

# Build TypeScript
RUN npm run build

# Production stage
FROM node:18-alpine AS production

WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Copy package files
COPY package*.json ./

# Install production dependencies only
RUN npm ci --only=production && npm cache clean --force

# Copy built application
COPY --from=builder /app/dist ./dist
COPY --chown=nodejs:nodejs . .

USER nodejs

EXPOSE 3000

CMD ["node", "dist/index.js"]
```

### GitHub Actions CI/CD
```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Type checking
        run: npm run type-check
      
      - name: Lint
        run: npm run lint
      
      - name: Run tests
        run: npm test
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
      
      - name: Build
        run: npm run build
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/lcov.info

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Build and push Docker image
        env:
          DOCKER_BUILDKIT: 1
        run: |
          docker build -t my-app:${{ github.sha }} .
          docker push my-app:${{ github.sha }}
```

## Best Practices

### Code Organization
```typescript
// Project structure
src/
├── controllers/          # Request/response handling
├── services/            # Business logic
├── repositories/        # Data access layer
├── models/             # Domain models
├── types/              # Type definitions
├── interfaces/         # Interface definitions
├── middleware/         # Express middleware
├── utils/              # Utility functions
├── config/             # Configuration
├── errors/             # Custom error classes
└── __tests__/          # Test files

// Barrel exports for clean imports
// src/types/index.ts
export * from './User';
export * from './ApiResponse';
export * from './Database';

// Usage
import { User, ApiResponse, CreateUserDto } from '@/types';
```

### Error Handling
```typescript
// src/errors/CustomErrors.ts
export abstract class AppError extends Error {
  abstract statusCode: number;
  abstract isOperational: boolean;

  constructor(message: string, public isOperational: boolean = true) {
    super(message);
    Object.setPrototypeOf(this, AppError.prototype);
  }
}

export class ValidationError extends AppError {
  statusCode = 400;
  isOperational = true;

  constructor(message: string) {
    super(message);
    Object.setPrototypeOf(this, ValidationError.prototype);
  }
}

export class NotFoundError extends AppError {
  statusCode = 404;
  isOperational = true;

  constructor(message: string) {
    super(message);
    Object.setPrototypeOf(this, NotFoundError.prototype);
  }
}

// src/middleware/errorHandler.ts
import { Request, Response, NextFunction } from 'express';
import { AppError } from '../errors/CustomErrors';
import { logger } from '../utils/logger';

export const errorHandler = (
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  let statusCode = 500;
  let message = 'Internal server error';

  if (error instanceof AppError) {
    statusCode = error.statusCode;
    message = error.message;
  }

  logger.error('Error:', {
    message: error.message,
    stack: error.stack,
    url: req.url,
    method: req.method
  });

  res.status(statusCode).json({
    success: false,
    message,
    ...(process.env.NODE_ENV === 'development' && { stack: error.stack })
  });
};
```

## Resources

- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [TypeScript ESLint Rules](https://typescript-eslint.io/rules/)
- [Express with TypeScript](https://github.com/Microsoft/TypeScript-Node-Starter)
- [Prisma TypeScript Guide](https://www.prisma.io/docs/concepts/overview/what-is-prisma)
- [Jest TypeScript Setup](https://jestjs.io/docs/getting-started#using-typescript)
- [TypeScript Best Practices](https://github.com/labs42io/clean-code-typescript)
- [Utility Types Reference](https://www.typescriptlang.org/docs/handbook/utility-types.html)
- [Advanced TypeScript Patterns](https://github.com/type-challenges/type-challenges)
- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/)
- [Effective TypeScript Book](https://effectivetypescript.com/)