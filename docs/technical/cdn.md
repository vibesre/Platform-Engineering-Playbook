# Content Delivery Networks (CDN)

## Overview

Content Delivery Networks distribute content across geographically dispersed servers to reduce latency, improve performance, and enhance reliability for end users worldwide.

## Core Technologies

### CloudFlare

Global CDN with integrated security features and edge computing capabilities.

#### Key Features
- 275+ global PoPs
- DDoS protection
- Web Application Firewall (WAF)
- Workers edge computing
- DNS management
- SSL/TLS termination

#### Configuration Example

**CloudFlare Configuration (wrangler.toml)**:
```toml
name = "my-app"
type = "webpack"
account_id = "your-account-id"
workers_dev = true
route = "example.com/*"
zone_id = "your-zone-id"

[env.production]
vars = { ENVIRONMENT = "production" }
kv_namespaces = [
  { binding = "CACHE", id = "namespace-id" }
]

[[r2_buckets]]
binding = "ASSETS"
bucket_name = "my-assets-bucket"

[site]
bucket = "./dist"
entry-point = "workers-site"

[build]
command = "npm run build"
```

**Page Rules Configuration**:
```json
{
  "targets": [
    {
      "target": "url",
      "constraint": {
        "operator": "matches",
        "value": "*.example.com/api/*"
      }
    }
  ],
  "actions": [
    {
      "id": "cache_level",
      "value": "aggressive"
    },
    {
      "id": "edge_cache_ttl",
      "value": 7200
    },
    {
      "id": "browser_cache_ttl",
      "value": 3600
    }
  ],
  "priority": 1,
  "status": "active"
}
```

**CloudFlare Workers Example**:
```javascript
// Edge computing with CloudFlare Workers
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const cache = caches.default
  const cacheKey = new Request(request.url, request)
  
  // Check cache
  let response = await cache.match(cacheKey)
  
  if (!response) {
    // Cache miss - fetch from origin
    response = await fetch(request)
    
    // Cache successful responses
    if (response.status === 200) {
      const headers = new Headers(response.headers)
      headers.set('Cache-Control', 'max-age=3600')
      
      response = new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers: headers
      })
      
      event.waitUntil(cache.put(cacheKey, response.clone()))
    }
  }
  
  return response
}

// Custom routing logic
async function routeRequest(request) {
  const url = new URL(request.url)
  
  // Route based on path
  if (url.pathname.startsWith('/api/')) {
    return fetch(`https://api.backend.com${url.pathname}`)
  } else if (url.pathname.startsWith('/static/')) {
    return fetch(`https://cdn.example.com${url.pathname}`)
  }
  
  return fetch(request)
}
```

### Fastly

Real-time CDN with edge computing and instant purging capabilities.

#### Key Features
- Instant purging
- Real-time analytics
- Edge computing with VCL
- Image optimization
- Video streaming
- Shield origin protection

#### Configuration Example

**Fastly VCL Configuration**:
```vcl
# Fastly VCL configuration
sub vcl_recv {
  # Normalize the host header
  set req.http.Host = regsub(req.http.Host, ":.*", "");
  
  # Remove tracking parameters
  if (req.url ~ "(\?|&)(utm_source|utm_medium|utm_campaign|utm_content|gclid|fbclid)=") {
    set req.url = regsuball(req.url, "(utm_source|utm_medium|utm_campaign|utm_content|gclid|fbclid)=[^&]+&?", "");
    set req.url = regsub(req.url, "(\?|&)$", "");
  }
  
  # Force SSL redirect
  if (!req.http.Fastly-SSL) {
    error 801 "Redirect to SSL";
  }
  
  # Add device detection
  if (req.http.User-Agent ~ "(?i)(mobile|android|iphone)") {
    set req.http.X-Device = "mobile";
  } else {
    set req.http.X-Device = "desktop";
  }
  
  # Cache static assets
  if (req.url ~ "\.(jpg|jpeg|gif|png|ico|css|js|woff|woff2|ttf|eot|svg)(\?|$)") {
    unset req.http.Cookie;
    return(lookup);
  }
  
  # Pass through for authenticated users
  if (req.http.Cookie ~ "session=") {
    return(pass);
  }
  
  return(lookup);
}

