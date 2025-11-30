# Clisonix Cloud API – Quick Start Guide

## 🚀 5-Minute Setup

### Prerequisites
- Node.js 14+ or Python 3.8+
- API endpoint: `https://api.clisonix.com`
- Valid email account for login

---

## Python Quick Start

### 1. Install
```bash
pip install requests
# Copy clisonix_sdk.py to your project
```

### 2. Login & Use
```python
from clisonix_sdk import ClisonixClient

# Create client
client = ClisonixClient(base_url="https://api.clisonix.com")

# Login
login = client.login("user@example.com", "password123")
print(f"✓ Token: {login['token'][:20]}...")

# Use API (token auto-included)
health = client.health()
print(f"✓ Health: {health['status']}")

# Refresh when expired
new_token = client.refresh()
print(f"✓ New token: {new_token['token'][:20]}...")

# Create API key for production
api_key = client.create_api_key("my-server")
print(f"✓ API Key: {api_key['api_key']}")
```

### 3. Use API Key Instead
```python
# For server-to-server auth
client = ClisonixClient(base_url="https://api.clisonix.com")
client.set_api_key("api_sk_your_key_here")

# All requests now use X-API-Key header
response = client.health()
```

---

## TypeScript Quick Start

### 1. Install
```bash
npm install
# Copy clisonix_sdk.ts to your project
```

### 2. Login & Use
```typescript
import { ClisonixClient } from './clisonix_sdk';

// Create client
const client = new ClisonixClient({
  baseUrl: 'https://api.clisonix.com'
});

// Login
const login = await client.login('user@example.com', 'password123');
console.log(`✓ Token: ${login.token.substring(0, 20)}...`);

// Use API (token auto-included)
const health = await client.health();
console.log(`✓ Health: ${health.status}`);

// Refresh when expired
const newToken = await client.refresh();
console.log(`✓ New token: ${newToken.token.substring(0, 20)}...`);

// Create API key for production
const apiKey = await client.createApiKey('my-server');
console.log(`✓ API Key: ${apiKey.api_key}`);
```

### 3. Use API Key Instead
```typescript
// For server-to-server auth
const client = new ClisonixClient({
  baseUrl: 'https://api.clisonix.com'
});
client.setApiKey('api_sk_your_key_here');

// All requests now use X-API-Key header
const response = await client.health();
```

---

## Postman Quick Start

### 1. Import Collection
1. Open Postman
2. Click "Import" → "Upload Files"
3. Select `postman_collection_auth.json`
4. Collection appears in sidebar

### 2. Setup Environment Variables
Collection includes pre-configured variables:
- `base_url`: `https://api.clisonix.com`
- `auth_token`: (auto-populated after login)
- `refresh_token`: (auto-populated after login)
- `api_key`: (auto-populated after creating key)

### 3. Test Authentication Flow
**Step 1: Login**
1. Go to "Auth" folder → "Login"
2. Edit email/password in request body
3. Click "Send"
4. ✓ Token auto-captured to `auth_token` variable

**Step 2: Use Token**
1. Any authenticated endpoint automatically uses `{{auth_token}}`
2. Click "Send" to test

**Step 3: Refresh (if expired)**
1. Go to "Auth" folder → "Refresh Token"
2. Click "Send"
3. ✓ New token auto-captured

**Step 4: Create API Key**
1. Go to "Auth" folder → "Create API Key"
2. Edit label in request body (e.g., "production-server")
3. Click "Send"
4. ✓ API key auto-captured to `api_key` variable

---

## Authentication Methods

### Method 1: JWT Bearer Token (Recommended for Web Apps)
```
POST /auth/login
Body: {"email": "user@example.com", "password": "password"}
Response: {token, refresh_token, api_key, expires_in}

Usage:
Header: Authorization: Bearer <token>
```

### Method 2: API Key (Recommended for Servers)
```
1. First login to get initial API key, OR
2. POST /auth/api-key with Bearer token to create new key

Usage:
Header: X-API-Key: api_sk_xxxxx
```

### Method 3: Refresh Token (When JWT Expires)
```
POST /auth/refresh
Body: {"refresh_token": "refresh_xxxxx"}
Response: {token, expires_in}

Usage:
Header: Authorization: Bearer <new_token>
```

---

## Common Errors & Solutions

### ❌ "401 Invalid credentials"
**Problem**: Email or password incorrect
**Solution**: Double-check email and password

### ❌ "401 Token expired"
**Problem**: JWT token has expired (after 1 hour)
**Solution**: Call `client.refresh()` to get new token

### ❌ "403 Forbidden"
**Problem**: API key doesn't have permission
**Solution**: Ensure using correct API key for endpoint

