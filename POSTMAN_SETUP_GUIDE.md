# Clisonix Cloud Postman Collections

Komplet Postman collections për testimin e Clisonix Cloud API.

## 📦 Files

- `Clisonix-Cloud-Complete-API.postman_collection.json` - Koleksioni kryesor me të gjitha endpoint-et
- `Clisonix-Cloud-Development.postman_environment.json` - Environment për development (localhost)
- `Clisonix-Cloud-Production.postman_environment.json` - Environment për production

## 🚀 Si të përdorni

### 1. Import në Postman

1. Hap Postman
2. Kliko "Import" (top-right)
3. Zgjedh "File"
4. Importo të dy files:
   - `Clisonix-Cloud-Complete-API.postman_collection.json`
   - `Clisonix-Cloud-Development.postman_environment.json` (ose Production)

### 2. Konfigurimi i Environment

1. Në Postman, zgjedh environment-in e duhur nga dropdown (top-right)
2. Për Development: përdor `Clisonix Cloud Development`
3. Për Production: përdor `Clisonix Cloud Production`

### 3. Testimi i API

1. Sigurohu që API server është running:
   ```bash
   cd apps/api
   python -m uvicorn main:app --host 0.0.0.0 --port 8000
   ```

2. Në Postman, ekzekuto requests nga folders:
   - 🔍 **System & Health** - Health checks dhe metrics
   - 🔐 **Authentication** - Login dhe user management
   - 🧠 **AI & Neural Processing** - AI agents dhe neural networks
   - 🌊 **Curiosity Ocean** - Groq LLM integration
   - 🧬 **EEG Processing** - EEG file upload dhe analysis
   - 🎵 **Audio Processing** - Audio file processing
   - 📊 **Monitoring** - Real-time metrics dhe analytics
   - 💰 **Crypto** - Cryptocurrency market data
   - 🏥 **Fitness** - Health dhe fitness metrics
   - 📈 **Reporting** - Report generation

## 🔧 Environment Variables

### Development
- `base_url`: `http://localhost:8000`
- `auth_token`: JWT token (auto-set nga login)
- `api_key`: API key për authenticated requests

### Production
- `base_url`: `https://api.clisonix.cloud`
- `auth_token`: JWT token
- `api_key`: Production API key

## 📝 Authentication Flow

1. **Create User** ose **Login** për të marrë JWT token
2. Token-i ruhet automatikisht në environment variable `auth_token`
3. Të gjitha requests e tjera përdorin token-in për authorization

## 🧪 Test Scripts

Collection-i përfshin test scripts që:
- Auto-save JWT tokens pas login
- Validon status codes (jo 5xx errors)
- Kontrollon response time (< 5000ms)
- Shton authorization headers automatikisht

## 📊 API Coverage

Collection-i mbulon këto module:

- ✅ **Core API** - Health, metrics, system status
- ✅ **Authentication** - User management, JWT tokens
- ✅ **AI Agents** - Neural processing, ML models
- ✅ **EEG Processing** - Brain wave analysis, file uploads
- ✅ **Audio Processing** - Spectrograms, audio analysis
- ✅ **Curiosity Ocean** - Groq LLM integration
- ✅ **Monitoring** - Real-time dashboards, metrics
- ✅ **Cryptocurrency** - Market data, coin details
- ✅ **Fitness & Health** - Training data, health metrics
- ✅ **Reporting** - Excel/PowerPoint report generation

## 🔄 Updates

Për të përditësuar collection-in:

1. Pull latest changes nga repository
2. Re-import collection files në Postman
3. Update environment variables sipas nevojës

## 🆘 Troubleshooting

### API Server nuk është running
```bash
# Development
cd apps/api
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Me Docker
docker-compose up api
```

### Authentication errors
- Sigurohu që ke bërë login dhe token-i është ruajtur
- Check environment variables në Postman

### File upload issues
- Për EEG/Audio uploads, zgjedh file nga file system
- Kontrollo Content-Type header (multipart/form-data)

---

**Clisonix Cloud** - Industrial AI Platform for EEG-to-Audio Processing
© 2025 Ledjan Ahmati</content>
<parameter name="filePath">c:\Users\pc\Clisonix-cloud\POSTMAN_SETUP_GUIDE.md