sub vcl_fetch {
  # Set cache TTL based on content type
  if (beresp.http.content-type ~ "^(text/css|application/javascript)") {
    set beresp.ttl = 7d;
    set beresp.http.Cache-Control = "public, max-age=604800";
  } else if (beresp.http.content-type ~ "^image/") {
    set beresp.ttl = 30d;
    set beresp.http.Cache-Control = "public, max-age=2592000";
  }
  
  # Enable Streaming Miss
  if (req.url ~ "\.mp4$") {
    set beresp.do_stream = true;
  }
  
  # Add security headers
  set beresp.http.X-Frame-Options = "SAMEORIGIN";
  set beresp.http.X-Content-Type-Options = "nosniff";
  set beresp.http.X-XSS-Protection = "1; mode=block";
  
  # Enable gzip compression
  if (beresp.http.content-type ~ "^(text/|application/javascript|application/json)") {
    set beresp.do_gzip = true;
  }
  
  return(deliver);
}

sub vcl_error {
  # SSL redirect
  if (obj.status == 801) {
    set obj.status = 301;
    set obj.http.Location = "https://" + req.http.host + req.url;
    return(deliver);
  }
  
  # Custom error pages
  if (obj.status == 503 && req.restarts < 3) {
    return(restart);
  }
  
  synthetic {"
    <!DOCTYPE html>
    <html>
    <head>
      <title>Error "} + obj.status + {"</title>
    </head>
    <body>
      <h1>Error "} + obj.status + {"</h1>
      <p>"} + obj.response + {"</p>
    </body>
    </html>
  "};
  return(deliver);
}
```

**Fastly Compute@Edge (Rust)**:
```rust
use fastly::{Error, Request, Response};

#[fastly::main]
fn main(req: Request) -> Result<Response, Error> {
    // Pattern match on the request method
    match req.get_method() {
        &Method::GET => handle_get(req),
        &Method::POST => handle_post(req),
        _ => Ok(Response::from_status(StatusCode::METHOD_NOT_ALLOWED)),
    }
}

fn handle_get(req: Request) -> Result<Response, Error> {
    let path = req.get_path();
    
    // Check cache
    let cache_key = format!("cache:{}", path);
    if let Some(cached) = cache::core::lookup(cache_key.parse()?).execute()? {
        return Ok(cached);
    }
    
    // Fetch from origin
    let backend = backends::get("origin")?;
    let mut origin_response = req.clone_without_body().send(backend)?;
    
    // Apply transformations
    if path.ends_with(".jpg") || path.ends_with(".png") {
        origin_response = optimize_image(origin_response)?;
    }
    
    // Cache the response
    if origin_response.get_status().is_success() {
        let mut cache_response = origin_response.clone_with_body();
        cache_response.set_header("Cache-Control", "public, max-age=3600");
        cache::core::insert(cache_key.parse()?, cache_response.clone())
            .execute()?;
    }
    
    Ok(origin_response)
}

fn optimize_image(mut response: Response) -> Result<Response, Error> {
    // Image optimization logic
    response.set_header("X-Image-Optimized", "true");
    Ok(response)
}
```

### Akamai

Enterprise-grade CDN with advanced security and media delivery capabilities.

#### Key Features
- 340,000+ edge servers
- Advanced caching algorithms
- Bot Manager
- Adaptive media delivery
- EdgeWorkers computing
- Ion performance optimization

#### Configuration Example

**Akamai Property Configuration (JSON)**:
```json
{
  "rules": {
    "name": "default",
    "children": [
      {
        "name": "Performance",
        "children": [
          {
            "name": "Compressible Objects",
            "criteria": [
              {
                "name": "contentType",
                "options": {
                  "matchOperator": "IS_ONE_OF",
                  "values": [
                    "text/*",
                    "application/javascript",
                    "application/json",
                    "application/xml"
                  ]
                }
              }
            ],
            "behaviors": [
              {
                "name": "gzipResponse",
                "options": {
                  "behavior": "ALWAYS"
                }
              }
            ]
          }
        ]
      },
      {
        "name": "Offload",
        "children": [
          {
            "name": "Static Content",
            "criteria": [
              {
                "name": "fileExtension",
                "options": {
                  "matchOperator": "IS_ONE_OF",
                  "values": [
                    "jpg", "jpeg", "png", "gif", "webp",
                    "css", "js", "woff", "woff2", "ttf"
                  ]
                }
              }
            ],
            "behaviors": [
              {
                "name": "caching",
                "options": {
                  "behavior": "MAX_AGE",
                  "ttl": "7d"
                }
              },
              {
                "name": "prefreshCache",
                "options": {
                  "enabled": true,
                  "prefreshval": 90
                }
              }
            ]
          }
        ]
      },
      {
        "name": "Security",
        "behaviors": [
          {
            "name": "allHttpInCacheHierarchy",
            "options": {
              "enabled": true
            }
          },
          {
            "name": "webApplicationFirewall",
            "options": {
              "firewallConfiguration": {
                "configId": 12345,
                "version": "LATEST"
              }
            }
          }
        ]
      }
    ],
    "behaviors": [
      {
        "name": "origin",
        "options": {
          "originType": "CUSTOMER",
          "hostname": "origin.example.com",
          "forwardHostHeader": "REQUEST_HOST_HEADER",
          "cacheKeyHostname": "ORIGIN_HOSTNAME"
        }
      },
      {
        "name": "cpCode",
        "options": {
          "value": {
            "id": 123456
          }
        }
      }
    ]
  }
}
```

**EdgeWorkers JavaScript Example**:
```javascript
// Akamai EdgeWorkers
import { httpRequest } from 'http-request';
import { createResponse } from 'create-response';
import { logger } from 'log';

export async function onClientRequest(request) {
  // Add geo-location header
  request.addHeader('X-Akamai-Geo-Country', request.getVariable('PMUSER_COUNTRY'));
  
  // A/B testing logic
  const testGroup = hashUserToGroup(request.getHeader('Cookie')[0]);
  request.addHeader('X-Test-Group', testGroup);
  
  // Custom routing based on geo
  const country = request.getVariable('PMUSER_COUNTRY');
  if (country === 'CN') {
    request.route('china-origin');
  }
}

export async function onOriginResponse(request, response) {
  // Modify cache key based on device type
  const userAgent = request.getHeader('User-Agent')[0];
  const deviceType = detectDevice(userAgent);
  
  response.addHeader('Vary', 'User-Agent');
  response.addHeader('X-Device-Type', deviceType);
  
  // Dynamic cache TTL
  if (response.status === 200) {
    const contentType = response.getHeader('Content-Type')[0];
    if (contentType && contentType.includes('application/json')) {
      response.setHeader('Cache-Control', 'max-age=300');
    }
  }
}

export async function responseProvider(request) {
  // Edge-side includes
  const template = await getTemplate();
  const data = await fetchData(request);
  
  const html = renderTemplate(template, data);
  
  return createResponse(
    200,
    { 'Content-Type': ['text/html'] },
    html
  );
}

function hashUserToGroup(cookie) {
  // Simple A/B test bucketing
  const userId = extractUserId(cookie);
  const hash = simpleHash(userId);
  return hash % 100 < 50 ? 'A' : 'B';
}

function detectDevice(userAgent) {
  if (/mobile/i.test(userAgent)) return 'mobile';
  if (/tablet/i.test(userAgent)) return 'tablet';
  return 'desktop';
}
```

## Best Practices

### Caching Strategies

1. **Cache Headers Configuration**
   ```nginx
   # Static assets - long cache
   location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff|woff2)$ {
     expires 1y;
     add_header Cache-Control "public, immutable";
     add_header Vary "Accept-Encoding";
   }
   
   # HTML - short cache with revalidation
   location ~* \.(html)$ {
     expires 1h;
     add_header Cache-Control "public, must-revalidate";
   }
   
   # API responses - no cache
   location /api/ {
     expires -1;
     add_header Cache-Control "no-store, no-cache, must-revalidate";
   }
   ```

2. **Cache Invalidation Patterns**
   ```python
   # CloudFlare purge example
   import requests
   
   def purge_cloudflare_cache(zone_id, urls):
       headers = {
           'X-Auth-Email': 'admin@example.com',
           'X-Auth-Key': 'api-key',
           'Content-Type': 'application/json'
       }
       
       data = {
           'files': urls
       }
       
       response = requests.post(
           f'https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache',
           headers=headers,
           json=data
       )
       
       return response.json()
   
   # Fastly purge example
   def purge_fastly_cache(service_id, key):
       headers = {
           'Fastly-Key': 'api-key',
           'Accept': 'application/json'
       }
       
       response = requests.post(
           f'https://api.fastly.com/service/{service_id}/purge/{key}',
           headers=headers
       )
       
       return response.json()
   ```

### Performance Optimization

1. **Origin Optimization**
   ```yaml
   # Origin shield configuration
   cloudflare:
     tiered_caching:
       enabled: true
       topology: "smart"
   
   fastly:
     shield:
       enabled: true
       pop: "IAD"
   
   akamai:
     sure_route:
       enabled: true
       test_object: "/akamai/sureroute-test"
   ```

2. **Compression Settings**
   ```json
   {
     "compression": {
       "algorithms": ["gzip", "brotli"],
       "types": [
         "text/html",
         "text/css",
         "text/javascript",
         "application/javascript",
         "application/json",
         "application/xml",
         "image/svg+xml"
       ],
       "min_size": 1024,
       "level": 6
     }
   }
   ```

### Security Configuration

1. **DDoS Protection**
   ```yaml
   cloudflare:
     ddos_protection:
       sensitivity_level: "high"
       rule_sets:
         - "http_ddos_managed"
         - "http_ratelimit_default"
   
   fastly:
     rate_limiting:
       window: 60
       threshold: 100
       action: "block"
       duration: 600
   ```

2. **WAF Rules**
   ```json
   {
     "waf_rules": [
       {
         "id": "block-sql-injection",
         "expression": "http.request.uri.query contains \"union select\"",
         "action": "block"
       },
       {
         "id": "block-xss",
         "expression": "http.request.uri contains \"<script\"",
         "action": "challenge"
       },
       {
         "id": "geo-blocking",
         "expression": "ip.geoip.country in {\"CN\" \"RU\"}",
         "action": "block"
       }
     ]
   }
   ```

## Common Patterns

### Multi-CDN Strategy

```yaml
# Traffic distribution configuration
traffic_split:
  providers:
    - name: cloudflare
      weight: 60
      regions: ["NA", "EU"]
    - name: fastly
      weight: 30
      regions: ["APAC"]
    - name: akamai
      weight: 10
      regions: ["ALL"]
  
  failover:
    enabled: true
    health_check_interval: 30
    failure_threshold: 3