### ❌ "429 Too Many Requests"
**Problem**: Rate limit exceeded
**Solution**: Wait 60 seconds and retry

---

## Environment Setup

### Development (.env)
```bash
CLISONIX_API_URL=https://api.clisonix.com
CLISONIX_EMAIL=dev@example.com
CLISONIX_PASSWORD=dev_password
```

### Production (Secrets Manager)
```bash
# Never commit these!
CLISONIX_API_KEY=api_sk_production_xxxxx
CLISONIX_API_URL=https://api.clisonix.com
```

### Load from Environment

**Python:**
```python
import os
from clisonix_sdk import ClisonixClient

client = ClisonixClient(base_url=os.getenv("CLISONIX_API_URL"))
client.set_api_key(os.getenv("CLISONIX_API_KEY"))
```

**TypeScript:**
```typescript
import { ClisonixClient } from './clisonix_sdk';

const client = new ClisonixClient({
  baseUrl: process.env.CLISONIX_API_URL
});
client.setApiKey(process.env.CLISONIX_API_KEY);
```

---

## API Examples

### Example 1: Ask a Question
```python
client = ClisonixClient(base_url="https://api.clisonix.com")
client.login("user@example.com", "password")

answer = client.ask("What is Clisonix?", include_details=True)
print(answer['answer'])
print(answer['details'])
```

### Example 2: Start Data Stream
```python
stream = client.alba_streams_start(
    stream_id="my-stream",
    channels=["C3", "C4", "Pz"],
    sampling_rate_hz=256
)
print(f"Stream started: {stream['stream_id']}")

# Get data
data = client.alba_streams_data(stream['stream_id'], limit=100)
print(f"Data points: {len(data['data_points'])}")

# Stop stream
client.alba_streams_stop(stream['stream_id'])
```

### Example 3: Generate BrainSync Music
```python
# EEG file processing and music generation
music_bytes = client.brain_music_brainsync(
    file_path="/path/to/eeg.csv",
    mode="relax",  # or "focus", "sleep"
    save_to="/output/music.wav"
)
print(f"✓ Music generated: {len(music_bytes)} bytes")
```

### Example 4: Check System Health
```python
health = client.health()
print(f"Status: {health['status']}")
print(f"Uptime: {health['uptime']} seconds")

status = client.status()
print(f"Brain modules: {status['brain_modules']}")
print(f"Active streams: {status['alba_streams']}")
```

---

## Complete Authentication Flow

```
┌─────────────────────────────────────────────────────────┐
│                    Your Application                     │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ├─→ 1. Login
                       │     client.login(email, password)
                       │     ↓
                       │     API: POST /auth/login
                       │     ↓
                       │     Return: token, refresh_token, api_key
                       │     ↓
                       │     SDK Auto-stores
                       │
                       ├─→ 2. Use API
                       │     client.health()  ← uses auto-stored token
                       │     client.ask(...)  ← includes Bearer header
                       │     ↓
                       │     API: GET /health
                       │     Header: Authorization: Bearer <token>
                       │
                       ├─→ 3. Token Expires (1 hour)
                       │     client.refresh()
                       │     ↓
                       │     API: POST /auth/refresh
                       │     Body: {refresh_token: "..."}
                       │     ↓
                       │     Return: new token
                       │     ↓
                       │     SDK Auto-updates
                       │
                       └─→ 4. Production (API Key)
                             client.set_api_key("api_sk_xxx")
                             ↓
                             All requests: Header: X-API-Key: api_sk_xxx
```

---

## Next Steps

1. ✅ **Read AUTHENTICATION.md** – Full authentication guide
2. ✅ **Review openapi.yaml** – Complete API specification
3. ✅ **Check index.html** – Landing page with examples
4. ✅ **Deploy SDKs** – Python (PyPI) and TypeScript (NPM)
5. ✅ **Implement endpoints** – Login, refresh, api-key

---

## Resources

- 📖 **Full Guide**: [AUTHENTICATION.md](AUTHENTICATION.md)
- 🔗 **API Spec**: [openapi.yaml](openapi.yaml)
- 💻 **Python SDK**: [clisonix_sdk.py](clisonix_sdk.py)
- 🎯 **TypeScript SDK**: [clisonix_sdk.ts](clisonix_sdk.ts)
- 📮 **Postman**: [postman_collection_auth.json](postman_collection_auth.json)
- 🌐 **Landing Page**: [index.html](index.html)
- 📋 **Implementation**: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)

---

**Clisonix Cloud** • Enterprise Neural Audio Engine  
**Part of UltraWebThinking / Euroweb**
