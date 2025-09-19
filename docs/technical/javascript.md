# JavaScript

## Overview

JavaScript is a versatile programming language essential for modern web development and increasingly important for platform engineering through Node.js. It's used for building APIs, automation scripts, monitoring dashboards, and infrastructure tooling.

## Key Features

- **Full-Stack Development**: Frontend and backend with Node.js
- **Event-Driven**: Excellent for asynchronous operations and APIs
- **Rich Ecosystem**: npm package manager with vast library selection
- **JSON Native**: Perfect for API development and configuration
- **Cloud Integration**: Strong support for serverless and cloud platforms

## Common Use Cases

### API Development with Express
```javascript
const express = require('express');
const app = express();

app.use(express.json());

app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        uptime: process.uptime()
    });
});

app.get('/metrics', (req, res) => {
    res.json({
        memory: process.memoryUsage(),
        cpu: process.cpuUsage()
    });
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});
```

### Infrastructure Automation
```javascript
const AWS = require('aws-sdk');
const ec2 = new AWS.EC2();

async function listInstances() {
    try {
        const data = await ec2.describeInstances().promise();
        data.Reservations.forEach(reservation => {
            reservation.Instances.forEach(instance => {
                console.log(`Instance: ${instance.InstanceId} - ${instance.State.Name}`);
            });
        });
    } catch (error) {
        console.error('Error:', error);
    }
}

listInstances();
```

### Monitoring Dashboards
```javascript
// React component for system metrics
import React, { useState, useEffect } from 'react';

function MetricsDashboard() {
    const [metrics, setMetrics] = useState(null);

    useEffect(() => {
        const fetchMetrics = async () => {
            const response = await fetch('/api/metrics');
            const data = await response.json();
            setMetrics(data);
        };

        fetchMetrics();
        const interval = setInterval(fetchMetrics, 5000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div>
            <h2>System Metrics</h2>
            {metrics && (
                <div>
                    <p>CPU Usage: {metrics.cpu}%</p>
                    <p>Memory Usage: {metrics.memory}%</p>
                </div>
            )}
        </div>
    );
}
```

## Essential Libraries for Platform Engineering

- **express** - Web application framework
- **axios** - HTTP client
- **lodash** - Utility library
- **moment** - Date manipulation
- **pm2** - Process manager
- **winston** - Logging library
- **jest** - Testing framework

## Runtime Environments

- **Node.js** - Server-side JavaScript runtime
- **Deno** - Secure JavaScript/TypeScript runtime
- **Bun** - Fast JavaScript runtime and package manager

## Best Practices

- Use `const` and `let` instead of `var`
- Handle promises with async/await
- Implement proper error handling
- Use environment variables for configuration
- Write unit tests for critical functions
- Follow ESLint rules for consistent code style

## Great Resources

- [MDN JavaScript Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide) - Comprehensive JavaScript reference
- [Node.js Documentation](https://nodejs.org/docs/) - Official Node.js guide and API reference
- [Express.js Guide](https://expressjs.com/en/guide/routing.html) - Web framework documentation
- [JavaScript.info](https://javascript.info/) - Modern JavaScript tutorial
- [npm Registry](https://www.npmjs.com/) - Package manager and library discovery
- [Awesome Node.js](https://github.com/sindresorhus/awesome-nodejs) - Curated Node.js resources
- [You Don't Know JS](https://github.com/getify/You-Dont-Know-JS) - Deep dive into JavaScript