```

### Edge Computing Patterns

1. **A/B Testing at Edge**
   ```javascript
   // CloudFlare Workers A/B testing
   const EXPERIMENTS = {
     'homepage-redesign': {
       enabled: true,
       traffic: 0.5,
       variants: ['control', 'variant-a']
     }
   };
   
   function getVariant(userId, experiment) {
     const hash = cyrb53(userId + experiment.name);
     const bucket = hash % 100;
     
     if (bucket < experiment.traffic * 100) {
       return experiment.variants[1];
     }
     return experiment.variants[0];
   }
   ```

2. **Dynamic Content Assembly**
   ```rust
   // Fastly Compute@Edge ESI implementation
   use fastly::{Request, Response, Error};
   use regex::Regex;
   
   fn process_esi_tags(content: String, req: &Request) -> Result<String, Error> {
       let esi_include = Regex::new(r#"<esi:include src="([^"]+)"/>"#)?;
       let mut result = content;
       
       for cap in esi_include.captures_iter(&content) {
           let url = &cap[1];
           let fragment = fetch_fragment(url, req)?;
           result = result.replace(&cap[0], &fragment);
       }
       
       Ok(result)
   }
   ```

## Monitoring and Analytics

### Real User Monitoring (RUM)

```javascript
// CDN RUM implementation
(function() {
  const rumData = {
    navigationStart: performance.timing.navigationStart,
    domContentLoaded: performance.timing.domContentLoadedEventEnd,
    loadComplete: performance.timing.loadEventEnd,
    cdn: 'cloudflare',
    pop: navigator.cdn?.pop || 'unknown',
    cacheStatus: navigator.cdn?.cacheStatus || 'unknown'
  };
  
  // Send to analytics endpoint
  navigator.sendBeacon('/analytics/rum', JSON.stringify(rumData));
})();
```

### CDN Performance Metrics

```yaml
metrics:
  cache_hit_ratio:
    target: 90%
    calculation: "(cache_hits / (cache_hits + cache_misses)) * 100"
  
  origin_response_time:
    target: < 200ms
    percentiles: [p50, p90, p99]
  
  edge_response_time:
    target: < 50ms
    percentiles: [p50, p90, p99]
  
  bandwidth_savings:
    calculation: "(1 - (origin_bandwidth / total_bandwidth)) * 100"
```

## Migration Strategies

### CDN Migration Checklist

```markdown
## Pre-Migration
- [ ] Audit current CDN configuration
- [ ] Document all custom rules and behaviors
- [ ] Inventory all cached content
- [ ] Map features to new CDN capabilities
- [ ] Plan DNS migration strategy

## Migration Steps
- [ ] Configure new CDN in staging
- [ ] Implement custom rules and behaviors
- [ ] Test with production-like traffic
- [ ] Set up monitoring and alerting
- [ ] Implement gradual traffic migration
- [ ] Monitor performance metrics
- [ ] Complete DNS cutover
- [ ] Verify cache warming

## Post-Migration
- [ ] Monitor error rates
- [ ] Verify cache hit ratios
- [ ] Check origin load
- [ ] Validate security rules
- [ ] Update documentation
```

### Traffic Migration Pattern

```python
# Gradual CDN migration using weighted DNS
import boto3

def update_route53_weights(zone_id, domain, old_cdn, new_cdn, new_weight):
    """
    Gradually shift traffic from old CDN to new CDN
    """
    client = boto3.client('route53')
    
    old_weight = 100 - new_weight
    
    changes = [
        {
            'Action': 'UPSERT',
            'ResourceRecordSet': {
                'Name': domain,
                'Type': 'CNAME',
                'SetIdentifier': 'old-cdn',
                'Weight': old_weight,
                'TTL': 60,
                'ResourceRecords': [{'Value': old_cdn}]
            }
        },
        {
            'Action': 'UPSERT',
            'ResourceRecordSet': {
                'Name': domain,
                'Type': 'CNAME',
                'SetIdentifier': 'new-cdn',
                'Weight': new_weight,
                'TTL': 60,
                'ResourceRecords': [{'Value': new_cdn}]
            }
        }
    ]
    
    response = client.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={'Changes': changes}
    )
    
    return response

