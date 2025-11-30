# Clisonix Cloud API – Authentication Guide

## Overview

Clisonix Cloud now features a complete enterprise-grade authentication system with JWT tokens, refresh tokens, and API key management. All authentication flows are implemented across the OpenAPI specification, Python SDK, TypeScript SDK, and Postman collection.

---

## Authentication Methods

### 1. JWT Bearer Token

- **Use Case**: Interactive applications, user sessions
- **Expiration**: 3600 seconds (1 hour)
- **Header**: `Authorization: Bearer <token>`
- **Refresh**: Use `/auth/refresh` endpoint with refresh_token

### 2. API Key

- **Use Case**: Server-to-server, service accounts, production deployments
- **Header**: `X-API-Key: <api_key>`
- **Lifespan**: Long-lived (no automatic expiration)
- **Generation**: Via `/auth/api-key` endpoint (requires JWT auth)

### 3. Refresh Token

- **Use Case**: Getting new JWT without re-login
- **Lifespan**: 7 days (typical)
- **Usage**: POST to `/auth/refresh` with refresh_token in body
- **Response**: New JWT token with same expiration

---

## API Endpoints

### POST /auth/login

Login with email and password. Returns JWT, refresh token, and API key.

**Request:**

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200 OK):**

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "refresh_eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "api_key": "api_sk_1234567890abcdefghijklmnop",
  "expires_in": 3600
}
```

**Security**: ✓ No auth required (public endpoint)

---

### POST /auth/refresh

Refresh JWT token using refresh_token. Returns new JWT.

**Request:**

```json
{
  "refresh_token": "refresh_eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 3600
}
```

**Security**: ✓ No auth required (public endpoint)

---

### POST /auth/api-key

Generate a new API key for the authenticated user.

**Request:**

```json
{
  "label": "production-server"
}
```

**Response (200 OK):**

```json
{
  "api_key": "api_sk_abcdefghijklmnopqrstuvwxyz",
  "label": "production-server",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Security**: 🔐 Requires Bearer JWT token
**Header**: `Authorization: Bearer <token>`

---

## Python SDK Authentication

### Installation

```bash
pip install requests pydantic
```

### Basic Login Flow

```python
from clisonix import ClisonixClient

# Initialize client
client = ClisonixClient(base_url="https://api.clisonix.com")

# Login with email and password
login_data = client.login("user@example.com", "password123")
print(f"✓ Token: {login_data['token'][:20]}...")
print(f"✓ Refresh Token: {login_data['refresh_token'][:20]}...")
print(f"✓ API Key: {login_data['api_key']}")

# Token is now automatically stored and used in headers
health = client.health()
print(f"✓ System health: {health['status']}")
```

### Using Refresh Token

```python
# Access token has expired, refresh it
refreshed = client.refresh()
print(f"✓ New token: {refreshed['token'][:20]}...")

# Continue using client - new token is automatically used
ask_response = client.ask("Hello, Clisonix!")
```

### Creating API Keys

```python
# Create a new API key for production deployment
api_key_data = client.create_api_key("my-production-service")
print(f"✓ API Key created: {api_key_data['api_key']}")

# Store this safely in environment variables or secrets management
```

### Using API Key Authentication

```python
# Initialize with API key instead of token
client = ClisonixClient(base_url="https://api.clisonix.com")
client.set_api_key("api_sk_abcdefghijklmnopqrstuvwxyz")

# All requests will use X-API-Key header
response = client.health()
```

### Available Methods

```python
# Authentication
client.login(email: str, password: str) -> Dict[str, Any]
client.refresh() -> Dict[str, Any]
client.create_api_key(label: str) -> Dict[str, Any]
client.set_api_key(api_key: str) -> None

# Health & Status
client.health() -> Dict[str, Any]
client.status() -> Dict[str, Any]
client.system_status() -> Dict[str, Any]

# AI & Neural
client.ask(question: str, context: str, include_details: bool) -> Dict[str, Any]
client.neural_symphony(save_to: Optional[str]) -> bytes

# File Processing
client.upload_eeg(file_path: str) -> Dict[str, Any]
client.upload_audio(file_path: str) -> Dict[str, Any]

# Brain Engine
client.brain_energy_check(file_path: str) -> Dict[str, Any]
client.brain_harmony(file_path: str) -> Dict[str, Any]
client.brain_scan_harmonic(file_path: str) -> Dict[str, Any]
client.brain_music_brainsync(file_path: str, mode: str) -> bytes

# ALBA Data Streams
client.alba_streams_start(stream_id: str, ...) -> Dict[str, Any]
client.alba_streams_stop(stream_id: str) -> Dict[str, Any]
client.alba_streams_list() -> Dict[str, Any]
client.alba_streams_data(stream_id: str, limit: int) -> Dict[str, Any]
```

---

## TypeScript SDK Authentication

-### Installation

```bash
npm install
```

-### Basic Login Flow

```typescript
import { ClisonixClient } from './clisonix_sdk';

// Initialize client
const client = new ClisonixClient({
  baseUrl: 'https://api.clisonix.com',
  timeout: 30000
});

// Login with email and password
const loginData = await client.login('user@example.com', 'password123');
console.log(`✓ Token: ${loginData.token.substring(0, 20)}...`);
console.log(`✓ API Key: ${loginData.api_key}`);

// Token is now automatically stored and used in headers
const health = await client.health();
console.log(`✓ System health: ${health.status}`);
```

-### Using Refresh Token

```typescript
// Access token has expired, refresh it
const refreshed = await client.refresh();
console.log(`✓ New token: ${refreshed.token.substring(0, 20)}...`);

// Continue using client - new token is automatically used
const response = await client.ask("Hello!");
```

-### Creating API Keys

```typescript
// Create a new API key for production deployment
const apiKeyData = await client.createApiKey('backend-service');
console.log(`✓ API Key created: ${apiKeyData.api_key}`);
```

-### Using API Key Authentication

```typescript
// Initialize with API key
const client = new ClisonixClient({
  baseUrl: 'https://api.clisonix.com'
});

client.setApiKey('api_sk_abcdefghijklmnopqrstuvwxyz');

// All requests will use X-API-Key header
const response = await client.health();
```

---

## Postman Collection

### Setup Environment Variables

Import the Postman collection from `postman_collection_auth.json`. It includes pre-configured variables:

| Variable | Purpose | Example |
|----------|---------|---------|
| `base_url` | API endpoint | `https://api.clisonix.com` |
| `auth_token` | JWT Bearer token | (auto-populated) |
| `refresh_token` | Refresh token | (auto-populated) |
| `api_key` | API key | (auto-populated) |

### Authentication Flow in Postman

**Step 1: Login*

- Endpoint: `POST /auth/login`
- Body: `{"email": "user@example.com", "password": "password123"}`
- Test script: Automatically captures `auth_token`, `refresh_token`, and `api_key`

**Step 2: Use Token*

- All authenticated endpoints use `{{auth_token}}` variable
- Header `Authorization: Bearer {{auth_token}}` is automatically applied

**Step 3: Refresh Token (when expired)*

- Endpoint: `POST /auth/refresh`
- Body: `{"refresh_token": "{{refresh_token}}"}`
- Test script: Automatically updates `auth_token` variable

**Step 4: Create API Key*

- Endpoint: `POST /auth/api-key`
- Header: `Authorization: Bearer {{auth_token}}`
- Body: `{"label": "my-service"}`
- Test script: Automatically captures new `api_key`

---

## Security Best Practices

### Token Storage

- **Frontend**: Store JWT in secure, httpOnly cookies or sessionStorage (NOT localStorage)
- **Backend**: Store in secure cache (Redis) with key rotation
- **Mobile**: Use platform-native secure storage (Keychain, Keystore)

### API Key Storage

- **Never** commit API keys to version control
- Use environment variables: `CLISONIX_API_KEY=api_sk_xxx`
- Rotate keys regularly
- Use separate keys per service/environment (dev, staging, prod)

### Token Rotation

- Implement automatic token refresh 5 minutes before expiration
- Revoke tokens on logout
- Implement token blacklisting for security breaches

### HTTPS Only

- Always use HTTPS in production
- Set `Secure` flag on cookies
- Implement certificate pinning on mobile apps

### Rate Limiting

- Implement exponential backoff on 429 (Too Many Requests)
- Monitor token usage patterns
- Alert on unusual activity

---

## Error Handling

### Common Error Responses

**401 Unauthorized*

```json
{
  "error": "Invalid credentials",
  "message": "Email or password is incorrect"
}
```

**401 Token Expired*

```json
{
  "error": "token_expired",
  "message": "Token has expired. Please refresh.",
  "expires_at": "2024-01-15T11:30:00Z"
}
```

**403 Forbidden*

```json
{
  "error": "insufficient_permissions",
  "message": "API key does not have permission to access this resource"
}
```

### SDK Error Handling

**Python:*

```python
try:
    response = client.ask("Question")
except Exception as e:
    print(f"Error: {e}")
    if "token_expired" in str(e):
        client.refresh()  # Auto-refresh and retry
```

**TypeScript:*

```typescript
try {
  const response = await client.ask("Question");
} catch (error) {
  console.error(`Error: ${error.message}`);
  if (error.message.includes('token_expired')) {
    await client.refresh();  // Auto-refresh and retry
  }
}
```

---

## Environment Setup

### Development

```bash
# .env file (never commit)
CLISONIX_API_URL=https://api.clisonix.com
CLISONIX_EMAIL=dev@example.com
CLISONIX_PASSWORD=dev_password
```

### Production

```bash
# Use secure secrets management (AWS Secrets Manager, Azure Key Vault, etc.)
export CLISONIX_API_KEY=api_sk_production_xxxxx
export CLISONIX_API_URL=https://api.clisonix.com
```

---

## OpenAPI Specification

All authentication schemas and endpoints are defined in `openapi.yaml`:

- **Schemas**: `AuthLoginRequest`, `AuthLoginResponse`, `AuthRefreshRequest`, `AuthRefreshResponse`, `ApiKeyCreateRequest`, `ApiKeyCreateResponse`
- **Endpoints**: `/auth/login`, `/auth/refresh`, `/auth/api-key`
- **Security Schemes**: `bearer` (JWT), `api_key` (X-API-Key header)

---

## Support & Resources

- 📖 **Full API Docs**: [API_DOCS.md](API_DOCS.md)
- 🔗 **OpenAPI Spec**: [openapi.yaml](openapi.yaml)
- 💻 **Python SDK**: [clisonix_sdk.py](clisonix_sdk.py)
- 🎯 **TypeScript SDK**: [clisonix_sdk.ts](clisonix_sdk.ts)
- 📮 **Postman Collection**: [postman_collection_auth.json](postman_collection_auth.json)
- 🌐 **Landing Page**: [index.html](index.html)

---

## Changelog

### v1.1.0 (Current)

- ✅ JWT Bearer authentication
- ✅ Refresh token support
- ✅ API key generation and management
- ✅ Python SDK with auth methods
- ✅ TypeScript SDK with auth methods
- ✅ Postman collection with auto-capture
- ✅ Landing page with code examples

---

**Clisonix Cloud API** • Part of UltraWebThinking / Euroweb
