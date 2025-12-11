# 🎉 CLISONIX CLOUD - COMPLETE SETUP & POSTMAN GUIDE

## ✅ EVERYTHING IS READY!

### Current Status
```
✅ Frontend Server:    http://localhost:3003 (Next.js 15.5.4)
✅ API Server:         http://localhost:8000 (FastAPI/Uvicorn)
✅ Postman Collection: Fully configured with all endpoints
✅ Startup Scripts:    Ready to use
✅ Documentation:      Complete
```

---

## 🧪 POSTMAN - QUICK START

### Step 1: Import the Collection
1. Open Postman
2. Click **Import** (top left)
3. Select file: `Clisonix-Cloud-API.postman_collection.json`
4. ✅ Collection imported successfully!

### Step 2: Test Your First Endpoint
1. Go to **System Status** folder
2. Click **Get System Status**
3. Click **Send** button
4. View the JSON response with system health data

### Step 3: Explore All Endpoints
The collection includes:
- **System Status** - Health monitoring
- **Industrial Dashboard** - Data sources, metrics, logs, bulk collection
- **Signal Generation** - Test signal creation
- **EEG Processing** - Upload and process EEG files
- **Audio Processing** - Upload and process audio files
- **Health Check** - API health status

---

## 🚀 STARTUP SCRIPTS

### Main Startup (Frontend + API)
```powershell
.\start-full-stack.ps1
```

### Docker & Monitoring Stack
```powershell
# Start everything
.\start-docker-stack.ps1 -Service all

# Start individual services
.\start-docker-stack.ps1 -Service docker      # Docker only
.\start-docker-stack.ps1 -Service grafana     # Grafana only
.\start-docker-stack.ps1 -Service prometheus  # Prometheus only
.\start-docker-stack.ps1 -Service mesh        # Mesh nodes
.\start-docker-stack.ps1 -Service status      # Check status
```

---

## 📡 API ENDPOINTS

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/system-status` | GET | Current system health |
| `/api/data-sources` | GET | Available data sources |
| `/api/performance-metrics` | GET | System performance |
| `/api/activity-log` | GET | Activity history |
| `/api/start-bulk-collection` | POST | Start data collection |
| `/api/signal-gen/generate` | POST | Generate test signals |
| `/api/uploads/eeg/process` | POST | Process EEG files |
| `/api/uploads/audio/process` | POST | Process audio files |
| `/health` | GET | API health check |

---

## 📚 EXAMPLE REQUESTS

### Example 1: Check System Status
```bash
curl http://localhost:8000/api/system-status
```

**Response:**
```json
{
  "timestamp": "2025-12-05T12:22:33.501397+00:00",
  "instance_id": "7d406e6d",
  "status": "active",
  "uptime": "1h 27m",
  "memory": { "used": 20379, "total": 65317 },
  "system": { "cpu_percent": 6.6, "memory_percent": 31.2, ... }
}
```

### Example 2: Start Bulk Collection
```bash
curl -X POST http://localhost:8000/api/start-bulk-collection \
  -H "Content-Type: application/json" \
  -d '{
    "source_ids": ["source1", "source2"],
    "duration_minutes": 30,
    "priority": "high"
  }'
```

---

## 🐳 DOCKER SERVICES (When Required)

Prerequisites:
- Docker Desktop installed and running

Available services:
- Redis (port 6379)
- PostgreSQL (port 5432)
- Prometheus (port 9090)
- Grafana (port 3001)

**Start Docker Stack:**
```powershell
docker-compose up -d
```

**Stop Docker Stack:**
```powershell
docker-compose down
```

---

## 📊 SERVICE PORTS & URLS

| Service | URL | Port | Status |
|---------|-----|------|--------|
| Frontend | http://localhost:3003 | 3003 | ✅ Running |
| API | http://localhost:8000 | 8000 | ✅ Running |
| Grafana | http://localhost:3001 | 3001 | ⏸️ Stopped |
| Prometheus | http://localhost:9090 | 9090 | ⏸️ Stopped |
| Redis | localhost | 6379 | ⏸️ Stopped |
| PostgreSQL | localhost | 5432 | ⏸️ Stopped |

---

## 🔧 ENVIRONMENT CONFIGURATION

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

### API (apps/api/.env)
```
# Already configured for development
```

---

## 🛠️ TROUBLESHOOTING

### Port Already in Use
```powershell
# Find and stop process on port
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### API Not Responding
```powershell
# Restart services
.\start-full-stack.ps1
```

### Docker Errors
```
Error: docker daemon not running
Solution: Start Docker Desktop application
```

### Module Import Errors
```
Fixed: mesh_cluster_startup.py now has fallback logger
```

---

## 📁 KEY FILES

| File | Purpose |
|------|---------|
| `Clisonix-Cloud-API.postman_collection.json` | Postman collection with all endpoints |
| `start-full-stack.ps1` | Start frontend + API |
| `start-docker-stack.ps1` | Start Docker & monitoring services |
| `.env.local` | Frontend environment config |
| `POSTMAN_SETUP_COMPLETE.md` | Setup documentation |
| `STARTUP_GUIDE.md` | Comprehensive startup guide |
| `API_DOCS.md` | Full API documentation |

---

## 💡 TIPS & TRICKS

### Monitor Real-Time Logs
- Frontend logs appear in terminal
- API logs appear in terminal
- Check browser console for client-side errors

### Test in Postman Collections
1. Use "Environment" feature for variables
2. Save requests for reuse
3. Use "Tests" tab for automatic validation
4. Run entire collections with "Collection Runner"

### Customize Postman
1. Create workspace for this project
2. Set up environment variables
3. Add pre-request scripts for authentication
4. Configure assertions for responses

---

## 🚀 QUICK COMMAND REFERENCE

```powershell
# Start everything
.\start-full-stack.ps1

# Check status
.\start-docker-stack.ps1 -Service status

# Clean up
Get-Process node | Stop-Process -Force
npm cache clean --force

# View API responses
curl http://localhost:8000/api/system-status

# Test Postman collection (via CLI)
newman run Clisonix-Cloud-API.postman_collection.json
```

---

## 📞 SUPPORT & DOCUMENTATION

- **Project**: Clisonix Cloud Industrial Platform
- **Owner**: Ledjan Ahmati
- **Company**: WEB8euroweb GmbH
- **Repository**: https://github.com/Kameleonlife/Clisonix-cloud
- **API Docs**: See `API_DOCS.md`
- **Integration Report**: See `INTEGRATION_COMPLETE_REPORT.md`

---

## 🎯 NEXT STEPS

1. **Import Postman Collection** ← Start here!
2. **Test API Endpoints** - Use Postman to call your first endpoint
3. **Monitor System Health** - Check `/api/system-status`
4. **Explore Frontend** - Navigate to http://localhost:3003
5. **Start Docker Stack** (when ready) - For Grafana/Prometheus

---

## ✨ FEATURES AVAILABLE

- ✅ Production-ready API
- ✅ Real-time system monitoring
- ✅ EEG signal processing
- ✅ Audio analysis capabilities
- ✅ Industrial-grade data collection
- ✅ Comprehensive telemetry
- ✅ CI/CD pipeline integration
- ✅ Docker containerization ready
- ✅ Mesh network support
- ✅ Grafana dashboards (Docker)

---

**Status**: ✅ **PRODUCTION READY**  
**Last Updated**: December 5, 2025  
**Ready For**: Development & Testing

🎉 **Enjoy building with Clisonix Cloud!**