# Migration schedule
migration_schedule = [
    (1, 10),   # Day 1: 10% to new CDN
    (3, 25),   # Day 3: 25% to new CDN
    (5, 50),   # Day 5: 50% to new CDN
    (7, 75),   # Day 7: 75% to new CDN
    (10, 100), # Day 10: 100% to new CDN
]
```

## Cost Optimization

### Bandwidth Management

```yaml
bandwidth_optimization:
  image_optimization:
    formats: ["webp", "avif"]
    quality: 85
    responsive_images: true
    lazy_loading: true
  
  video_optimization:
    adaptive_bitrate: true
    codec: "h265"
    container: "mp4"
  
  compression:
    static_assets: "brotli"
    dynamic_content: "gzip"
    level: 6
```

### Origin Offload Strategies

```nginx
# Maximize origin offload
location / {
    # Cache everything by default
    proxy_cache_valid 200 1h;
    proxy_cache_valid 404 5m;
    
    # Ignore cache-busting parameters
    proxy_cache_key "$scheme$request_method$host$uri";
    
    # Serve stale content while updating
    proxy_cache_use_stale error timeout updating;
    proxy_cache_background_update on;
    
    # Lock to prevent thundering herd
    proxy_cache_lock on;
    proxy_cache_lock_timeout 5s;
}
```